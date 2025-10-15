# Webhooks – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Endpoint outage | 5xx/timeout spikes | Quarantine endpoint; notify tenant | DLQ stable |
| Abuse traffic | High callbacks; low acceptance | Rate limit; require mTLS | Load normalizes |

## Procedures
### Handle endpoint outage
1. Quarantine endpoint
2. Notify tenant
3. Replay after recovery

### Mitigate abuse
1. Tighten rate limits
2. Enforce mTLS
3. Rotate secret

## Safety Notes
- Respect tenant rate limits and contracts.
