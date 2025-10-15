# Exports – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Export stuck | Snapshot ready; queue depth | Retry with backoff; verify target access | Job completes |
| High failures to a target | HTTP codes; throttling | Reduce concurrency; raise backoff | Failure rate ↓ |

## Procedures
### Unblock stuck export
1. Check snapshot availability
2. Inspect retries & DLQ
3. Replay after fix

### Stabilize flaky target
1. Throttle deliveries
2. Increase backoff
3. Coordinate with tenant

## Safety Notes
- Respect tenant rate limits and contracts.
