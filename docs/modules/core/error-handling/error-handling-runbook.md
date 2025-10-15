# Error Handling Runbook

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Operational playbooks for handling error spikes with the platform’s canonical error model. This runbook is action‑oriented: detect, triage, mitigate, verify, and close. It applies to API Gateway + Lambda services, containerized services, and batch jobs.

## Incident Classification
| Severity | Symptoms | Examples |
|---------|----------|----------|
| **P1** | Widespread `error.rate` > 1% across multiple services; customer impact is broad | `dependency_unavailable` spike region‑wide; elevated p99 and 5xx |
| **P2** | Single service or endpoint degraded; limited blast radius | `serialization_failure` spike on a hot write route |
| **P3** | Client misuse or configuration issues | `rate_limited` spikes from a few tokens; repeated validation failures |

## Common Signals to Check
- Dashboard: service “Errors” → `error.rate`, `error.by_code`, p99
- Logs: filter by `code` and `correlation_id`
- Traces: look for dependency spans with elevated error tags
- DRR: any freshness incidents coinciding with spikes
- Releases: deployment markers around onset time

## P1 – Platform Fault (Wide Impact)
### Triage
1. Confirm breadth: 3+ services impacted, multiple endpoints.  
2. Identify dominant codes: `dependency_unavailable`, `timeout`, `internal_error`.  
3. Check shared dependencies: DB, cache, messaging, identity.

### Mitigation
- **Traffic management**
  - Enable API cache on safe GET routes.
  - Temporarily reduce concurrency for failing writes; favor reads.
- **Capacity and cold starts**
  - Increase provisioned concurrency for affected Lambdas.
  - Scale out replicas or raise DB max connections if saturation is evident.
- **Dependency remediation**
  - Failing DB: promote replica, reduce aggressive queries, enable read‑only mode for non‑critical writes.
  - Identity failures: switch to cached JWKs if JWKS fetch is failing.

### Verification
- `error.rate` falls below 1% for 15 minutes.
- p99 within SLO.
- No new `dependency_unavailable` alerts.

### Closure
- Capture 3–5 representative `correlation_id`s for postmortem.
- Tag Evidence Ledger entries with the incident id.

## P2 – Endpoint/Service Degradation
### Triage
- Narrow to a route: e.g., `POST /catalog/migrate` showing `serialization_failure` or `conflict` growth.
- Review DDL changes, index stats, and query plans.
- Check workload change: batch size, retry storms.

### Mitigation
- Reduce batch size; enable exponential backoff with jitter.
- Add or adjust indexes; analyze + reindex if needed.
- For `serialization_failure`: lower contention by:
  - Sorting updates by key
  - Narrowing transaction scope
  - Using advisory locks for hot keys

### Verification
- Error counts return to baseline.
- Retry success > 95% for retryable codes.
- Throughput meets target QPS.

## P3 – Client Misuse or Config Issues
### Triage
- `rate_limited` spikes with steady traffic → abusive clients.
- `validation_failed` top offender → SDK drift or contract mismatch.

### Mitigation
- Adjust per‑client limits; contact owner with examples.
- Improve validation messages and documentation.
- Add schema lint to CI for SDKs if contract drift is frequent.

### Verification
- Error rate normalized for the tenant cohort.
- No follow‑up alerts within 24 hours.

## Code‑Specific Playbooks
### `dependency_unavailable` / `timeout`
- Confirm which downstream is failing.
- Circuit break calls if failure rate > 50% over 1 minute.
- Backoff retries; consider fallback content for read endpoints.
- Engage the owning team of the dependency.

### `serialization_failure`
- Switch the job to smaller batches.
- Increase retry attempts to 3 with jitter.
- Reduce lock contention using deterministic key order.

### `stale_read` (412)
- Validate ETag usage in the client or orchestration.
- Promote read‑modify‑write to a two‑step: `GET` → validate → `PATCH` with If‑Match.

### `rate_limited` (429)
- Inspect tenant token(s); compare to request caps.
- Offer higher limits only after verifying behavior.
- Confirm `Retry-After` logic in clients.

### `internal_error` (500)
- Inspect last deployment; flip Lambda alias back if errors started post‑deploy.
- Grep logs for stack signature; apply hotfix or toggles as needed.

## Forensics Workflow
1. **Pick a spike window** from the dashboard (e.g., 10 minutes).  
2. **Top offenders**: `error.by_code` and `endpoint`.  
3. **Sample correlation ids** from logs; pivot to traces.  
4. **Drill** into dependency spans and DB locks.  
5. **Tie** to DRR incidents and Evidence Ledger entries using `correlation_id`.

## CLI Snippets (SQL/Queries)
### Find top error codes in last hour
```sql
select code, count(*) as c
from error_event
where ts > now() - interval '1 hour'
group by code order by c desc;
```

### Find tenants most affected by rate limiting
```sql
select tenant_hash, count(*) as c
from error_event
where code = 'rate_limited' and ts > now() - interval '1 day'
group by tenant_hash order by c desc limit 20;
```

### Sample correlation ids for a service
```sql
select correlation_id, count(*) as c
from error_event
where service = 'catalog' and ts > now() - interval '30 minutes'
group by correlation_id order by c desc limit 10;
```

## Rollback and Feature Flags
- Lambda: revert alias to previous version; confirm with synthetic checks.
- Containers: roll back to last healthy image; drain and restart pods.
- Toggle risky features off via Config & Flags; document default states and blast radius.

## Communication
- Post status in #oncall and #incident channels with: severity, impacted areas, codes, time window, mitigations, ETA for next update.
- Notify Governance if GDPR/PII implications are suspected (even though errors avoid PII by design).

## Post‑Incident
- Timeline: onset, detection, mitigation, verification.
- Root cause and contributing factors.
- Action items: rate limits, index changes, client guidance.
- Update this runbook with new heuristics and queries.

## Appendix – Decision Trees
### Is it Platform or Client?
- If `invalid_request`/`validation_failed` dominate → client.
- If `dependency_unavailable`/`timeout` dominate → platform or downstream.
- If `serialization_failure` spikes → data contention.

### Do We Retry?
- Retry if code is in retryable set; otherwise fix payload or access.
- Check `Retry-After`; throttle SDKs that ignore it.

## Summary
These playbooks convert error signals into immediate, repeatable operator actions. Follow the decision flow, fix the hot path first, and always verify via correlation ids, DRR overlays, and post‑deploy synthetic checks.