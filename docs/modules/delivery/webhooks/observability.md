# Webhooks – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| deliveries_total | counter | count | event | Throughput |
| delivery_latency_seconds | histogram | seconds | endpoint | Latency |
| dlq_depth | gauge | count | endpoint | Backlog |

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
