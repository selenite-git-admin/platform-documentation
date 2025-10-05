# Compute Fabric – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Stuck DAG | Pending nodes, blocked dependencies | Unblock dependency; resume DAG | DAG completes |
| Worker starvation | Queue depth, CPU/mem | Scale nodes; preempt low priority | P95 run latency ↓ |
| DLQ growth | Poison messages | Quarantine and replay after fix | DLQ stable |

## Procedures
### Hot pool contention
1. Enable burst capacity
2. Shift workloads to alternate pool
3. Tune bin‑packing weights

### Noisy neighbor
1. Throttle offending job
2. Migrate others
3. Apply network policy

## Safety Notes
- Respect idempotency and exactly‑once semantics where applicable.
