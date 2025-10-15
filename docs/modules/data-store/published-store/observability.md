# Published Store – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| snapshots_created_total | counter | count | dataset | Snapshot throughput |
| exports_total | counter | count | target | Export throughput |
| export_latency_seconds | histogram | seconds | target | Delivery latency |

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
