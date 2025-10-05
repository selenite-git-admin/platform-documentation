# Data Model

> Schemas are additive. Fields are lowercase snake_case. Timestamps are ISO‑8601 UTC.

## Common types
- `ulid` — sortable unique id
- `json` — freeform object validated per contract
- `uri` — RFC 3986

## Tables / Collections
### `migration-service_resource`
| field | type | notes |
|---|---|---|
| id | ulid | primary key |
| tenant_id | ulid | isolation |
| name | string | unique per tenant |
| spec | json | contract-specific |
| status | enum(`active`,`inactive`,`deprecated`) | |
| created_at | timestamp | |
| updated_at | timestamp | |

### `receipt`
| field | type | notes |
|---|---|---|
| evidence_id | ulid | receipt id |
| subject_id | ulid | references `migration-service_resource.id` |
| action | enum | e.g., `create`,`update`,`delete` |
| actor | string | service/user |
| checksum | string | integrity |
| created_at | timestamp | |

## Indexing
- `(tenant_id, name)` unique
- `(tenant_id, updated_at)` covering for lists

## Lineage
- Each mutation emits `receipt` linked to upstream contract/policy ids where applicable.

    ### `migration_plan`
    | field | type | notes |
    |---|---|---|
    | id | ulid | |
    | subject | string | dataset/kpi |
    | steps | json | ordered operations |
    | dry_run | bool | |
    | status | enum | `planned`,`running`,`paused`,`completed`,`failed`,`rolled_back` |
    | created_at | timestamp | |
    | updated_at | timestamp | |
