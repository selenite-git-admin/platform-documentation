# Compute Fabric – Data Model

## Scope
Logical entities and relationships.

## Entities
### Pool
Resource pool for workloads.

| Field | Type | Req | Notes |
|------|------|-----|------|
| pool_id | string | ✓ | PK |
| kind | string | ✓ | cpu,gpu |
| quota | object | ✓ | cpu,mem,concurrency |

### Job
Instance of execution.

| Field | Type | Req | Notes |
|------|------|-----|------|
| job_id | string | ✓ | PK |
| image | string | ✓ |  |
| cpu | integer | ✓ |  |
| mem_gib | number | ✓ |  |
| state | string | ✓ | queued,running,completed,failed,stopping |

## Relationships
- Pool 1→* Job (by placement)

## Retention
- Logs: 30d · Metrics: 90d · Job history: 180d+
