# GDP Store – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| versions_published_total | counter | count | dataset | Publish throughput |
| dq_failures_total | counter | count | rule | Quality failures |
| transform_latency_seconds | histogram | seconds | dataset | Build latency |

## Logs
Structured JSON with correlation IDs.

## Traces
- Root span per ingest/query; spans for storage IO and transform steps.

## Dashboards
- Ingest throughput, storage growth, query latency/error budget.

## Alerts
- Backlog growth, failed ingests, query timeouts, storage pressure.

## SLOs
- Availability ≥ 99.9% (30 days).
- P99 read/write latency per store within target.
