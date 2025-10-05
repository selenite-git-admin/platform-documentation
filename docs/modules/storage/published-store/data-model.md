# Published Store – Data Model

## Scope
Logical entities and relationships.

## Entities
### Snapshot
Materialized read‑only copy.

| Field | Type | Req | Notes |
|------|------|-----|------|
| snapshot_id | string | ✓ | PK |
| dataset | string | ✓ |  |
| version | string | ✓ |  |
| format | string | ✓ | parquet,csv |
| status | string | ✓ | building,ready,failed |

### ExportJob
Delivery of snapshot to target.

| Field | Type | Req | Notes |
|------|------|-----|------|
| export_id | string | ✓ | PK |
| snapshot_id | string | ✓ | FK→Snapshot |
| target | string | ✓ | URI |
| status | string | ✓ | queued,running,done,failed |

## Relationships
- Snapshot 1→* ExportJob

## Retention
- Raw: 90d+ (policy) · GDP: 365d · KPI: 365d+ · Published: per contract
