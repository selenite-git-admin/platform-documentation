# Dashboards – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Share link abuse | Unusual origin IPs; spikes | Revoke link; tighten scopes | Traffic normalizes |
| Tile cache collapse | Hit ratio; CPU | Increase TTL; warm tiles | Hit ratio ↑ |

## Procedures
### Revoke abused link
1. Revoke share
2. Block offending IPs
3. Enable stricter scopes

### Recover cache
1. Increase TTL
2. Warm tiles
3. Enable coalescing

## Safety Notes
- Respect tenant rate limits and contracts.
