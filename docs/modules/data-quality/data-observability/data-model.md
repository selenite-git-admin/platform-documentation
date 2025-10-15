# Data Model

> Schemas are additive. Fields are lowercase snake_case. Timestamps are ISO‑8601 UTC.

## Common types
- `ulid` — sortable unique id
- `json` — freeform object validated per contract
- `uri` — RFC 3986

## Tables / Collections
### `data-observability_resource`
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
| subject_id | ulid | references `data-observability_resource.id` |
| action | enum | e.g., `create`,`update`,`delete` |
| actor | string | service/user |
| checksum | string | integrity |
| created_at | timestamp | |

## Indexing
- `(tenant_id, name)` unique
- `(tenant_id, updated_at)` covering for lists

## Lineage
- Each mutation emits `receipt` linked to upstream contract/policy ids where applicable.

    ### `signal`
    | field | type | notes |
    |---|---|---|
    | id | ulid | |
    | dataset | string | subject |
    | kind | enum | `freshness`,`drift`,`volume`,`nulls`,`outlier` |
    | value | json | numeric or structured |
    | level | enum | `info`,`warn`,`critical` |
    | window_start | timestamp | |
    | window_end | timestamp | |
    | produced_at | timestamp | |

## Event schema

Each observability event uses a consistent structure so that producers and consumers can interoperate.

```json
{
  "event_id": "01JACQ2M8X3K7P6Z7VANR1K9A2",
  "tenant_id": "t-123",
  "dataset_id": "ds.gdp.sales.orders.v3",
  "layer": "gdp",
  "run_id": "r-2025-10-14-1100",
  "connector_id": "sap-odata-01",
  "plan_id": "plan-9f2c",
  "metric": "freshness_seconds",
  "value": 3420.0,
  "unit": "seconds",
  "window": "PT1H",
  "threshold": 3600.0,
  "comparison": "lte",
  "outcome": "pass",
  "dimensions": {"region": "APAC", "partition_key": "2025-10-14"},
  "emitted_at": "2025-10-14T11:10:02Z",
  "source": "operations"
}
```
Fields include identifiers, metric name and unit, the evaluation window, threshold comparison, outcome, and a small set of dimensions used for slicing and debugging.

## Metric taxonomy

The platform standardizes a small set of metrics with fixed units.

| Metric | Unit | Scope | Description |
|---|---|---|---|
| freshness_seconds | seconds | dataset | time elapsed since last successful update |
| completeness_pct | percent | dataset or partition | proportion of expected rows present |
| volume_delta_pct | percent | dataset | percent change versus baseline |
| schema_drift_count | count | run | number of incompatible schema changes |
| rule_violations_count | count | run | number of DQC rule failures |
| quality_score | percent | run | composite score produced by DQC |

## Snapshot model

A snapshot captures the exact metrics used by a promotion decision and is referenced by the Evidence Ledger.

```json
{
  "snapshot_id": "snap-0a2b",
  "run_id": "r-2025-10-14-1100",
  "dataset_id": "ds.kpi.finance.cashflow.v1",
  "metrics": [
    {"metric": "quality_score", "value": 97.5, "unit": "percent"},
    {"metric": "freshness_seconds", "value": 120.0, "unit": "seconds"}
  ],
  "hash": "merkle:e6b41b",
  "created_at": "2025-10-14T11:12:00Z"
}
```
