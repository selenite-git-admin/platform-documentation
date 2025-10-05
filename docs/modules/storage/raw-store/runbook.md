# Raw Store – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Ingest backlog | Queue depth, worker health | Scale consumers; increase partitions | Backlog drains |
| Query timeouts | Hot partitions, skew | Repartition or add indexes | P99 ↓ |
| Storage pressure | Utilization %, growth rate | Expand tier; purge per policy | Utilization stable |

## Procedures
### Recover from ingest backlog
1. Scale consumers
2. Increase partitions
3. Throttle low-priority sources

### Checksum mismatch
1. Quarantine object
2. Re-fetch from source
3. Re-register after fix

## Safety Notes
- Do not bypass retention policies; use approved purge jobs.
