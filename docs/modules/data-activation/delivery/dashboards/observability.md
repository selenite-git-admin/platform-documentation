# Dashboards – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| renders_total | counter | count | dashboard | Throughput |
| render_latency_seconds | histogram | seconds | dashboard | Latency |
| share_links_active | gauge | count | dashboard | Link hygiene |

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
