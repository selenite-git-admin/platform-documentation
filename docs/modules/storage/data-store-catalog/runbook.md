# Data Store Catalog (Catalog) Runbook

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
This runbook defines standard operating procedures for the Data Store Catalog service. It describes how to identify, mitigate, and recover from incidents affecting dataset discovery, metadata consistency, or API availability. Catalog is a read-heavy service; the most common issues involve synchronization drift, API latency, or stale metadata.

## Incident Taxonomy
| Severity | Definition | Typical Impact |
|-----------|-------------|----------------|
| **P1 – Critical** | Service unavailable or metadata corruption detected | Platform-wide dataset discovery blocked |
| **P2 – Major** | Partial unavailability or API latency SLO violated | Users experience delayed responses or outdated listings |
| **P3 – Minor** | Non-blocking errors, drift or audit lag detected | No customer impact, internal remediation only |

## Quick Checks
1. Verify API health: `GET /storage/v1/catalog/health` returns 200.
2. Check database availability: `SELECT 1;` on primary PostgreSQL instance.
3. Confirm replication lag < 30 seconds (`pg_stat_replication`).
4. Check Grafana dashboards for `catalog.api.latency_p99` and `catalog.api.errors_5xx`.
5. Review recent alert notifications in PagerDuty.

## P1 – Service Outage or Metadata Corruption

### Symptoms
- API health endpoint returns 500 or timeout.
- Catalog datasets missing or unreadable.
- Evidence Ledger mismatch > 5% in reconciliation job.

### Mitigation
1. **Failover:** Route traffic to standby region if available.
2. **DB Health:** Check PostgreSQL cluster status (`pg_isready`, `aws rds describe-db-instances`).
3. **Rollback:** Restore from the latest RDS snapshot if corruption confirmed.
4. **Restart:** Redeploy Catalog API pods to clear connection exhaustion.
5. **Lock Writes:** Temporarily disable internal write APIs via feature flag to prevent further corruption.

### Verification
- Health endpoint returns 200.
- Random `GET /storage/v1/catalog/datasets/{id}` returns expected records.
- Audit entries consistent with Evidence Ledger.
- p99 latency < 100 ms for 15 minutes.

### Escalation
- Notify **Platform Foundation Lead**.
- Engage **DBA** for PostgreSQL recovery if RDS integrity is at risk.
- Record incident in postmortem tracker (`platform_incidents` table).

---

## P2 – Performance Degradation or API Latency Breach

### Symptoms
- `catalog.api.latency_p99` > 150 ms sustained for > 5 minutes.
- Elevated error_5xx > 1%.
- Cache hit ratio < 0.7.

### Mitigation
1. Check API pod CPU/memory in ECS or container orchestrator.
2. Verify RDS performance insights (slow queries, lock contention).
3. Increase API replicas temporarily.
4. Validate caching layer configuration (ETag, Redis TTL).
5. Tune slow query plans using `EXPLAIN ANALYZE`.

### Verification
- p99 latency restored below 100 ms.
- error_5xx < 0.5% for 15 minutes.
- Cache hit ratio > 0.85.

### Escalation
- Notify **SRE on-call** and **DevOps** if scaling or performance tuning required.
- Create `Performance` ticket tagged with affected region.

---

## P3 – Metadata Drift or Audit Lag

### Symptoms
- Drift detected between Catalog and DRR > 300 seconds.
- Missing audit entries in Evidence Ledger reconciliation.
- Stale data in read replicas.

### Mitigation
1. Trigger on-demand reconciliation job: `POST /storage-internal/v1/catalog/reconcile`.
2. Review drift summary: `SELECT * FROM catalog_drift_summary WHERE detected_at > now() - interval '1 hour';`
3. Rebuild stale replicas if lag > 60 seconds (`aws rds restart-db-instance`).
4. Inspect recent migrations for errors: `SELECT * FROM catalog_migration_audit WHERE status='failed';`
5. Force sync from primary Catalog if needed: `catalog_replay_audit.py --from-ledger`.

### Verification
- Drift < 60 seconds.
- All audit entries reconciled to Evidence Ledger.
- No failed migrations in last 30 minutes.

### Escalation
- Inform **Platform Governance** if audit gap > 1 hour.
- Root cause review at next ops sync.

---

## Scheduled Maintenance Procedures

### Weekly
- Review orphan_count metric.
- Validate 100% audit coverage.
- Reindex frequently queried columns (`analyze; vacuum analyze;`).
- Confirm cache warmup job executes hourly.

### Monthly
- Validate DRR-Catalog consistency report.
- Rotate API keys and internal tokens.
- Export reconciliation summary to S3.
- Refresh Grafana dashboards and alert thresholds.

### Quarterly
- Simulate disaster recovery by restoring from RDS snapshot to staging.
- Validate latency SLO under load test.
- Review schema compatibility entries for inactive datasets.

---

## Common Queries
| Purpose | Query |
|----------|-------|
| Find datasets without location | `SELECT dataset_id FROM catalog_dataset WHERE dataset_id NOT IN (SELECT dataset_id FROM catalog_location);` |
| Check schema version drift | `SELECT dataset_id, version FROM catalog_schema_version WHERE published_at < now() - interval '90 days';` |
| Identify failed migrations | `SELECT * FROM catalog_migration_audit WHERE status='failed' ORDER BY started_at DESC LIMIT 20;` |
| Verify replication lag | `SELECT * FROM pg_stat_replication;` |

---

## Recovery Validation Checklist
- [x] Health endpoints return 200.
- [x] Catalog API RPS restored to baseline.
- [x] p99 latency < 100 ms.
- [x] No orphaned datasets.
- [x] Audit entries reconciled.
- [x] Alerts cleared in PagerDuty.

---

## Postmortem Guidelines
Within 24 hours of incident closure:
1. Document root cause and contributing factors.
2. Record detection time, MTTA, and MTTD.
3. Update mitigation playbook if process gaps found.
4. Validate alert thresholds were appropriate.
5. Share summary in platform ops channel.

---

## Ownership
| Role | Responsibility |
|------|----------------|
| Platform Foundation | Primary owner of Catalog service and API reliability |
| DevOps | CI/CD pipelines, scaling, configuration, alerting |
| SRE | Monitoring, reconciliation jobs, drift detection |
| Governance | Audit validation, compliance sign-off |

## Summary
The Catalog runbook provides structured procedures to ensure metadata consistency and API availability across the PostgreSQL-based data platform. By following defined response tiers and reconciliation workflows, the platform maintains trust in dataset discovery and governance.