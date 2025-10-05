# Schema Module

> **Purpose:** Authoritative contracts for **Raw**, **GDP**, and **KPI** data, with governed evolution, validation, and evidence.  
> **Backbone link:** Pipelines generate and validate code against these contracts at every stage.

## Tenets
- **Contracts over code.** Schemas are the source of truth; code is generated and validated against them.
- **Additive-first evolution.** No silent breaks; incompatible changes follow a migration plan.
- **Receipts & lineage.** Every write emits an evidence receipt, linked to ADRs and impact notifications.
- **Determinism.** Canonical JSON Schema (draft 2020‑12) + stable subject taxonomy.

## Subject Classes
- `raw:<source>.<stream>` — extractor payload; minimal normalization.
- `gdp:<entity>` — conformed entity model; stable IDs & semantics.
- `kpi:<measure>` — KPI payload; time windows & dimensions.
- `ref:<name>` — static reference tables (currencies, regions).
- `meta:<name>` — platform metadata (calendar, run receipts).

## Interfaces (high-level)
- REST: `/api/v1/schema-registry/...`
- CLI: `bc schema <subcommand>`
- Events: signed webhooks on create/deprecate/alias; mTLS optional.
- UI: subjects explorer, diff & impact map, deprecation planner.

## Cross-Module Contracts
- **Governance:** Data Contracts and policy checks gate schema writes.
- **Pipelines:** Ingestion validates Raw; transforms compile to GDP; KPIs validate before publish.
- **Catalog:** Receives item/relationship updates; powers discovery.
- **Delivery:** Cache invalidation on schema changes for API & dashboards.
- **Migration Service:** Plans/backfills for breaking changes.

See lifecycle details in: [`lifecycle/`](lifecycle/).
