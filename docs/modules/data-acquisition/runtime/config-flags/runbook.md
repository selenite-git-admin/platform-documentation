# Config & Flags – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Stuck DAG | Pending nodes, blocked dependencies | Unblock dependency; resume DAG | DAG completes |
| Worker starvation | Queue depth, CPU/mem | Scale nodes; preempt low priority | P95 run latency ↓ |
| DLQ growth | Poison messages | Quarantine and replay after fix | DLQ stable |

## Procedures
### Emergency kill switch
1. Activate killswitch
2. Notify owners
3. Roll back after mitigation

### Bad rollout
1. Pause flag
2. Fix rule/segment
3. Gradually re‑enable

## Safety Notes
- Respect idempotency and exactly‑once semantics where applicable.
