# Metering – Data Model

## Scope
Logical entities and relationships.

## Entities
### Delta
Usage increment event.

| Field | Type | Req | Notes |
|------|------|-----|------|
| event_id | string |  | Idempotency |
| tenant_id | string | ✓ |  |
| feature | string | ✓ |  |
| units | integer | ✓ | positive |
| timestamp | datetime | ✓ | UTC |

### Counter
Aggregated usage.

| Field | Type | Req | Notes |
|------|------|-----|------|
| tenant_id | string | ✓ | PK1 |
| feature | string | ✓ | PK2 |
| window_start | datetime | ✓ | PK3 |
| window_end | datetime | ✓ |  |
| used | integer | ✓ |  |

## Relationships
- Delta many→Counter (by aggregation)

## Retention
- Logs: 30d · Metrics: 90d · Job history: 180d+
