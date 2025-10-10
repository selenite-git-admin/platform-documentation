# Evidence Ledger – Data Model

## Scope
Logical entities and relationships.

## Entities
### Evidence
Immutable record with hash chaining.

| Field | Type | Req | Notes |
|------|------|-----|------|
| evidence_id | string | ✓ | PK |
| tenant_id | string | ✓ |  |
| kind | string | ✓ | decision, admin, security |
| payload | object | ✓ | JSON |
| hash | string | ✓ | chained |
| prev_hash | string |  | link to previous |
| timestamp | datetime | ✓ | UTC |

### ExportJob
Asynchronous export task.

| Field | Type | Req | Notes |
|------|------|-----|------|
| export_id | string | ✓ | PK |
| from | datetime | ✓ |  |
| to | datetime | ✓ |  |
| status | string | ✓ | queued, running, done, failed |
| location | string |  | URI |

## Relationships
- Evidence many→1 Export range

## Retention
- Logs: 30d · Metrics: 90d · Evidence (ledger): 90d+
