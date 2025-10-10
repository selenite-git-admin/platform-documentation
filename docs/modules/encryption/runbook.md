# Encryption – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| High latency | Cache hit ratio; provider health | Scale pods; warm cache | P99 ≤ target |
| Error spikes | Dependency status | Circuit break; retry/backoff | Error rate ↓ |

## Procedures
### Rotate key alias
1. Call /admin/rotate
2. Verify active_kid changed
3. Confirm decrypt works for old data

### Handle KMS outage
1. Enable circuit breaker
2. Fail closed for decrypt/sign
3. Queue operations until recovery

## Safety Notes
- Avoid manual state edits; use admin APIs.
