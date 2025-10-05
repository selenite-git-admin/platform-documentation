# Gateway – Data Model

## Scope
Logical entities and relationships.

## Entities
### Route
Path and upstream mapping.

| Field | Type | Req | Notes |
|------|------|-----|------|
| path | string | ✓ | PK |
| upstream | string | ✓ |  |
| retries | integer |  | default 1 |
| timeout_ms | integer |  |  |

### WAFPolicy
Ruleset and mode.

| Field | Type | Req | Notes |
|------|------|-----|------|
| policy_id | string | ✓ | PK |
| name | string | ✓ |  |
| mode | string | ✓ | detect,block |
| rules | array<string> | ✓ |  |

### RateLimit
Per‑tenant overrides.

| Field | Type | Req | Notes |
|------|------|-----|------|
| tenant_id | string | ✓ | PK |
| limit_rps | integer | ✓ |  |
| burst | integer |  |  |
| expires_at | datetime |  |  |

### Certificate
TLS certificate metadata.

| Field | Type | Req | Notes |
|------|------|-----|------|
| cert_id | string | ✓ | PK |
| domain | string | ✓ |  |
| not_after | datetime | ✓ |  |
| status | string | ✓ | active,rotating |

## Relationships


## Retention
- Logs: 30d · Metrics: 90d · Config history: 180d+
