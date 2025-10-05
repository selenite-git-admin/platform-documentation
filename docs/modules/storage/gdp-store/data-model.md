# GDP Store – Data Model

## Scope
Logical entities and relationships.

## Entities
### Dataset
Logical dataset with versions.

| Field | Type | Req | Notes |
|------|------|-----|------|
| dataset_id | string | ✓ | PK |
| current | string |  | FK→DatasetVersion.version |

### DatasetVersion
Materialized version.

| Field | Type | Req | Notes |
|------|------|-----|------|
| dataset_id | string | ✓ | PK1 |
| version | string | ✓ | PK2 |
| schema_id | string | ✓ | FK→Schema |
| status | string | ✓ | building,ready,failed |

## Relationships
- Dataset 1→* DatasetVersion

## Retention
- Raw: 90d+ (policy) · GDP: 365d · KPI: 365d+ · Published: per contract
