# Action Delivery – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Slow actions | Rule eval queue depth | Scale workers; shard topics | P99 within target |
| Delivery failures | Endpoint error rate | Retry with backoff; quarantine endpoints | Error rate ↓ |
| DLQ growth | Poison messages | Inspect and purge after fix | DLQ stable |

## Procedures
### Quarantine endpoint
1. Block egress to endpoint
2. Notify tenant owner
3. Re-enable after receiver fix

### Purge poison messages
1. Identify repeated failures
2. Extract sample payload
3. Apply fix and replay

## Safety Notes
- Respect tenant rate limits and idempotency keys.
