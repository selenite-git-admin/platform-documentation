# Orchestrator – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| runs_total | counter | count | dag,state | Run throughput |
| run_latency_seconds | histogram | seconds | dag | End‑to‑end time |
| sla_breaches_total | counter | count | dag | SLA failures |

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
