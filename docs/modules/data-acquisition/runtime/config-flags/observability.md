# Config & Flags – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| flag_evaluations_total | counter | count | flag_key | Throughput |
| eval_latency_seconds | histogram | seconds | flag_key | Latency |
| killswitch_activations_total | counter | count | flag_key | Emergency usage |

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
