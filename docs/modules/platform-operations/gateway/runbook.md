# Gateway – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Elevated 4xx | WAF rule changes, client errors | Roll back rule set; tune false positives | Block rate normalizes |
| TLS errors | Cert expiry, mismatch | Rotate certs via admin API | Handshake success |
| Latency spike | Rate limiters, backends | Scale edge; enable surge mode | P99 ≤ target |

## Procedures
### Roll back WAF policy
1. Switch to shadow mode
2. Reapply baseline
3. Monitor block rate

### Blue/green cert rotate
1. Upload new cert
2. Activate green
3. Rollback if handshake fails

## Safety Notes
- Never disable WAF protections in production; use per‑tenant exceptions.
