# Secrets – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| High latency | Cache hit ratio; provider health | Scale pods; warm cache | P99 ≤ target |
| Error spikes | Dependency status | Circuit break; retry/backoff | Error rate ↓ |

## Procedures
### Recover from provider outage
1. Enable read‑through cache
2. Rate limit reads per tenant
3. Backfill audit entries after recovery

### Emergency rotate secret
1. Trigger /admin/rotate
2. Notify dependent services
3. Verify rollout via health checks

## Safety Notes
- Avoid manual state edits; use admin APIs.
