# Runbook

## Scope
Operational procedures for Calendar Service in incidents and routine tasks.

## Quick reference
| Symptom | First checks | Safe mitigations | Validation |
| --- | --- | --- | --- |
| Resolve latency spike | set size, hot tenants | Cache resolved ranges for common windows | p95 within target |
| Working time latency | payload size, tz conversions | Cache effective calendars, pre compute business windows | p95 within target |
| Wrong effective events | overlay mismatch | Re-fetch overlay, validate suppress ids against definitions | Correct events returned |

## Procedures

### 1. Investigate slow resolve
1. Check set membership size and event density
2. Verify cache hit ratio
3. Increase cache TTL for hot sets

### 2. Correct a bad overlay
1. Read overlay for tenant
2. Update with corrected add or suppress entries using a fresh Idempotency Key
3. Confirm resolve returns corrected events

### 3. Time zone anomalies
1. Confirm tz parameter passed by caller
2. Validate calendar definition timezone
3. Add tests for daylight saving boundaries

## Routine tasks
- Export calendar and fiscal snapshots monthly
- Review overlay usage and prune stale overlays

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
