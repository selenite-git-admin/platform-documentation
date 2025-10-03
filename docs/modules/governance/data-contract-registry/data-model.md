# Data Model

## Scope
Persistent data structures for Data Contract Registry. This page defines entities, relationships, DBML, DDL skeletons, seed examples, validation queries, and migration notes.

## Conventions
- Database: PostgreSQL
- Identifiers: snake_case
- Primary keys: surrogate `uuid` unless noted
- Timestamps: `timestamptz` in UTC
- Soft delete is not used. Use status fields and history instead

## ERD
<a href="#fig-dcr-erd" class="image-link">
  <img src="/assets/diagrams/data-contract-registry/data-contract-registry-erd.svg" alt="Data Contract Registry ERD">
</a>

<div id="fig-dcr-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-contract-registry/data-contract-registry-erd.svg" alt="Data Contract Registry ERD">
</div>

_Figure 1: Data Contract Registry ERD_{.figure-caption}

## Entities
- `datasets`
  Registered datasets with ownership and lifecycle status
- `contract_versions`
  Immutable schema versions per dataset and layer. Exactly one version may be current per dataset and layer
- `schema_artifacts` (optional)
  References to external Schema Registry IDs and metadata for artifacts
- `subscriptions`
  Consumer requirements for compatibility and minimum version per dataset and layer
- `audit_log`
  Administrative actions and state transitions

## Relationships
- One `datasets` to many `contract_versions`
- One `datasets` to many `subscriptions`
- One `contract_versions` to zero or one `schema_artifacts`

## Status and enums
- Dataset status: `active`, `deprecated`, `retired`
- Layer: `extraction`, `raw`, `gold`, `activation`
- Compatibility posture: `backward`, `forward`, `both`, `none`

## DBML
```dbml
Project BareCount_DataContractRegistry {
  database_type: "PostgreSQL"
}

Table datasets {
  dataset_id uuid [pk]
  namespace text [not null, note: 'e.g. sap.mm or materials']
  name text [not null, note: 'e.g. mara or key_materials']
  owner text [not null]
  steward text
  status text [not null, note: 'active|deprecated|retired']
  created_at timestamptz [not null, default: `now()`]
  created_by text
  Indexes {
    (namespace, name) [unique]
  }
}

Table contract_versions {
  version_id uuid [pk]
  dataset_id uuid [not null, ref: > datasets.dataset_id]
  layer text [not null, note: 'extraction|raw|gold|activation']
  version int [not null]
  schema_json jsonb
  schema_registry_id text
  compatibility text [not null, note: 'backward|forward|both|none']
  is_current boolean [not null, default: false]
  created_at timestamptz [not null, default: `now()`]
  created_by text
  Indexes {
    (dataset_id, layer, version) [unique]
  }
}

Table schema_artifacts {
  artifact_id uuid [pk]
  version_id uuid [not null, ref: > contract_versions.version_id]
  schema_registry_id text [note: 'reference to external Schema Registry']
  artifact_hash text
  size_bytes bigint
  created_at timestamptz [not null, default: `now()`]
  Indexes {
    (version_id) [unique]
  }
}

Table subscriptions {
  subscription_id uuid [pk]
  dataset_id uuid [not null, ref: > datasets.dataset_id]
  layer text [not null, note: 'extraction|raw|gold|activation']
  consumer text [not null, note: 'service or team id']
  required_compatibility text [not null, note: 'backward|forward|both']
  min_version int [default: 1]
  created_at timestamptz [not null, default: `now()`]
  created_by text
  Indexes {
    (dataset_id, layer, consumer) [unique]
  }
}

Table audit_log {
  audit_id uuid [pk]
  actor text
  action text [not null]
  target text
  old_value jsonb
  new_value jsonb
  at timestamptz [not null, default: `now()`]
  Indexes {
    (at)
  }
}
```

## DDL skeletons
```sql
create table if not exists datasets (
  dataset_id uuid primary key,
  namespace text not null,
  name text not null,
  owner text not null,
  steward text,
  status text not null check (status in ('active','deprecated','retired')),
  created_at timestamptz not null default now(),
  created_by text,
  unique (namespace, name)
);

create table if not exists contract_versions (
  version_id uuid primary key,
  dataset_id uuid not null references datasets(dataset_id),
  layer text not null check (layer in ('extraction','raw','gold','activation')),
  version int not null,
  schema_json jsonb,
  schema_registry_id text,
  compatibility text not null check (compatibility in ('backward','forward','both','none')),
  is_current boolean not null default false,
  created_at timestamptz not null default now(),
  created_by text,
  unique (dataset_id, layer, version)
);

create table if not exists schema_artifacts (
  artifact_id uuid primary key,
  version_id uuid not null references contract_versions(version_id),
  schema_registry_id text,
  artifact_hash text,
  size_bytes bigint,
  created_at timestamptz not null default now(),
  unique (version_id)
);

create table if not exists subscriptions (
  subscription_id uuid primary key,
  dataset_id uuid not null references datasets(dataset_id),
  layer text not null check (layer in ('extraction','raw','gold','activation')),
  consumer text not null,
  required_compatibility text not null check (required_compatibility in ('backward','forward','both')),
  min_version int default 1,
  created_at timestamptz not null default now(),
  created_by text,
  unique (dataset_id, layer, consumer)
);

create table if not exists audit_log (
  audit_id uuid primary key,
  actor text,
  action text not null,
  target text,
  old_value jsonb,
  new_value jsonb,
  at timestamptz not null default now()
);
create index if not exists idx_audit_time on audit_log(at);
```

## Seed examples
```sql
insert into datasets (dataset_id, namespace, name, owner, status)
values (gen_random_uuid(), 'sap.mm', 'mara', 'platform-admins', 'active');

insert into contract_versions (version_id, dataset_id, layer, version, schema_json, compatibility, is_current)
select gen_random_uuid(), d.dataset_id, 'extraction', 1,
       '{"type":"record","name":"mara_extraction","fields":[{"name":"matnr","type":"string"},{"name":"maktx","type":"string"}]}'::jsonb,
       'both',
       true
from datasets d
where d.namespace = 'sap.mm' and d.name = 'mara';
```

## Validation queries
```sql
-- list current versions per dataset and layer
select d.namespace, d.name, v.layer, v.version
from datasets d
join contract_versions v on v.dataset_id = d.dataset_id
where v.is_current = true
order by d.namespace, d.name, v.layer;

-- subscriptions for activation layer
select d.namespace, d.name, s.consumer, s.min_version
from subscriptions s
join datasets d on d.dataset_id = s.dataset_id
where s.layer = 'activation';
```

## Migration notes
- Treat `contract_versions` as immutable. New version creates a new row and flips `is_current`
- Ensure at most one current per `(dataset_id, layer)` via application logic
- Prefer referencing external Schema Registry via `schema_registry_id` when available
- Add indexes after query patterns are observed
- Validate `schema_json` in application code when storing artifacts
