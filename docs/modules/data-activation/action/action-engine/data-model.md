# Action Engine – Data Model

## Scope
Logical entities and relationships.

## Entities
### Rule
Condition and target template.

| Field | Type | Req | Notes |
|------|------|-----|------|
| rule_id | string | ✓ | PK |
| name | string | ✓ |  |
| expr | string | ✓ | condition |
| template_id | string | ✓ | FK→Template |
| status | string | ✓ | active,paused |

### Job
Executable action created by rules.

| Field | Type | Req | Notes |
|------|------|-----|------|
| job_id | string | ✓ | PK |
| rule_id | string | ✓ | FK→Rule |
| state | string | ✓ | queued,running,completed,failed,dlq |
| retries | integer | ✓ | 0.. |
| payload | object | ✓ | rendered template |

## Relationships
- Rule 1→* Job

## Retention
- Logs: 30d · Metrics: 90d · Action history: 90d+
