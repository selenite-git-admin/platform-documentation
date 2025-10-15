# Catalog – Data Model

## Scope
Logical entities and relationships used by catalog.

## Entities
### CatalogResource
Consumer-facing resource entry.

| Field | Type | Req | Notes |
|------|------|-----|------|
| id | string | ✓ | `kpi:<key>` or `dataset:<name>` |
| title | string | ✓ |  |
| summary | string |  |  |
| owner | string | ✓ |  |
| contract | string | ✓ | v1+ |
| tags | array<string> |  |  |
| freshness_sla | string |  | ISO-8601 duration |
| lineage_ref | string |  | Evidence/lineage pointer |

### Collection
Persona-oriented grouping.

| Field | Type | Req | Notes |
|------|------|-----|------|
| collection_id | string | ✓ | PK |
| title | string | ✓ |  |
| items | array<string> | ✓ | Resource ids |

## Relationships
- CatalogResource many↔many Collection

## Retention
- Requests: 30d · Metrics: 90d · Receipts: 180d+
