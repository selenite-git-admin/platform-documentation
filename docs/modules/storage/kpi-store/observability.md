# KPI Store – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| kpi_queries_total | counter | count | kpi | Query throughput |
| kpi_query_latency_seconds | histogram | seconds | kpi | Latency |
| kpi_cache_hit_ratio | gauge | ratio | kpi | Cache efficiency |

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
