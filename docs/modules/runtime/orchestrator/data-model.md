# Orchestrator – Data Model

## Scope
Logical entities and relationships.

## Entities
### DAG
Directed acyclic graph of tasks.

| Field | Type | Req | Notes |
|------|------|-----|------|
| dag_id | string | ✓ | PK |
| schedule | string |  | cron |
| owner | string | ✓ |  |

### Run
Execution instance of a DAG.

| Field | Type | Req | Notes |
|------|------|-----|------|
| run_id | string | ✓ | PK |
| dag_id | string | ✓ | FK→DAG |
| window | object |  | from,to |
| state | string | ✓ | queued,running,success,failed |
| attempts | integer | ✓ | 0.. |

## Relationships
- DAG 1→* Run

## Retention
- Logs: 30d · Metrics: 90d · Job history: 180d+
