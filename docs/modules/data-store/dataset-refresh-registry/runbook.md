# Dataset Refresh Registry (DRR) Runbook

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Purpose
The DRR runbook provides operational guidance for responding to common alerts and service degradations. It is written for on-call engineers and SRE teams supporting DRR and its upstream Runtime.

## Key Components
- DRR service (API and writer)
- PostgreSQL database (multi-region replicated)
- Runtime event source (job completion queue)
- Evidence Ledger integration
- Metrics and alerting through Prometheus and Grafana

## Common Scenarios

### 1. Propagation Lag High
**Alert ID:** RB-DRR-001  
**Condition:** p95 update lag > 10 s for 10 min  
**Impact:** Dashboards may show stale data though jobs succeeded in Runtime.

**Checklist**
1. Check the lag metric:
   ```bash
   kubectl exec -it drr-api -- curl http://localhost:9090/api/v1/query?query=drr_state_update_lag_p95
   ```
2. Verify if Runtime events are delayed:
   - Query `runtime_event_queue_depth` in Prometheus.
   - Inspect Kafka or SQS consumer lag.
3. Inspect writer pod logs for `stale_update` or `timeout` messages.
4. If DB replication lag > 2s, throttle writes and notify DB operations.
5. If Runtime backlog exists, coordinate with Runtime on call to flush queue.

**Temporary Mitigation**
- Enable stale-read fallback for UI consumers (read from last persisted state).
- Reduce alert noise by silencing DRR for 30 minutes while Runtime recovers.

**Postmortem Requirements**
- Capture duration of lag, affected tenants, and root cause in Evidence Ledger.
- Tag incident with `propagation-lag`.

---

### 2. Writer Conflict or Stale Update
**Alert ID:** RB-DRR-002  
**Condition:** Conflict rate > 0.1 percent over 10 min window  
**Impact:** Some dataset states may not reflect latest completion run.

**Checklist**
1. Review DRR writer logs for `stale_update` errors.
2. Confirm system time skew between Runtime and DRR nodes < 1s.
3. Verify Idempotency-Key reuse via recent requests in API logs.
4. Confirm `runtime_run_id` is unique across retried jobs.
5. Check if Runtime resubmitted an old job completion.

**Temporary Mitigation**
- Allow retry with force update flag only for internal service account.  
- Validate correct ordering through `updated_at` timestamp.

**Postmortem Requirements**
- Record dataset_ids with rejected updates.  
- Open issue with Runtime for event duplication.

---

### 3. RLS (Row-Level Security) Violation
**Alert ID:** RB-DRR-003  
**Condition:** cross-tenant read detected  
**Impact:** Tenant data isolation breach risk.

**Checklist**
1. Immediately revoke affected API token or service key.  
2. Check audit logs for recent queries containing multiple tenant_ids.  
3. Execute:
   ```sql
   SELECT * FROM audit_log WHERE service='drr' AND event='cross_tenant_read' ORDER BY ts DESC LIMIT 50;
   ```
4. Verify RLS policies in PostgreSQL using:
   ```sql
   \d+ dataset_refresh_state
   ```
5. If misconfiguration found, apply policy patch from GitOps repository.

**Temporary Mitigation**
- Disable `/datasets` list endpoint via feature flag.  
- Restrict DRR read access to trusted internal roles.

**Postmortem Requirements**
- Notify Security and Platform leads.  
- Add incident entry with correlation ID to Evidence Ledger.  
- Run targeted data access audit for affected tenants.

---

### 4. Read Latency High
**Alert ID:** RB-DRR-004  
**Condition:** P99 > 100 ms for 5 min  
**Impact:** API degradation; dashboards may timeout.

**Checklist**
1. Inspect `drr_read_latency_p99` metric across regions.  
2. Check PostgreSQL CPU and active connections.  
3. Confirm cache hit ratio via `drr.cache.hit_ratio` < 0.9 triggers warm-up.  
4. Review slow query logs for large table scans on `dataset_run_log`.

**Mitigation**
- Scale read replicas horizontally.  
- Evict cold cache entries.  
- If DB IO high, move run log queries to replica.

**Postmortem Requirements**
- Capture query plans and add summary to internal wiki.

---

### 5. Error Spike or Availability Drop
**Alert ID:** RB-DRR-005  
**Condition:** error_rate > 1% or availability < 99.9%  
**Impact:** Service partial outage.

**Checklist**
1. Identify failing endpoints using error distribution dashboard.  
2. Inspect app logs for top error codes.  
3. Check dependency health: DB connection, Evidence Ledger, Runtime webhook.  
4. If 5xx responses cluster around `/refresh-state`, investigate DB lock contention.  
5. Validate ingress and network routing (look for 502/504).

**Mitigation**
- Restart affected pods.  
- Reroute to secondary region if enabled.  
- Disable non-critical internal endpoints.

**Postmortem Requirements**
- Create incident report within 24 hours.  
- Attach logs and Grafana screenshots.

---

### 6. Database Replication Lag
**Alert ID:** RB-DRR-006  
**Condition:** replica lag > 5s for 10 min  
**Impact:** Cross-region consistency gap.

**Checklist**
1. Query DB replication metrics:
   ```sql
   SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(), pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn());
   ```
2. Confirm replication channel status.
3. If lag increasing, switch reader traffic to primary.

**Mitigation**
- Temporarily disable async replication.  
- Notify DB team to rebalance WAL sender slots.

**Postmortem Requirements**
- Record lag duration and dataset impact.

---

## Escalation and Ownership
| Role | Responsibility |
|------|----------------|
| Platform Foundation | Primary owner of DRR |
| Data Platform SRE | Secondary escalation |
| Security | Engaged for RLS or auth anomalies |
| Runtime Team | Engaged for event delay or duplication |

Escalate via PagerDuty service **“drr-service”** using playbook link `pd://service/drr`.

## Communication
- All incident communication in `#oncall-drr` channel.  
- Postmortem template stored in `/runbooks/templates/drr-postmortem.md`.

## Postmortem Classification
| Code | Category | Description |
|------|-----------|-------------|
| DRR-PL | Propagation lag | Delayed freshness updates |
| DRR-WC | Writer conflict | Stale or duplicate update |
| DRR-RLS | RLS violation | Cross-tenant access |
| DRR-LAT | Latency issue | Slow API performance |
| DRR-ERR | Error spike | Elevated error rate |
| DRR-DBL | Database lag | Replication or performance issue |