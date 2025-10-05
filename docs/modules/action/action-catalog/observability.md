# Action Catalog – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| template_publish_total | counter | count | tenant,kind | Published templates |
| template_validation_failures_total | counter | count | reason | Validation errors |

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
