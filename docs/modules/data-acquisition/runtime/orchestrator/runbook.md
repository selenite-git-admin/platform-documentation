# Orchestrator – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Stuck DAG | Pending nodes, blocked dependencies | Unblock dependency; resume DAG | DAG completes |
| Worker starvation | Queue depth, CPU/mem | Scale nodes; preempt low priority | P95 run latency ↓ |
| DLQ growth | Poison messages | Quarantine and replay after fix | DLQ stable |

## Procedures
### Clear stuck run
1. Pause DAG
2. Mark task for retry with checkpoint
3. Resume DAG

### Mass backfill
1. Increase parallelism
2. Raise quotas temporarily
3. Revert after catch‑up

## Safety Notes
- Respect idempotency and exactly‑once semantics where applicable.
