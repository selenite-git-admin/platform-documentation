# Published Store – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Ingest backlog | Queue depth, worker health | Scale consumers; increase partitions | Backlog drains |
| Query timeouts | Hot partitions, skew | Repartition or add indexes | P99 ↓ |
| Storage pressure | Utilization %, growth rate | Expand tier; purge per policy | Utilization stable |

## Procedures
### Export stuck
1. Check DLQ
2. Retry with backoff
3. Validate target access

### Contract violation
1. Inspect schema diff
2. Bump contract or fix break
3. Rebuild snapshot

## Safety Notes
- Do not bypass retention policies; use approved purge jobs.
