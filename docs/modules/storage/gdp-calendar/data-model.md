# GDP Calendar – Data Model

## Scope
Logical entities and relationships.

## Entities
### Schedule
Dataset schedule with TZ.

| Field | Type | Req | Notes |
|------|------|-----|------|
| schedule_id | string | ✓ | PK |
| dataset | string | ✓ |  |
| cron | string | ✓ |  |
| timezone | string | ✓ | IANA TZ |
| status | string | ✓ | active,paused |

### Run
Execution result.

| Field | Type | Req | Notes |
|------|------|-----|------|
| run_id | string | ✓ | PK |
| dataset | string | ✓ |  |
| started_at | datetime | ✓ |  |
| ended_at | datetime |  |  |
| status | string | ✓ | running,success,failed |

## Relationships
- Schedule 1→* Run

## Retention
- Raw: 90d+ (policy) · GDP: 365d · KPI: 365d+ · Published: per contract
