# SCD Runtime Loader Pattern

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
Defines the minimal job pattern to apply SCD merges in PostgreSQL using the SQL templates. Runtime schedules and executes the job. No extra services are introduced.

## Inputs
- Staging table `{{schema}}.{{staging}}` with `business_key`, attributes, and optional `event_ts`.
- Merge type: `s1` or `s2`.
- Correlation id for Evidence Ledger.

## Steps
1. Begin transaction with serializable isolation.
2. Execute SCD merge SQL (`s1` or `s2`).
3. Update DRR with dataset refresh completion.
4. Emit audit event with counts and correlation id.
5. Commit transaction.

## Pseudocode

```sql
-- example transaction wrapper
begin;
set local transaction isolation level serializable;

-- run the merge block for SCD1 or SCD2

-- record audit (counts from CTEs or rowcount())
-- select pg_notify('evidence_bus', json_build_object(...));

commit;
```

## Retry
- Catch SQLSTATE `40001` and retry up to 3 times with jitter.
- On repeated failure, alert and leave staging intact for rerun.

## Metrics
- Rows inserted, rows updated, rows closed (SCD2).
- Merge duration and retries.
- Staging to dimension lag seconds.

## Ownership
- Runtime owns scheduling and retries.
- Store owns SQL templates and table design.
- DRR records freshness for the dimension and views.