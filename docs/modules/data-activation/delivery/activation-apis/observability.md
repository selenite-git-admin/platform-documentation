# Activation APIs – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| queries_total | counter | count | resource | Throughput |
| query_latency_seconds | histogram | seconds | resource | Latency |
| cache_hit_ratio | gauge | ratio | resource | Cache efficiency |

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
