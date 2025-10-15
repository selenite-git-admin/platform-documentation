# Dataset Refresh Registry (DRR) Observability

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Objectives
Observability verifies that DRR meets its availability and freshness propagation targets and that tenant isolation is intact. This document defines signals, dashboards, alerts, and standard queries for on call and product teams.

## Service Level Indicators
| SLI | Definition | Target |
|-----|------------|--------|
| Read latency P99 | Server side latency for GET endpoints | ≤ 100 ms |
| Read availability | Successful reads divided by total reads | 99.99 percent |
| Write propagation lag | Time from Runtime completion to visible DRR state | ≤ 10 s p95 |
| Event delay | Time from state change to event publication | ≤ 1 s p95 |
| RLS correctness | Percent of sampled requests that pass row level checks | 100 percent |

## Golden Signals
| Signal | Metric name | Unit | Dimension keys |
|--------|-------------|------|----------------|
| Latency | drr.read.latency | ms | endpoint, status_code, region |
| Traffic | drr.read.rps | rps | endpoint, region |
| Errors | drr.read.error_rate | ratio | code, endpoint, region |
| Saturation | drr.db.pool.utilization | ratio | role, region |
| Propagation | drr.state.update.lag | s | dataset_id, tenant_id, region |

## Metrics
### API
- `drr.read.latency` histogram
- `drr.read.error_rate` counter by `code in {invalid_request, forbidden, not_found, stale_update, internal_error}`
- `drr.read.bytes_out` counter
- `drr.cache.hit_ratio` gauge for ETag and CDN validation
- `drr.rlq.depth` queue depth for async tasks if events are enabled

### Writer
- `drr.writer.requests` counter
- `drr.writer.conflict.count` counter for stale updates and idempotency conflicts
- `drr.state.update.lag` histogram from Runtime finish time to DRR visibility
- `drr.writer.reject.count` counter for auth and policy denies

### Database
- `drr.db.pool.utilization` gauge
- `drr.db.qps` gauge by statement class
- `drr.db.replication.lag` seconds
- `drr.db.deadlock.count` counter

## Logs
Structured JSON logs with the following fields
- `ts`, `level`, `message`
- `correlation_id`, `request_id`
- `dataset_id`, `tenant_id`, `runtime_run_id`
- `endpoint`, `status_code`, `latency_ms`
- `writer_event` for internal writes
- `rls_evaluated` and `rls_result`

Sensitive values are not logged. Use sampling for success logs and full capture for errors.

## Traces
Every request opens a root span named `drr.api` with tags
- `endpoint`, `dataset_id`, `tenant_id`
- `cache_status` in {hit, miss, validated}
- `db.query.count`, `db.total_ms`
Internal writes include a child span `drr.writer.update` and link to the Runtime span via `runtime_run_id`.

## Dashboards
### Operations Overview
- Read latency P50, P95, P99 by endpoint
- Error rate by code
- Propagation lag p50 and p95
- Database saturation and replication lag

### Tenant View
- Top tenants by read volume
- Freshness distribution by status for a tenant
- Unknown status counts over time

### Writer Health
- Writer conflicts
- Stale update rejects
- State update lag distribution

## Alerts
| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Read latency high | P99 > 100 ms for 5 min | High | Investigate DB saturation and cache misses |
| Read availability drop | Availability < 99.9 percent for 10 min | High | Fail traffic to secondary region if enabled |
| Propagation lag high | p95 update lag > 10 s for 10 min | High | Page Runtime on call and check event backlog |
| Error spike | error_rate > 1 percent for 5 min | Medium | Inspect recent deploys and logs |
| RLS anomaly | any cross tenant read detected | Critical | Freeze listing endpoint and rotate tokens |

## Standard Queries
PromQL style sketches

- Read latency p99
```
histogram_quantile(0.99, sum(rate(drr_read_latency_bucket[5m])) by (le, endpoint))
```
- Read availability
```
sum(rate(drr_read_success_total[5m])) / sum(rate(drr_read_total[5m]))
```
- Propagation lag p95
```
histogram_quantile(0.95, sum(rate(drr_state_update_lag_bucket[5m])) by (le))
```
- Top endpoints by error rate
```
topk(5, sum(rate(drr_read_errors_total[5m])) by (endpoint))
```

## Sampling and Retention
- Request logs sampled at 1 percent, errors at 100 percent, writer updates at 100 percent
- Metrics retained at high resolution for 14 days and downsampled for 13 months
- Traces sampled at 0.1 percent baseline with dynamic upsampling on errors

## Runbook References
- RB DRR 001 propagation lag
- RB DRR 002 writer conflict
- RB DRR 003 RLS anomaly

## Ownership and Escalation
- Primary owner is Platform Foundation
- Secondary owner is Data Platform SRE
- Pager label drr service