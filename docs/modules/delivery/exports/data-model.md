# Exports – Data Model

## Scope
Logical entities and relationships used by exports.

## Entities
### ExportJob
Delivery of snapshot to target.

| Field | Type | Req | Notes |
|------|------|-----|------|
| export_id | string | ✓ | PK |
| dataset | string | ✓ |  |
| version | string | ✓ |  |
| format | string | ✓ | csv,parquet |
| target | string | ✓ | URI |
| snapshot_ref | string |  | FK→Published Store |
| status | string | ✓ | queued,running,done,failed |

### Artifact
Exported output object.

| Field | Type | Req | Notes |
|------|------|-----|------|
| uri | string | ✓ | Output location |
| bytes | integer |  | Size |

## Relationships
- ExportJob 1→* Artifact

## Retention
- Requests: 30d · Metrics: 90d · Receipts: 180d+
