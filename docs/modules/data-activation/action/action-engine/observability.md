# Action Engine – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| rule_evals_total | counter | count | tenant,rule | Throughput |
| jobs_created_total | counter | count | tenant,template | Job creation |
| eval_latency_seconds | histogram | seconds | tenant | Latency |

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
