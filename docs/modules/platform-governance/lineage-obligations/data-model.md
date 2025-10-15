# Data Model

## Scope
Defines persistent structures and relationships for Lineage Obligations. The model stores assets, processes, runs, edges, obligations, evaluation results, and audit events. It does not store business data. It records metadata needed to evaluate obligations against lineage.

## Conventions
- Database: PostgreSQL
- Identifiers: snake_case
- Primary keys: `uuid` unless noted
- Time: UTC. DBML uses `datetime`. DDL uses `timestamptz`
- JSON fields: `jsonb` in DDL

## Entities
- lineage_assets  
  Catalog of assets by tenant. Fields include `qualified_name`, `asset_type`, `layer` and optional `contract_ref` to Data Contract Registry. Tags hold key and value pairs from Platform Catalog taxonomy.
- lineage_processes  
  Processes that produce lineage. Captures engine name, code reference, and owner.
- lineage_runs  
  Executions of a process. Links to the process and tracks status and correlation id.
- lineage_edges  
  Edges observed within a run from a source asset to a destination asset. Captures operation kind and optional column mapping or stats.
- obligations  
  Checks to apply over lineage. References a policy in Policy Registry via `policy_ref`. `check_type` is a controlled value and parameters and scope are JSON.
- evaluations  
  Results of evaluating an obligation. Optionally ties to a specific run and asset.
- lineage_audit  
  Append only audit trail for changes to assets, processes, runs, edges, obligations, and evaluations.

## ERD
<a href="#fig-lo-erd" class="image-link">
  <img src="/assets/diagrams/lineage-obligations/lineage-obligations-erd.svg" alt="Lineage Obligations ERD">
</a>

<div id="fig-lo-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/lineage-obligations/lineage-obligations-erd.svg" alt="Lineage Obligations ERD">
</div>

_Figure 1: Lineage Obligations ERD_{.figure-caption}

## DBML
```dbml
Table lineage_assets {
  asset_id uuid [pk]
  tenant_id uuid [not null]
  asset_type text [not null]
  qualified_name text [not null, unique]
  layer text [not null]
  contract_ref text
  tags json
  created_at datetime
  updated_at datetime
  Indexes {
    (tenant_id)
    (layer)
  }
}

Table lineage_processes {
  process_id uuid [pk]
  tenant_id uuid [not null]
  name text [not null]
  system text
  code_ref text
  owner text
  created_at datetime
  updated_at datetime
  Indexes {
    (tenant_id, name) [unique]
  }
}

Table lineage_runs {
  run_id uuid [pk]
  process_id uuid [not null]
  started_at datetime [not null]
  ended_at datetime
  status text [not null]
  correlation_id text
  Indexes {
    (process_id, started_at)
  }
}

Table lineage_edges {
  edge_id uuid [pk]
  run_id uuid [not null]
  src_asset_id uuid [not null]
  dest_asset_id uuid [not null]
  op text [not null]
  columns json
  stats json
  created_at datetime
  Indexes {
    (run_id)
    (src_asset_id)
    (dest_asset_id)
  }
}

Table obligations {
  obligation_id uuid [pk]
  tenant_id uuid [not null]
  policy_ref text [not null]
  name text [not null]
  description text
  check_type text [not null]
  params json
  scope json
  enabled boolean [not null, default: true]
  created_at datetime
  updated_at datetime
  Indexes {
    (tenant_id, name) [unique]
  }
}

Table evaluations {
  eval_id uuid [pk]
  obligation_id uuid [not null]
  run_id uuid
  asset_id uuid
  status text [not null]
  details json
  evaluated_at datetime [not null]
  Indexes {
    (obligation_id, evaluated_at)
    (status)
  }
}

Table lineage_audit {
  audit_id uuid [pk]
  tenant_id uuid
  actor text
  action text [not null]
  target text
  old_value json
  new_value json
  at datetime [not null]
  Indexes {
    (at)
  }
}

Ref: lineage_runs.process_id > lineage_processes.process_id
Ref: lineage_edges.run_id > lineage_runs.run_id
Ref: lineage_edges.src_asset_id > lineage_assets.asset_id
Ref: lineage_edges.dest_asset_id > lineage_assets.asset_id
Ref: evaluations.obligation_id > obligations.obligation_id
Ref: evaluations.run_id > lineage_runs.run_id
Ref: evaluations.asset_id > lineage_assets.asset_id
```

## DDL skeletons
```sql
create table if not exists lineage_assets (
  asset_id uuid primary key,
  tenant_id uuid not null,
  asset_type text not null,
  qualified_name text not null unique,
  layer text not null,
  contract_ref text,
  tags jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists lineage_processes (
  process_id uuid primary key,
  tenant_id uuid not null,
  name text not null,
  system text,
  code_ref text,
  owner text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (tenant_id, name)
);

create table if not exists lineage_runs (
  run_id uuid primary key,
  process_id uuid not null,
  started_at timestamptz not null,
  ended_at timestamptz,
  status text not null check (status in ('success','failed','running','aborted')),
  correlation_id text
);

create table if not exists lineage_edges (
  edge_id uuid primary key,
  run_id uuid not null,
  src_asset_id uuid not null,
  dest_asset_id uuid not null,
  op text not null check (op in ('read','write','transform','join')),
  columns jsonb,
  stats jsonb,
  created_at timestamptz not null default now()
);

create table if not exists obligations (
  obligation_id uuid primary key,
  tenant_id uuid not null,
  policy_ref text not null,
  name text not null,
  description text,
  check_type text not null check (check_type in ('required_tag','forbid_flow','require_provenance','freshness_sla')),
  params jsonb,
  scope jsonb,
  enabled boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (tenant_id, name)
);

create table if not exists evaluations (
  eval_id uuid primary key,
  obligation_id uuid not null,
  run_id uuid,
  asset_id uuid,
  status text not null check (status in ('pass','fail','warn','skip')),
  details jsonb,
  evaluated_at timestamptz not null default now()
);

create table if not exists lineage_audit (
  audit_id uuid primary key,
  tenant_id uuid,
  actor text,
  action text not null,
  target text,
  old_value jsonb,
  new_value jsonb,
  at timestamptz not null default now()
);
create index if not exists idx_evaluations_obligation_time on evaluations(obligation_id, evaluated_at);
create index if not exists idx_edges_src on lineage_edges(src_asset_id);
create index if not exists idx_edges_dest on lineage_edges(dest_asset_id);
```

## Validation queries
```sql
-- most recent run status per process
select p.name, r.status, r.started_at
from lineage_processes p
join lateral (
  select status, started_at from lineage_runs rr
  where rr.process_id = p.process_id
  order by rr.started_at desc limit 1
) r on true;

-- assets with no incoming lineage and with no outgoing lineage
with deg as (
  select a.asset_id,
         sum(case when e.dest_asset_id = a.asset_id then 1 else 0 end) as in_deg,
         sum(case when e.src_asset_id = a.asset_id then 1 else 0 end) as out_deg
  from lineage_assets a
  left join lineage_edges e on e.src_asset_id = a.asset_id or e.dest_asset_id = a.asset_id
  group by a.asset_id
)
select * from deg where in_deg = 0 or out_deg = 0;

-- failed obligations in the last 7 days
select o.name, count(*) as fails
from evaluations ev
join obligations o on o.obligation_id = ev.obligation_id
where ev.status = 'fail' and ev.evaluated_at >= now() - interval '7 days'
group by 1 order by 2 desc;
```

## Migration notes
- Avoid destructive schema changes. Prefer additive columns and new tables
- Keep audit append only. Include actor and correlation id
- Index hot traversal paths. Measure before adding wide indexes
