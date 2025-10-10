# Network Security – Data Model

## Scope
Logical entities and relationships.

## Entities
### Segment
Per‑tenant network segment or tag.

| Field | Type | Req | Notes |
|------|------|-----|------|
| segment_id | string | ✓ | PK |
| tenant_id | string | ✓ |  |
| cidr | string | ✓ | CIDR block |
| labels | array<string> |  |  |

### PrivateLink
Connectivity to external service.

| Field | Type | Req | Notes |
|------|------|-----|------|
| link_id | string | ✓ | PK |
| tenant_id | string | ✓ |  |
| service | string | ✓ | e.g., s3 |
| region | string | ✓ |  |
| status | string | ✓ | provisioning,active,failed |

### EgressPolicy
Outbound allow‑list.

| Field | Type | Req | Notes |
|------|------|-----|------|
| policy_id | string | ✓ | PK |
| tenant_id | string | ✓ |  |
| domains | array<string> | ✓ |  |
| ports | array<int> |  |  |
| status | string | ✓ | active,disabled |

## Relationships


## Retention
- Logs: 30d · Metrics: 90d · Config history: 180d+
