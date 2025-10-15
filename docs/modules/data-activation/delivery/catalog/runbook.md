# Catalog – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Stale freshness | Upstream SLA feed | Re-ingest metadata | Freshness updated |
| Broken lineage links | Evidence registry | Rebuild pointers | Links resolve |

## Procedures
### Refresh metadata
1. Trigger metadata sync
2. Validate samples
3. Publish collection rebuild

### Fix lineage links
1. Inspect evidence refs
2. Recompute mappings
3. Re-publish entries

## Safety Notes
- Respect tenant rate limits and contracts.
