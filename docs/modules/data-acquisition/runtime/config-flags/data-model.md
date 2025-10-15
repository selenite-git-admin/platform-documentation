# Config & Flags – Data Model

## Scope
Logical entities and relationships.

## Entities
### Flag
Feature toggle.

| Field | Type | Req | Notes |
|------|------|-----|------|
| flag_id | string | ✓ | PK |
| key | string | ✓ | unique |
| rules | array<object> | ✓ | targeting |
| status | string | ✓ | active,paused |

### Evaluation
Flag decision record.

| Field | Type | Req | Notes |
|------|------|-----|------|
| eval_id | string | ✓ | PK |
| subject | string | ✓ |  |
| flag_key | string | ✓ |  |
| value | boolean | ✓ |  |
| variant | string |  |  |

## Relationships
- Flag 1→* Evaluation (sampling)

## Retention
- Logs: 30d · Metrics: 90d · Job history: 180d+
