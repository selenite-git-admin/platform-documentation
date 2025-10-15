# GDP Calendar – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| runs_total | counter | count | dataset,status | Run throughput |
| run_latency_seconds | histogram | seconds | dataset | Duration |
| schedule_misses_total | counter | count | dataset | Missed windows |

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
