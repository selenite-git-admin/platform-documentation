# Action Catalog – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Slow actions | Rule eval queue depth | Scale workers; shard topics | P99 within target |
| Delivery failures | Endpoint error rate | Retry with backoff; quarantine endpoints | Error rate ↓ |
| DLQ growth | Poison messages | Inspect and purge after fix | DLQ stable |

## Procedures
### Rollback template
1. Deprecate current version
2. Republish previous version
3. Invalidate caches

### Validation outage
1. Freeze publishes
2. Use cached schemas
3. Resume after fix

## Safety Notes
- Respect tenant rate limits and idempotency keys.
