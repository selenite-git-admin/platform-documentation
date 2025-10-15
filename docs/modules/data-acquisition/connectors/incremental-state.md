# Reference: Incremental Extraction and State

## Purpose
This reference explains how incremental extraction works when connectors are stateless. 
It defines what the connector must do, what the platform does, and how the state registry preserves progress between runs. 
The goal is a clear division of responsibilities so that connectors remain simple and reliable while the platform provides durable state and governance.

## Scope
This document applies to all connectors and all runner types. 
It covers cursor fields, state representation, run lifecycle, checkpointing, idempotency, and failure handling. 
It also provides examples for SAP OData, Salesforce REST, JDBC, and file based ingestion. 
Streaming and change data capture are noted for completeness with a focus on how they record checkpoints.

## Key Concepts

### Cursor
A cursor is the field or token that orders changes at the source. 
Common cursors are timestamps such as LastUpdated or sequence identifiers such as SystemModstamp or an auto incrementing id. 
The cursor must be monotonic for the scope of the selected stream. 
If a cursor is not available, the connector uses full refresh or a synthetic strategy agreed during configuration.

### Stateless Connector
The connector does not persist any progress locally. 
It accepts an input state from the orchestrator and returns an output state when it finishes. 
It is safe to scale, retry, or redeploy the connector without losing progress.

### State Registry
The platform stores a committed state per tenant, per connector, and per stream. 
The state registry is the single source of truth for incremental progress. 
It supports atomic updates so that only successful runs advance the checkpoint.

A minimal state record looks like this:
```json
{
  "tenant_id": "t1",
  "connector_id": "sap_s4hana_odata",
  "stream_id": "sap.s4hana.gl_accounts",
  "last_cursor": "2025-09-30T23:59:59Z",
  "cursor_field": "LastUpdated",
  "version": 7
}
```

## Run Lifecycle

1. Initialize 
   The orchestrator reads the last committed state from the registry. 
   If no state exists it uses a configured baseline or requests a full refresh.

2. Execute 
   The orchestrator launches the connector with the input state. 
   The connector queries the source with a predicate that selects records newer than the input cursor. 
   The connector emits records to the Bronze destination.

3. Track 
   While reading data the connector tracks the highest cursor value seen for the stream. 
   This is maintained in memory only for the duration of the run.

4. Commit 
   When the run finishes successfully the connector returns the new max cursor to the orchestrator. 
   The orchestrator writes the new state to the registry atomically. 
   If the run fails the state is not advanced.

5. Repeat 
   Future runs continue from the committed checkpoint. 
   The process is identical regardless of runner type.

## Connector Contract

### Input State
The orchestrator passes state to the connector at start. 
The connector must treat it as read only.

```json
{
  "stream_id": "sap.s4hana.gl_accounts",
  "cursor_field": "LastUpdated",
  "cursor_value": "2025-09-30T23:59:59Z"
}
```

### Output State
The connector returns one output state object per stream. 
Only successful completion should return a value. 
Failures return no state and the orchestrator keeps the previous checkpoint.

```json
{
  "stream_id": "sap.s4hana.gl_accounts",
  "cursor_field": "LastUpdated",
  "cursor_value": "2025-10-02T11:20:45Z",
  "records_emitted": 12894
}
```

### Manifest Hints
Manifests describe how state is handled for each stream. 
The manifest does not include the state value itself.

```yaml
streams:
  - id: sap.s4hana.gl_accounts
    key: [AccountID]
    cursor: LastUpdated
    schema_strategy: discovery
    state_handling: platform_registry
```

## Query Patterns

### Timestamp cursor
```sql
SELECT * 
FROM GLAccounts 
WHERE LastUpdated > :cursor_value 
ORDER BY LastUpdated, AccountID 
LIMIT :page_size;
```

### Numeric id cursor
```sql
SELECT * 
FROM orders 
WHERE id > :cursor_value 
ORDER BY id 
LIMIT :page_size;
```

### Salesforce REST
Use SystemModstamp and the WHERE clause in SOQL. 
```sql
SELECT Id, Name, SystemModstamp 
FROM Account 
WHERE SystemModstamp > 2025-09-30T23:59:59Z 
ORDER BY SystemModstamp ASC 
LIMIT 2000
```

### OData
Use server side filtering with a timestamp cursor. 
```
GET /GLAccounts?$filter=LastUpdated gt 2025-09-30T23:59:59Z&$orderby=LastUpdated asc&$top=1000
```

## Idempotency and Ordering
Connectors must emit an envelope that allows idempotent upserts in Bronze. 
Include a deterministic key and the cursor value with every record. 
If the source uses eventual consistency, use greater than or equal to in the next run and de duplicate by key plus cursor during landing.

Example envelope:
```json
{
  "stream": "sap.s4hana.gl_accounts",
  "emitted_at": "2025-10-02T11:21:03Z",
  "cursor": "2025-10-02T11:20:45Z",
  "key": {"AccountID": "100-445"},
  "record": { "...": "..." }
}
```

## Exactly Once and At Least Once
Connectors operate in an at least once delivery model during extraction. 
Bronze landing must be idempotent so that retries do not create duplicates. 
Use a compound key of stream id, key fields, and cursor to achieve idempotent writes. 
If the destination supports transactions, use upsert semantics keyed on that compound key.

## Failure Handling

### Mid run failure
If a run fails after emitting some records the checkpoint is not advanced. 
On retry the connector will read those records again. 
Idempotent landing ensures there are no duplicates in Bronze.

### Partial page failure
If a page fails during extraction use smaller page sizes or exponential backoff. 
Only advance the in memory max cursor when a page is fully acknowledged by the sink.

### Source clock skew
If the source clock lags or jumps forward use server timestamps where possible. 
Alternatively include a safety window. 
For example use LastUpdated greater than or equal to cursor minus five minutes.

```yaml
safety_window: PT5M
```

## Examples

### SAP OData example
Input state
```json
{"stream_id":"sap.s4hana.gl_accounts","cursor_field":"LastUpdated","cursor_value":"2025-09-30T23:59:59Z"}
```
Request
```
GET /GLAccounts?$filter=LastUpdated gt 2025-09-30T23:59:59Z&$orderby=LastUpdated asc&$top=1000
```
Output state
```json
{"stream_id":"sap.s4hana.gl_accounts","cursor_field":"LastUpdated","cursor_value":"2025-10-02T11:20:45Z","records_emitted":12894}
```

### Salesforce example
Input state
```json
{"stream_id":"sf.account","cursor_field":"SystemModstamp","cursor_value":"2025-09-30T23:59:59Z"}
```
SOQL
```sql
SELECT Id, Name, SystemModstamp 
FROM Account 
WHERE SystemModstamp > 2025-09-30T23:59:59Z 
ORDER BY SystemModstamp ASC 
LIMIT 2000
```
Output state
```json
{"stream_id":"sf.account","cursor_field":"SystemModstamp","cursor_value":"2025-10-02T09:12:04Z","records_emitted":44201}
```

### JDBC example
Input state
```json
{"stream_id":"jdbc.public.customers","cursor_field":"updated_at","cursor_value":"2025-09-30T23:59:59Z"}
```
SQL
```sql
SELECT * 
FROM public.customers 
WHERE updated_at > '2025-09-30 23:59:59+00' 
ORDER BY updated_at, id 
LIMIT 10000
```
Output state
```json
{"stream_id":"jdbc.public.customers","cursor_field":"updated_at","cursor_value":"2025-10-02T08:00:00Z","records_emitted":9903}
```

### File ingestion example
Input state
```json
{"stream_id":"file.s3.sales_orders_csv","cursor_field":"_file_checkpoint","cursor_value":"s3://bucket/sales/orders/2025-09-30/orders_2359.csv.gz#sha256=abc"}
```
Selection
```
List files under s3://bucket/sales/orders/ newer than the last processed file and checksum.
```
Output state
```json
{"stream_id":"file.s3.sales_orders_csv","cursor_field":"_file_checkpoint","cursor_value":"s3://bucket/sales/orders/2025-10-02/orders_1200.csv.gz#sha256=def","records_emitted":125000}
```

## Streaming and CDC
Streaming and change data capture record offsets instead of timestamps. 
The connector reports the last acknowledged offset and the registry commits it transactionally. 
Examples include Kafka partition offsets and database log sequence numbers.

Example state
```json
{"stream_id":"jdbc.public.orders.cdc","cursor_field":"lsn","cursor_value":"0000:001A:00F3"}
```

## Security Considerations
State values can contain identifiers or timestamps. 
Treat state as sensitive metadata. 
Encrypt state at rest, restrict access by tenant, and never write raw state into unsecured logs.

## Testing
Unit tests must cover the following:
- The connector respects the input state and does not read older data. 
- The connector returns the maximum cursor seen across all pages. 
- Idempotent landing is preserved during retries. 
- Safety window logic is applied when configured. 

Integration tests must run against a sandbox source and verify at least one full incremental cycle and one retry cycle.

## Principles
- The connector is stateless. 
- The platform registry is the single source of truth for checkpoints. 
- Bronze landing must be idempotent. 
- Cursors must be monotonic or the connector must fall back to full refresh. 
- All state updates must be atomic and audited.

## Exclusions
This reference does not define downstream Silver or Gold mapping behavior. 
It does not cover tenant onboarding flows or UI behavior for schedules and credentials.
