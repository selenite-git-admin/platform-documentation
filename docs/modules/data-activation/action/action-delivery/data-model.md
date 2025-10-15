# Action Delivery – Data Model

## Scope
Logical entities and relationships.

## Entities
### Endpoint
Configured delivery target.

| Field | Type | Req | Notes |
|------|------|-----|------|
| endpoint_id | string | ✓ | PK |
| kind | string | ✓ | email,slack,itsm,webhook |
| config | object | ✓ | host, path, headers |
| status | string | ✓ | healthy,degraded,blocked |

### Receipt
Result of a delivery attempt.

| Field | Type | Req | Notes |
|------|------|-----|------|
| job_id | string | ✓ | PK1 |
| attempt | integer | ✓ | PK2 |
| code | integer | ✓ | HTTP or channel code |
| latency_ms | integer | ✓ |  |
| signature | string |  | webhook signature |

## Relationships
- Endpoint 1→* Receipt

## Retention
- Logs: 30d · Metrics: 90d · Action history: 90d+
