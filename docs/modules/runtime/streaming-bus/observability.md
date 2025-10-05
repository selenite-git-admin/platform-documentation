# Streaming Bus – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| produce_total | counter | count | topic | Throughput |
| consumer_lag | gauge | count | group | Backlog health |
| dlq_depth | gauge | count | topic | Poison backlog |

## Logs
Structured JSON with correlation IDs.

## Traces
- Root span per operation; spans for queueing, scheduling, execution, and I/O.

## Dashboards
- Queue depth, run latency, success ratio, resource utilization, DLQ size.

## Alerts
- Stuck DAGs, run latency breach, worker exhaustion, DLQ growth.

## SLOs
- Availability ≥ 99.9% (30 days).
- P95 orchestration latency ≤ target.
