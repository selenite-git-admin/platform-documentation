# Metering – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| deltas_ingested_total | counter | count | feature | Throughput |
| aggregation_latency_seconds | histogram | seconds | feature | Pipeline time |
| drift_ratio | gauge | ratio | tenant,feature | Mismatch vs enforcement |

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
