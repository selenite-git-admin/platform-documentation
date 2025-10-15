# Activation APIs – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Cache storm | Hit ratio, request coalescing | Increase TTL; enable coalescing | Hit ratio ↑; P95 ↓ |
| Contract break | Resolver errors; 4xx spikes | Roll back; bump contract | Errors normalize |

## Procedures
### Mitigate cache storm
1. Enable coalescing
2. Increase TTL
3. Warm hotspot queries

### Handle contract break
1. Roll back resolver
2. Bump contract version
3. Notify integrators

## Safety Notes
- Respect tenant rate limits and contracts.
