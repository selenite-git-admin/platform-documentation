# Compute Fabric – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| jobs_total | counter | count | state,tenant | Job throughput |
| job_latency_seconds | histogram | seconds | tenant | Queue→finish time |
| pool_utilization_ratio | gauge | ratio | pool | Capacity usage |

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
