# Subscription Enforcement – Runbook

## Scope
Operational procedures for routine tasks and incident response for Subscription Enforcement. 【121†source】

## Quick reference table
| Symptom | First checks | Safe mitigations | Validation |
|---|---|---|---|
| Spike in denies | Verify plan cache freshness; compare with change log | Trigger safe plan cache refresh; enable grace policy temporarily | Deny rate returns to baseline |
| Latency above SLO | Inspect cache hit ratio; check dependency health | Scale evaluator pods; reduce trace sampling | P99 ≤ 50ms |
| Drift > 0.5% | Compare counters vs Metering aggregates | Run reconciliation job; replay missing deltas idempotently | Drift ≤ 0.5% |
| Frequent throttling | Review tenant usage pattern | Increase soft limit via time‑boxed override | Throttle rate drops without breaches |

## Procedures 【121†source】

### Refresh plan cache
**Preconditions:** Plan registry stable; no ongoing migrations.  
1. Call `POST /internal/plan/refresh` (admin only).  
2. Check `plan_refresh_total` and logs for success.  
3. Validate random tenant via `GET /plan`.  
**Validation:** Cache hit ratio ≥ 0.9 within 5 minutes.

### Rebuild usage counters
**Preconditions:** Incident ID created; maintenance window approved.  
1. Pause evaluators for affected tenants.  
2. Launch backfill with time range and idempotency key.  
3. Compare aggregates with Metering after completion.  
**Validation:** Drift ratio ≤ 0.5% for the last hour.

### Audit evidence chain
**Preconditions:** Evidence Ledger reachable.  
1. List recent `evidence_id` values from logs.  
2. Run verification tool to check hash chain continuity.  
3. Export report to audit bucket.  
**Validation:** 0 verification failures.

## Routine tasks 【121†source】
- Review top throttled tenants weekly.  
- Validate rate limits configuration weekly.  
- Rotate API credentials quarterly.  
- Exercise disaster recovery playbook biannually.

## Safety notes 【121†source】
- Do not modify plan registry data manually. Use approved workflows.  
- Rebuild counters only during an approved window.  
- Never disable evidence writes during production traffic.

## References 【121†source】
- [API](api.md)  
- [Data Model](data-model.md)  
- [Observability](observability.md)  
- [Security](security.md)
