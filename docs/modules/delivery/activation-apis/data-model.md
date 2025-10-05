# Activation APIs – Data Model

## Scope
Logical entities and relationships used by activation apis.

## Entities
### Resource
Queryable entity (KPI or dataset).

| Field | Type | Req | Notes |
|------|------|-----|------|
| id | string | ✓ | PK |
| kind | string | ✓ | kpi,dataset |
| contract | string | ✓ | v1+ |

### QueryLog
Recorded query for audits.

| Field | Type | Req | Notes |
|------|------|-----|------|
| log_id | string | ✓ | PK |
| resource | string | ✓ |  |
| filters | object |  |  |
| duration_ms | integer | ✓ |  |

## Relationships
- Resource 1→* QueryLog (sampling)

## Retention
- Requests: 30d · Metrics: 90d · Receipts: 180d+
