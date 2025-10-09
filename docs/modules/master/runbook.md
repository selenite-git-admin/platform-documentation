# Runbook

## Scope
Operational procedures for Platform Catalog. This runbook covers detection, triage, mitigation, and validation for read heavy operations and calendar resolution.

## Roles and access
- Catalog administrator for writes
- Operator with access to dashboards and logs

## Safety
- Prefer reversible actions
- Record each operator action with a correlation_id
- Use API calls. Avoid direct database changes

## Quick reference
| Symptom | First checks | Safe mitigations | Validation |
| --- | --- | --- | --- |
| Read latency spike | Route level p95 | Increase cache TTL, add missing indexes | p95 within target |
| Write errors increasing | Error codes by resource | Validate payloads, roll back last change if bad data | Errors drop |
| Event publish failures | Broker health | Retry publish with backoff, queue locally | Events flowing |
| Calendar resolve slow | Payload size, set size | Cache resolved sets for range, pre compute | Resolve within target |

## Procedures

### 1. Resolve stale reads due to cache
1. Confirm recent write in logs with `catalog.*` event names
2. Verify change event published
3. Purge or expire caches on consumers if lagging

### 2. Recover from bad catalog change
1. Identify bad write by correlation_id
2. Upsert a corrected record with a fresh Idempotency Key
3. Confirm change event fired and caches updated

### 3. Calendar resolution latency
1. Measure `resolve` route latency
2. Cache resolution results for common ranges
3. Consider splitting large calendar sets

## Routine tasks
- Export reference snapshots monthly
- Review active regions and plans quarterly
- Validate tag taxonomy against usage

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
