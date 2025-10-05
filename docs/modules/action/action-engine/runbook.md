# Action Engine – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Slow actions | Rule eval queue depth | Scale workers; shard topics | P99 within target |
| Delivery failures | Endpoint error rate | Retry with backoff; quarantine endpoints | Error rate ↓ |
| DLQ growth | Poison messages | Inspect and purge after fix | DLQ stable |

## Procedures
### Drain safely
1. Pause rule executions
2. Let in-flight jobs complete
3. Resume after deploy

### Backlog recovery
1. Scale workers
2. Increase partitions
3. Re-enable consumers gradually

## Safety Notes
- Respect tenant rate limits and idempotency keys.
