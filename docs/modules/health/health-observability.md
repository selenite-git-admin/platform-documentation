# Health Observability

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Give operators full visibility into service liveness, readiness, and data freshness. Health observability covers metrics, logs, traces, dashboards, and alert policies that validate signals from `/healthz`, `/readyz`, `/startupz`, `/metrics`, and `/dataz` across all services.

## Design principles
- End to end correlation using `X-Correlation-Id` across probes, logs, and traces
- Low overhead checks with clear outcomes and short hints
- Consistent labels across services for easy rollups
- Separation of service health and data health so failures are diagnosable

## Metrics
All services emit health metrics to the platform collector. Prefer Prometheus style naming. Default labels: `service_name`, `environment`, `region`.

| Metric | Type | Description |
|---|---|---|
| `health_ready_check_total` | counter | Count of readiness checks |
| `health_ready_fail_total` | counter | Count of failed readiness checks |
| `health_ready_latency_ms` | histogram | Readiness latency distribution |
| `health_startup_gate_open` | gauge | 1 when startup has completed |
| `health_liveness_ok` | gauge | 1 when liveness responding |
| `health_data_fresh_ok_total` | counter | Data freshness checks passing |
| `health_data_fresh_late_total` | counter | Data checks late |
| `health_data_fresh_missing_total` | counter | Missing core dataset |
| `health_dependency_status` | gauge | 1 ok, 0 degraded, -1 fail per dependency label |
| `health_aggregator_services_ok` | gauge | Number of services ready in fleet rollup |

Example PromQL
```promql
# Readiness error rate (5m)
rate(health_ready_fail_total[5m]) / rate(health_ready_check_total[5m])

# P95 readiness latency by service
histogram_quantile(0.95, sum(rate(health_ready_latency_ms_bucket[5m])) by (le, service_name))

# Data late rate by environment
sum(rate(health_data_fresh_late_total[15m])) by (environment)
```

SLO guardrails
- Readiness success ratio ≥ 99.9 percent monthly
- P95 readiness latency ≤ 50 ms
- Data late rate ≤ 1 percent of expected intervals per week

## Logging
Health probes and outcomes are logged as structured JSON. Logs are short and safe for exposure in shared viewers.

Common fields
| Field | Example | Notes |
|---|---|---|
| `timestamp` | 2025-10-13T08:30:00Z | UTC |
| `level` | info | severity |
| `service` | notifications | logical service name |
| `probe` | readyz | liveness, readyz, startupz, dataz |
| `check` | db | dependency name or dataset |
| `status` | ok | ok, degraded, fail, late, missing, invalid |
| `latency_ms` | 14 | for readiness checks |
| `hint` | pool warm | short human hint |
| `correlation_id` | 01JC2Q0... | trace key |

Sampling
- Log readiness outcomes at info at most once per minute per service
- Always log failures and transitions

Routing
- Logs go to the central sink with 30 day retention
- Sensitive diagnostic details remain in traces and are not logged

## Tracing
Health operations create short traces to capture dependency calls and timing. Use OpenTelemetry.

Span model
- Root `health.readyz` for readiness checks
- Child spans per dependency `health.dep.db`, `health.dep.secrets`, `health.dep.queue`
- Root `health.dataz` for data freshness with child `drr.lookup` and `schema.validate`

Trace attributes
| Key | Example |
|---|---|
| `service_name` | notifications |
| `environment` | prod |
| `region` | ap-south-1 |
| `probe` | readyz |
| `status` | ok |
| `dependency` | db |
| `latency_ms` | 12 |

Sampling
- Always sample failures
- Sample 5 percent of successful checks per service

## Dashboards
Overview
- Uptime and readiness success ratio per service and region
- Readiness latency p95 and p99
- Top failing dependencies
- Data freshness status by dataset and service
- Fleet rollup with service counts ok, degraded, failing

Data health
- Late and missing counts over time
- Freshness lag histogram
- Core dataset card with last as_of and lag

Fleet view
- Grid of services with current readiness
- Drill down to per service dependency detail

## Alerts
Alert policies align with SLOs and default thresholds.

| Alert | Condition | Suggested threshold | Action |
|---|---|---|---|
| Readiness failing | ratio of `ready_fail` over `ready_check` > 0.1 percent for 5 minutes | P1 for core services | Page on call |
| Slow readiness | p95 readiness latency > 200 ms for 10 minutes | P2 | Investigate dependency saturation |
| Data late core | `data_fresh_late_total` increases for core dataset beyond interval budget | P1 | Trigger owner runbook |
| Data missing | `data_fresh_missing_total` increases | P1 | Investigate ingestion failure |
| Fleet partial | less than 90 percent of services ready | P2 | Check deploy or network |
| Startup stuck | `startup_gate_open` remains 0 for more than 10 minutes after deploy | P2 | Roll back or fix init |

Notification channels
- Page on call via email and Slack using the Notifications module
- Annotate alerts with runbook links

## Synthetic checks
External
- Ping public endpoints and validate headers and HTML markers
- Simulate user flows with a short read only journey

Internal
- Authenticated call to a key API returning a known token record
- Validate latency and status

Data
- Load a fixed small record into a sandbox dataset and verify round trip read in minutes

## Example queries
Recent readiness failures
```sql
select service_name, check_name, status, hint, ts
from health_check_log
where status = 'fail' and ts > now() - interval '1 hour'
order by ts desc;
```

Datasets late over the last day
```sql
select dataset_name, count(*) as late_count
from data_health_log
where status = 'late' and ts > now() - interval '24 hours'
group by dataset_name
order by late_count desc;
```

Service uptime estimation
```promql
sum_over_time(health_ready_check_total{service_name="api"}[30d]) 
- sum_over_time(health_ready_fail_total{service_name="api"}[30d])
```

## Retention
- Metrics hot for 30 days and cold for 6 months
- Logs retained for 30 days with failure extracts archived
- Traces sampled for 7 days with failure traces 30 days
- Data health logs retained for 30 to 90 days

## Testing checklist
- Readiness check includes only critical dependencies
- Cache headers are correct on all endpoints
- Failures propagate correlation id into logs and traces
- Synthetic checks fail when a core dependency is intentionally broken
- Dashboards display data for new services within one hour

## Summary
Health observability creates a tight feedback loop from probes to dashboards. Clear metrics, concise logs, and focused traces make failures obvious and recovery fast, while fleet and data views show the real state of the platform without revealing sensitive information.