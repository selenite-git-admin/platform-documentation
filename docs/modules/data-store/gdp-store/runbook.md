# GDP Store – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Ingest backlog | Queue depth, worker health | Scale consumers; increase partitions | Backlog drains |
| Query timeouts | Hot partitions, skew | Repartition or add indexes | P99 ↓ |
| Storage pressure | Utilization %, growth rate | Expand tier; purge per policy | Utilization stable |

## Procedures
### Failed build
1. Inspect DQ report
2. Fix transform or input
3. Re-run version build

### Rollback publish
1. Promote previous version
2. Invalidate caches
3. Notify consumers

## Safety Notes
- Do not bypass retention policies; use approved purge jobs.
