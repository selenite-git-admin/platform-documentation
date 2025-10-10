# Subscription Enforcement – Observability

## Scope
Defines metrics, logs, traces, dashboards, alerts, SLOs, and retention for the module.

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| enforcement_decisions_total | counter | count | decision, tenant, feature | Track decision outcomes |
| enforcement_latency_seconds | histogram | seconds | tenant, feature | Evaluate decision latency |
| enforcement_cache_hit_ratio | gauge | ratio | tenant | Measure plan/entitlement cache efficacy |
| quota_drift_ratio | gauge | ratio | tenant | Detect usage vs metering mismatch |
| plan_refresh_total | counter | count | result | Count plan cache refresh operations |

### Metric Notes
- Latency buckets: `0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5` seconds.  
- Drift ratio target is `< 0.5%` rolling over 1 hour.

## Logs
Structured JSON lines with correlation identifiers.
- `decision_event`: `{tenant_id, feature, decision, reason, quota, evidence_id}`  
- `plan_refresh`: `{tenant_id?, plan_id, version, result}`  
- `throttle_trigger`: `{tenant_id, feature, window, retry_after_ms}`

## Traces
Spans and attributes
- `EvaluateAction` (root): `tenant_id`, `feature`, `request_hash`  
- `CacheLookup`: `hit`, `doc_version`  
- `UsageSnapshot`: `window`, `used_units`  
- `DecisionEmit`: `evidence_id`

Trace sampling 10% default; 100% on error paths.

## Dashboards
- **Decision Overview**: stacked outcomes by tenant and feature.  
- **Latency**: P50/P95/P99 with alerts.  
- **Drift**: per‑tenant drift and top offenders.  
- **Cache**: hit ratio and refresh rate.

## Alerts
| Alert | Condition | Severity | Action |
|------|-----------|----------|--------|
| High Deny Rate | `denied / total > 0.02` for 10m | High | Validate plan and overrides |
| High Latency | P99 > 50ms for 10m | High | Scale evaluators; check cache |
| Drift Exceeds | drift_ratio > 0.005 for 1h | Medium | Reconcile counters |
| Cache Miss Surge | hit_ratio < 0.8 for 10m | Medium | Warm cache; review TTL |

## SLOs
| Metric | Objective | Window |
|--------|-----------|--------|
| Availability | ≥ 99.9% | 30 days |
| Decision latency P99 | ≤ 50ms | 30 days |
| Evidence write success | ≥ 99.99% | 30 days |

## Retention
- Metrics: 90 days.  
- Logs: 30 days.  
- Traces: 7 days (error paths 30 days).

