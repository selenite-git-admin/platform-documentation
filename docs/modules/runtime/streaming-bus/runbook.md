# Streaming Bus – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Stuck DAG | Pending nodes, blocked dependencies | Unblock dependency; resume DAG | DAG completes |
| Worker starvation | Queue depth, CPU/mem | Scale nodes; preempt low priority | P95 run latency ↓ |
| DLQ growth | Poison messages | Quarantine and replay after fix | DLQ stable |

## Procedures
### Consumer lag spike
1. Scale consumers
2. Investigate slow partitions
3. Rebalance groups

### Replay safely
1. Quiesce consumers
2. Start replay with watermark
3. Monitor DLQ

## Safety Notes
- Respect idempotency and exactly‑once semantics where applicable.
