# Evidence Ledger – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| High latency | Cache hit ratio; provider health | Scale pods; warm cache | P99 ≤ target |
| Error spikes | Dependency status | Circuit break; retry/backoff | Error rate ↓ |

## Procedures
### Recover from integrity failure
1. Quarantine affected shard
2. Run full verify on previous checkpoints
3. Rebuild chain from last good root

### Export support
1. Start /export
2. Monitor job status
3. Share artifact with auditors

## Safety Notes
- Avoid manual state edits; use admin APIs.
