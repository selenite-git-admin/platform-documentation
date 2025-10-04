# SAP ODATA

## Purpose
This document describes the development requirements and behaviors for the SAP S4HANA OData connector. 
It explains discovery, incremental extraction, supported runners and network patterns, and how the connector integrates with platform registries. 
It is written for developers who implement, test, and certify the connector.

## Scope
Reads data from SAP S4HANA using OData services. 
Supports discovery from the OData metadata endpoint, incremental extraction using timestamp cursors, and batch pagination. 
Includes authentication, request shaping, throttling, retries, error handling, observability, and CI certification. 
This page does not include tenant onboarding instructions or customer runbooks.

## Supported Versions
- SAP S4HANA on premise OData services
- SAP S4HANA Cloud OData services
The connector expects standard service metadata to be available and reachable over the selected network path.

## Authentication
Supported modes
- OAuth 2.0 client credentials or authorization code when provided by the gateway
- Basic authentication for lab systems when allowed by policy
Secrets are retrieved from the platform secrets store at runtime.

## Network and Deployment
Supported runners
- AWS Fargate for long running extracts and heavier dependencies
- AWS Lambda for light extracts within limits

Supported network patterns
- Site to site VPN to reach internal SAP gateways
- AWS PrivateLink when an internal NLB is exposed
- NAT allowlist for public endpoints if approved
Use VPC endpoints for AWS services such as S3, STS, and Secrets Manager.

## Discovery
Implement discover to read the OData metadata document and enumerate entity sets. 
For each entity set the connector emits a stream with an identifier, keys, and an optional cursor proposal.

Example discovery output
```yaml
streams:
  - id: sap.s4hana.gl_accounts
    key: [AccountID]
    cursor: LastUpdated
  - id: sap.s4hana.customers
    key: [CustomerID]
    cursor: UpdatedOn
```

If keys are not available in metadata the connector records a missing key condition and requires configuration in the connection profile. 
If no cursor is available the connector proposes full refresh with an option to configure a baseline.

## Incremental Extraction
Preferred cursor fields include LastUpdated or ChangeTimestamp. 
The connector accepts an input state from the orchestrator and returns the maximum cursor seen.

Example request pattern
```
GET /GLAccounts?$filter=LastUpdated gt 2025-09-30T23:59:59Z&$orderby=LastUpdated asc&$top=1000
```

Paging
- Use server paging tokens if available
- Otherwise use skip and top with an upper bound on total pages per run

Safety window
- Apply a safety window when clock skew is suspected
- Example configuration in the connection profile
```yaml
safety_window: PT5M
```

## Manifest
Minimal manifest fragment
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::sap::sap_s4hana::odata
name: SAP S4HANA OData Connector
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: sap
  product: s4hana
  method: odata
runtime:
  supported_runners: [fargate, lambda]
  network_patterns: [vpn, private_link, nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
observability:
  logs: json_structured
  metrics: standard_connector_metrics
  tracing: opentelemetry
compliance:
  sensitive_data: pii
  security_controls: secrets_manager
```

## Throttling and Retries
Follow vendor rate limits when documented. 
If limits are not documented start with a conservative default such as 5 requests per second per stream and adjust after measurement. 
Use exponential backoff with jitter. 
Retries must be idempotent and safe for at least once delivery.

## Error Handling
Classify errors into retryable and terminal categories.
- Retryable: 429 Too Many Requests, 5xx responses, transient network errors
- Terminal: authentication failure, permission denied, invalid query, missing service
Surface terminal errors with clear messages that identify the failing entity set and request parameters without exposing credentials.

## Schema Handling
Emit source schemas during discovery. 
The platform stores schemas in the schema registry and compares versions before promotion. 
Do not embed large schemas in the manifest. 
On drift detect, raise a compatibility alert and continue landing to Bronze.

## Observability
Logs must include connector id, tenant id, run id, entity set, request id, and status. 
Metrics must include records read, records emitted, bytes processed, request latency, error counts, and retries. 
Tracing must correlate orchestrator tasks with connector calls using a shared trace id.

## Testing
Unit tests must cover authentication flows, discovery parsing, pagination, and incremental cursors. 
Integration tests must run against a sandbox service and validate one full refresh and one incremental cycle. 
Certification requires successful runs in each declared runner and at least one declared network pattern.

## Limits and Considerations
- Large entity sets may require partitioning by date to keep run times reasonable
- Some OData services restrict filter operators on date time fields
- Metadata may not expose primary keys for all sets and may require configuration
- Avoid large $expand queries that increase response size without benefit

## Relationships
Integrates with state registry for cursor checkpoints, schema registry for schema versions, catalog for capability surfacing, and policy registry for PII tagging and residency constraints.

## Exclusions
This document does not include business mappings, GDP or KPI definitions, or tenant onboarding procedures.
