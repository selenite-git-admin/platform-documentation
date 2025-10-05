# Network Security – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Elevated 4xx | WAF rule changes, client errors | Roll back rule set; tune false positives | Block rate normalizes |
| TLS errors | Cert expiry, mismatch | Rotate certs via admin API | Handshake success |
| Latency spike | Rate limiters, backends | Scale edge; enable surge mode | P99 ≤ target |

## Procedures
### Contain egress incident
1. Identify offending segment
2. Apply emergency deny‑all egress
3. Add minimal allow‑list and monitor

### Private link failure
1. Check provider status
2. Recreate link
3. Fail over to secondary region

## Safety Notes
- Never disable WAF protections in production; use per‑tenant exceptions.
