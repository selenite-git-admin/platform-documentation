# Data Store Catalog (Catalog) Data Model

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
The Catalog data model records dataset identity, PostgreSQL locations, schema references, compatibility, lineage, ownership, and lifecycle. It is optimized for read-heavy discovery with controlled writes from owners and platform migrations. All datasets live inside governed PostgreSQL stores.

## Model Overview
Primary entities

| Table | Purpose |
|-------|---------|
| `catalog_dataset` | Canonical registry of datasets with identity and ownership |
| `catalog_location` | PostgreSQL physical coordinates for each dataset |
| `catalog_schema_version` | Schema references and version history |
| `catalog_compatibility` | Declared compatibility between schema versions |
| `catalog_tag` | Freeform tags applied to datasets |
| `catalog_dataset_tag` | Dataset to tag mapping |
| `catalog_lineage` | Upstream and downstream relationships |
| `catalog_deprecation` | Deprecation marker and replacement hints |
| `catalog_access_policy` | Access class and role mapping |
| `catalog_audit` | Immutable audit trail for changes |

Each table enforces referential integrity on `dataset_id`. Writes are transactional and idempotent through internal APIs.

## Entity Relationships

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/data-store-catalog/catalog-erd.svg" alt="Dataset Refresh Registry">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-store-catalog/catalog-erd.svg" alt="Dataset Refresh Registry">
</div>

_Figure 2: Dataset Catalog_{.figure-caption}


## Entity Definitions

### catalog_dataset
Canonical dataset record.

| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (PK) | Stable logical identifier `layer.name_version` |
| `layer` | text | raw, gdp, kpi, published |
| `title` | text | Human readable title |
| `summary` | text | Short description |
| `classification` | text | internal, restricted, public |
| `owner_module` | text | Owning module name |
| `owner_email` | text | Contact for stewardship |
| `tenant_scope` | text | single or multi |
| `created_at` | timestamptz | Creation time |
| `updated_at` | timestamptz | Last update |

Notes
- `dataset_id` is immutable. Breaking changes require a new id or major version.
- Visibility is enforced by RLS using tenant context.

### catalog_location
PostgreSQL physical coordinates for reads.

| Column | Type | Description |
|--------|------|-------------|
| `location_id` | uuid (PK) | Unique location identifier |
| `dataset_id` | text (FK) | Reference to `catalog_dataset` |
| `type` | text | postgres_table or postgres_matview |
| `database` | text | Logical database name |
| `schema` | text | Schema name |
| `name` | text | Table or materialized view name |
| `is_primary` | boolean | Preferred location for reads |
| `created_at` | timestamptz | Creation time |
| `updated_at` | timestamptz | Last update |

Rules
- At least one active location per dataset.
- Exactly one location marked as primary.

### catalog_schema_version
Schema reference for dataset versions.

| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (FK, PK part) | Dataset reference |
| `version` | text (PK part) | Semantic version string |
| `schema_uri` | text | URI of schema document (json, avro, parquet json) |
| `schema_type` | text | json, avro |
| `checksum` | text | Integrity checksum of the schema doc |
| `published_at` | timestamptz | When this version became current |
| `deprecated_at` | timestamptz | Optional deprecation time |

### catalog_compatibility
Declarative compatibility rules between versions.

| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (FK, PK part) | Dataset reference |
| `from_version` | text (PK part) | Older version |
| `to_version` | text (PK part) | Newer version |
| `mode` | text | backward, forward, full, none |
| `since` | text | First version where this applies |

### catalog_tag and catalog_dataset_tag
Tag dictionary and mapping.

| Column | Type | Description |
|--------|------|-------------|
| `tag` | text (PK) | Tag key |
| `created_at` | timestamptz | Creation time |

Mapping
| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (FK, PK part) | Dataset reference |
| `tag` | text (FK, PK part) | Tag key |

### catalog_lineage
Lightweight lineage references.

| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (FK, PK part) | Current dataset |
| `direction` | text (PK part) | upstream or downstream |
| `related_dataset_id` | text | Related dataset id |
| `note` | text | Optional context |
| `updated_at` | timestamptz | Last update |

### catalog_deprecation
Deprecation marker and replacement.

| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (FK, PK) | Dataset reference |
| `deprecated` | boolean | Deprecation flag |
| `replacement_dataset_id` | text | Suggested replacement id |
| `reason` | text | Reason for deprecation |
| `deprecated_at` | timestamptz | When deprecation was set |

### catalog_access_policy
Access class mapping to Postgres roles.

| Column | Type | Description |
|--------|------|-------------|
| `dataset_id` | text (FK, PK) | Dataset reference |
| `access_class` | text | read_internal, read_external, restricted |
| `role_name` | text | Postgres role to assume |
| `notes` | text | Optional guidance |
| `updated_at` | timestamptz | Last update |

### catalog_audit
Immutable audit trail for Catalog changes.

| Column | Type | Description |
|--------|------|-------------|
| `event_id` | uuid (PK) | Unique audit id |
| `dataset_id` | text | Dataset reference |
| `actor` | text | Service or user id |
| `action` | text | create, update, migrate, deprecate |
| `correlation_id` | text | External correlation id |
| `payload` | jsonb | Redacted change payload |
| `ts` | timestamptz | Event time |

## DBML

```dbml
Project Catalog {
  database_type: "PostgreSQL"
  note: "Data Store Catalog schema"
}

Table catalog_dataset as DS {
  dataset_id text [pk]
  layer text
  title text
  summary text
  classification text
  owner_module text
  owner_email text
  tenant_scope text
  created_at timestamptz
  updated_at timestamptz
}

Table catalog_location as LOC {
  location_id uuid [pk]
  dataset_id text [ref: > DS.dataset_id]
  type text
  database text
  schema text
  name text
  is_primary boolean
  created_at timestamptz
  updated_at timestamptz
}

Table catalog_schema_version as SV {
  dataset_id text [pk, ref: > DS.dataset_id]
  version text [pk]
  schema_uri text
  schema_type text
  checksum text
  published_at timestamptz
  deprecated_at timestamptz
}

Table catalog_compatibility as COMP {
  dataset_id text [ref: > DS.dataset_id]
  from_version text
  to_version text
  mode text
  since text
  indexes {
    (dataset_id, from_version, to_version) [pk]
  }
}

Table catalog_tag as TAG {
  tag text [pk]
  created_at timestamptz
}

Table catalog_dataset_tag as DSTAG {
  dataset_id text [ref: > DS.dataset_id]
  tag text [ref: > TAG.tag]
  indexes {
    (dataset_id, tag) [pk]
  }
}

Table catalog_lineage as LIN {
  dataset_id text [ref: > DS.dataset_id]
  direction text
  related_dataset_id text
  note text
  updated_at timestamptz
  indexes {
    (dataset_id, direction, related_dataset_id) [pk]
  }
}

Table catalog_deprecation as DEP {
  dataset_id text [pk, ref: > DS.dataset_id]
  deprecated boolean
  replacement_dataset_id text
  reason text
  deprecated_at timestamptz
}

Table catalog_access_policy as ACP {
  dataset_id text [pk, ref: > DS.dataset_id]
  access_class text
  role_name text
  notes text
  updated_at timestamptz
}

Table catalog_audit as AUD {
  event_id uuid [pk]
  dataset_id text [ref: > DS.dataset_id]
  actor text
  action text
  correlation_id text
  payload jsonb
  ts timestamptz
}
```

## Constraints and Integrity
- All foreign keys cascade on delete from `catalog_dataset` only when a dataset is fully removed as part of decommission.
- Writes require a valid dataset record and an owner or platform token.
- Catalog rejects updates that change `dataset_id` or violate compatibility rules.
- Audit events are immutable after insert.

## Retention and Classification
| Table | Retention | Classification |
|-------|-----------|----------------|
| catalog_dataset | Permanent | Metadata |
| catalog_location | Permanent | Metadata |
| catalog_schema_version | Permanent | Metadata |
| catalog_compatibility | Permanent | Metadata |
| catalog_tag, catalog_dataset_tag | Permanent | Metadata |
| catalog_lineage | Permanent | Metadata |
| catalog_deprecation | Permanent | Metadata |
| catalog_audit | 365 days | Audit metadata (no PII) |

## Query Access Patterns
| Use Case | Query Target | Expected Latency |
|---------|--------------|------------------|
| Resolve descriptor by id | catalog_dataset join catalog_location | <100 ms |
| Search by tag or layer | catalog_dataset join catalog_dataset_tag | <100 ms |
| Resolve schema and compatibility | catalog_schema_version join catalog_compatibility | <150 ms |
| List downstream references | catalog_lineage filtered by direction | <150 ms |

## Reliability Guarantees
- Reads are strongly consistent within a single region.
- Writes are atomic per dataset record.
- Migrations execute under transactional boundaries with audit entries.

## Data Ownership
- Primary writers are dataset owners and platform migrations.
- Readers are internal services and UIs through Catalog APIs.