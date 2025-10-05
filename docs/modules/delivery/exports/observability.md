# Exports – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| exports_total | counter | count | dataset | Throughput |
| export_latency_seconds | histogram | seconds | target | Duration |
| export_failures_total | counter | count | reason | Failures |

## Logs
Structured JSON with correlation IDs (`x-request-id`).

## Traces
- Root span per call; spans for cache, query, transform, and delivery.

## Dashboards
- Throughput, latency, cache hit ratio, error rates.

## Alerts
- Spike in 5xx, cache collapse, unusual query load.

## SLOs
- Availability ≥ 99.9% (30 days).
- P95 latency ≤ agreed target.
