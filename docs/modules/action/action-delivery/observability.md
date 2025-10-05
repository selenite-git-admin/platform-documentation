# Action Delivery – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| deliveries_total | counter | count | tenant,endpoint | Throughput |
| delivery_latency_seconds | histogram | seconds | endpoint | Latency |
| dlq_depth | gauge | count | tenant | Backlog health |

## Logs
Structured JSON with correlation IDs.

## Traces
- Root span per action; spans for rule eval, template render, delivery.

## Dashboards
- Throughput, success ratio, DLQ depth, and latency percentiles.

## Alerts
- Rule eval backlog, delivery retries exceeding budget, DLQ growth.

## SLOs
- Availability ≥ 99.9% (30 days).
- P99 latency per operation ≤ target.
