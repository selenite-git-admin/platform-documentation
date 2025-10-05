# Raw Store – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| ingest_bytes_total | counter | bytes | source | Ingest volume |
| ingest_failures_total | counter | count | reason | Failures |
| ingest_latency_seconds | histogram | seconds | op | Latency |

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
