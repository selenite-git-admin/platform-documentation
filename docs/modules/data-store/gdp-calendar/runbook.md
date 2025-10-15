# GDP Calendar – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Ingest backlog | Queue depth, worker health | Scale consumers; increase partitions | Backlog drains |
| Query timeouts | Hot partitions, skew | Repartition or add indexes | P99 ↓ |
| Storage pressure | Utilization %, growth rate | Expand tier; purge per policy | Utilization stable |

## Procedures
### Missed schedule
1. Inspect scheduler logs
2. Reschedule run
3. Notify subscribers

### Failed run
1. Review job logs
2. Re-run with backoff
3. Update status

## Safety Notes
- Do not bypass retention policies; use approved purge jobs.
