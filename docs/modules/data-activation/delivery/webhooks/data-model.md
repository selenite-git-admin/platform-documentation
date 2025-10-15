# Webhooks – Data Model

## Scope
Logical entities and relationships used by webhooks.

## Entities
### Endpoint
Tenant delivery endpoint.

| Field | Type | Req | Notes |
|------|------|-----|------|
| endpoint_id | string | ✓ | PK |
| url | string | ✓ |  |
| events | array<string> | ✓ | Subscribed event keys |
| status | string | ✓ | active,paused |

### Delivery
Delivery attempt record.

| Field | Type | Req | Notes |
|------|------|-----|------|
| job_id | string | ✓ | PK |
| endpoint_id | string | ✓ | FK→Endpoint |
| code | integer | ✓ | HTTP code |
| latency_ms | integer | ✓ |  |

## Relationships
- Endpoint 1→* Delivery

## Retention
- Requests: 30d · Metrics: 90d · Receipts: 180d+
