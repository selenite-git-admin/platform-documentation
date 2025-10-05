# Catalog – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| catalog_views_total | counter | count | resource | Usage |
| catalog_search_latency_seconds | histogram | seconds |  | Search perf |
| catalog_collections_total | counter | count | owner | Collections created |

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
