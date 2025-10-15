# Data Store Catalog (Catalog)

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Overview
Mid sized enterprises want insights without building a data platform. Catalog provides a single source to discover datasets and learn how to read them inside a governed PostgreSQL estate. It removes guesswork, reduces integration cost, and stabilizes dependencies across layers.

Catalog records dataset identity, PostgreSQL coordinates, schema, classification, ownership, and lifecycle policy. It answers two questions for any consumer. Where is the dataset and how do I read it. Catalog is optimized for read availability and stable identifiers. Freshness is provided by DRR. Catalog focuses on discovery and access contracts.

## Design Principles
- Stable identity. A dataset has a durable logical id that stays the same across moves.
- PostgreSQL first. Physical coordinates reference governed Postgres databases and schemas.
- Zero engineering. Consumers use standard SQL and simple HTTP APIs. No warehouses or proprietary engines.
- Contract first. Schema references and compatibility rules are part of the record.
- Least privilege. Callers see only what they are allowed to see.
- Low latency. Reads are fast and predictable.

## Domain Model in Context
Each dataset is registered with a logical id and one or more PostgreSQL locations. A location points to a database and schema table name or a materialized view used for serving. Catalog also stores schema references, lineage pointers, retention policy, and data classification.

When a dataset moves or evolves, the owning module submits a migration that updates the record. Consumers continue to resolve the same logical id. Compatibility rules indicate whether a change is backward compatible.

### Example Interaction
A service wants to read KPI data.
1. Resolve coordinates: `GET /storage/v1/catalog/datasets/kpi.cash_conversion_cycle_v2`
2. Optional freshness check: `GET /storage/v1/datasets/kpi.cash_conversion_cycle_v2/freshness` from DRR
3. Read from the returned PostgreSQL table using the documented access class

**Example response**
```json
{
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "layer": "kpi",
  "physical": [
    {"type": "postgres_table", "database": "platform_store", "schema": "kpi", "name": "cash_conversion_cycle_v2"}
  ],
  "schema_uri": "s3://schemas/kpi/cash_conversion_cycle_v2/1.4.0/json",
  "classification": "internal",
  "retention": {"policy": "90d_raw_365d_agg"},
  "owner": {"module": "kpi-service", "email": "kpi-owners@example.com"},
  "access_class": "read_internal",
  "tags": ["finance", "executive"],
  "compatibility": {"mode": "backward", "since": "1.3.0"}
}
```

## Responsibilities
- Maintain catalog entries for all datasets in the Store family.
- Provide metadata for discovery, PostgreSQL coordinates, schema, classification, retention, lineage, and ownership.
- Enforce visibility by tenant and access class.
- Serve read APIs with 99.99 percent availability.
- Accept controlled write operations from owners and platform migrations.

## Interfaces
| Direction | Type | Endpoint | Authentication | Notes |
|-----------|------|----------|----------------|-------|
| Read | Public API | `/storage/v1/catalog/datasets/{id}` | user or m2m | Resolve a dataset descriptor |
| Read | Public API | `/storage/v1/catalog/datasets?layer=&tag=&tenant_id=` | user or m2m | Filtered listing with pagination |
| Read | Public API | `/storage/v1/catalog/datasets/{id}:describe?include=freshness` | user or m2m | Composite read that joins DRR |
| Write | Internal API | `/storage-internal/v1/catalog/datasets/{id}` | internal m2m | Upsert descriptor by owner or platform |
| Write | Internal API | `/storage-internal/v1/catalog/migrations` | internal m2m | Submit and apply migration steps |

## Guardrails
- Logical id is immutable once created. Breaking changes require a new major version.
- Physical coordinates point only to governed PostgreSQL resources. No external warehouses.
- Physical coordinates are updated through migrations with audit trail.
- Each dataset has a single owning module.
- Schema changes declare compatibility mode.
- Catalog does not store secrets. Access class maps to Postgres roles managed outside the record.

## Reliability
- Reads available at 99.99 percent. P99 latency under 100 ms.
- Writes gated by single writer per dataset. Conflict resolution is explicit.
- Multi region read replicas supported. Writes funnel to the primary region.
- ETag and cache headers supported on all read endpoints.

## Security
- Authentication through platform JWT for users and m2m for services.
- Authorization enforced through roles and tenant filters.
- Classification drives redaction behavior for public surfaces.
- All updates recorded to Evidence Ledger with correlation id.

## Dependencies
- Identity and Authorization for caller context and scopes.
- Evidence Ledger for change recording.
- DRR for optional freshness checks in composite reads.

## Summary
Data Store Catalog is the discovery system for a PostgreSQL governed platform. It gives every consumer the answer to where and how to read a dataset through stable identifiers and strict contracts. DRR tells whether the data is ready. Catalog tells where it lives and how to access it.