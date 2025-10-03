# Data Model

## Scope
Persistent data structures for Tenant Management. This page defines entities, relationships, DBML, DDL skeletons, validation queries, and migration notes.

## Conventions
- Database: PostgreSQL
- Identifiers: snake_case
- Primary keys: surrogate `uuid` unless noted
- Timestamps: `timestamptz` in UTC
- Audit is append only

## ERD
<a href="#fig-tm-erd" class="image-link">
  <img src="/assets/diagrams/tenant-management/tenant-management-erd.svg" alt="Tenant Management ERD">
</a>

<div id="fig-tm-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/tenant-management/tenant-management-erd.svg" alt="Tenant Management ERD">
</div>

_Figure 1: Tenant Management ERD_{.figure-caption}

## DBML
```dbml
Table tenants {
  tenant_id uuid [pk]
  slug text [not null, unique] // stable short handle
  legal_name text [not null]
  status text [not null] // draft | active | suspended | archived
  created_at timestamp
  updated_at timestamp
  Indexes { (status) }
}

Table tenant_regions {
  tenant_id uuid [not null]
  region_code text [not null] // ref: Platform Catalog regions.code
  Primary Key (tenant_id, region_code)
}

Table tenant_residency {
  residency_id uuid [pk]
  tenant_id uuid [not null]
  policy_id uuid [not null] // ref: Platform Catalog data_residency_policies.policy_id
  effective_from date [not null]
  effective_to date // null = open ended
  Indexes { (tenant_id, effective_from) }
}

Table tenant_plan_assignments {
  assignment_id uuid [pk]
  tenant_id uuid [not null]
  plan_code text [not null] // enforced by Subscription Enforcement
  effective_from date [not null]
  effective_to date
  status text [not null] // proposed | active | ended
  Indexes { (tenant_id, effective_from) }
}

Table tenant_contacts {
  contact_id uuid [pk]
  tenant_id uuid [not null]
  role text [not null] // owner | billing | security | operations
  name text [not null]
  email text [not null]
  phone text
  active boolean
  Indexes { (tenant_id, role) }
}

Table tenant_external_ids {
  tenant_id uuid [not null]
  system_key text [not null] // billing | crm | support | sap_company_code etc.
  id_value text [not null]
  Primary Key (tenant_id, system_key)
}

Table tenant_tags {
  tenant_id uuid [not null]
  tag_key text [not null] // ref: Platform Catalog tag_taxonomy.key
  tag_value text [not null] // must conform to taxonomy if enumerated
  Primary Key (tenant_id, tag_key, tag_value)
}

Table tenant_audit {
  audit_id uuid [pk]
  tenant_id uuid
  actor text
  action text [not null] // create | update | lifecycle | plan | residency | regions | contacts | external_ids | tags
  target text
  old_value json
  new_value json
  at timestamp [not null]
}
```

## DDL skeletons
```sql
create table if not exists tenants (
  tenant_id uuid primary key,
  slug text not null unique,
  legal_name text not null,
  status text not null check (status in ('draft','active','suspended','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists tenant_regions (
  tenant_id uuid not null,
  region_code text not null,
  primary key (tenant_id, region_code)
);

create table if not exists tenant_residency (
  residency_id uuid primary key,
  tenant_id uuid not null,
  policy_id uuid not null,
  effective_from date not null,
  effective_to date
);

create table if not exists tenant_plan_assignments (
  assignment_id uuid primary key,
  tenant_id uuid not null,
  plan_code text not null,
  effective_from date not null,
  effective_to date,
  status text not null check (status in ('proposed','active','ended'))
);

create table if not exists tenant_contacts (
  contact_id uuid primary key,
  tenant_id uuid not null,
  role text not null check (role in ('owner','billing','security','operations')),
  name text not null,
  email text not null,
  phone text,
  active boolean not null default true
);

create table if not exists tenant_external_ids (
  tenant_id uuid not null,
  system_key text not null,
  id_value text not null,
  primary key (tenant_id, system_key)
);

create table if not exists tenant_tags (
  tenant_id uuid not null,
  tag_key text not null,
  tag_value text not null,
  primary key (tenant_id, tag_key, tag_value)
);

create table if not exists tenant_audit (
  audit_id uuid primary key,
  tenant_id uuid,
  actor text,
  action text not null,
  target text,
  old_value jsonb,
  new_value jsonb,
  at timestamptz not null default now()
);
create index if not exists idx_tenant_audit_time on tenant_audit(at);
```

## Validation queries
```sql
-- active tenants by region
select r.region_code, count(*) tenants
from tenant_regions r
join tenants t on t.tenant_id = r.tenant_id and t.status = 'active'
group by 1 order by 2 desc;

-- current residency policy per tenant
select t.slug, rr.policy_id
from tenants t
left join lateral (
  select policy_id from tenant_residency r
  where r.tenant_id = t.tenant_id and (r.effective_to is null or r.effective_to >= current_date)
  order by r.effective_from desc limit 1
) rr on true;

-- current plan per tenant
select t.slug, pp.plan_code
from tenants t
left join lateral (
  select plan_code from tenant_plan_assignments p
  where p.tenant_id = t.tenant_id and (p.effective_to is null or p.effective_to >= current_date)
  order by p.effective_from desc limit 1
) pp on true;
```

## Migration notes
- Avoid destructive schema changes on tenants
- Keep audit append only and include actor and correlation id
- Prefer additive tag taxonomy in Platform Catalog and validate at write time
