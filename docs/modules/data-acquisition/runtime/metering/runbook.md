# Metering – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Stuck DAG | Pending nodes, blocked dependencies | Unblock dependency; resume DAG | DAG completes |
| Worker starvation | Queue depth, CPU/mem | Scale nodes; preempt low priority | P95 run latency ↓ |
| DLQ growth | Poison messages | Quarantine and replay after fix | DLQ stable |

## Procedures
### Backfill counters
1. Pause ingestion for tenant
2. Run backfill job
3. Resume and verify drift

### High drift
1. Inspect enforcement evidence
2. Recompute window
3. Fix out‑of‑order events

## Safety Notes
- Respect idempotency and exactly‑once semantics where applicable.
