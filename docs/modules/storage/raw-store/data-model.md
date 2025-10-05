# Raw Store – Data Model

## Scope
Logical entities and relationships.

## Entities
### RawObject
Immutable object with metadata.

| Field | Type | Req | Notes |
|------|------|-----|------|
| object_id | string | ✓ | PK |
| source | string | ✓ |  |
| checksum | string | ✓ | sha256 |
| bytes | integer | ✓ |  |
| partition | string | ✓ | dt=YYYY-MM-DD/... |
| tags | object |  | k:v |

### IngestReceipt
Result of ingest.

| Field | Type | Req | Notes |
|------|------|-----|------|
| receipt_id | string | ✓ | PK |
| object_id | string |  | FK→RawObject |
| status | string | ✓ | accepted,rejected |
| reason | string |  |  |

## Relationships


## Retention
- Raw: 90d+ (policy) · GDP: 365d · KPI: 365d+ · Published: per contract
