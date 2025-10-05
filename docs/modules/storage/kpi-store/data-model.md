# KPI Store – Data Model

## Scope
Logical entities and relationships.

## Entities
### KPI
Named metric with contract.

| Field | Type | Req | Notes |
|------|------|-----|------|
| kpi | string | ✓ | PK |
| contract | string | ✓ | v1,v2 |

### Series
Time series points.

| Field | Type | Req | Notes |
|------|------|-----|------|
| kpi | string | ✓ | PK1 |
| ts | datetime | ✓ | PK2 |
| value | float | ✓ |  |
| dim | object |  | dimension map |

## Relationships
- KPI 1→* Series

## Retention
- Raw: 90d+ (policy) · GDP: 365d · KPI: 365d+ · Published: per contract
