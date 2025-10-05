# Dashboards – Data Model

## Scope
Logical entities and relationships used by dashboards.

## Entities
### Dashboard
Logical dashboard.

| Field | Type | Req | Notes |
|------|------|-----|------|
| dashboard_id | string | ✓ | PK |
| status | string | ✓ | draft,active |

### ShareLink
Expiring share link.

| Field | Type | Req | Notes |
|------|------|-----|------|
| share_id | string | ✓ | PK |
| dashboard_id | string | ✓ | FK→Dashboard |
| expires_at | datetime | ✓ |  |

## Relationships
- Dashboard 1→* ShareLink

## Retention
- Requests: 30d · Metrics: 90d · Receipts: 180d+
