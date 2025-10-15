# Data Model

## Scope
Persistent data structures for Platform Catalog. This page defines entities, relationships, DBML, DDL skeletons, seed examples, validation queries, and migration notes.

## Conventions
- Database: PostgreSQL
- Identifiers: snake_case
- Primary keys: surrogate `uuid` unless noted
- Timestamps: `timestamptz` in UTC
- Use effective dating for policy style tables
- Keep audit append only

## ERD
<a href="#fig-pc-erd" class="image-link">
  <img src="/assets/diagrams/platform-catalog/platform-catalog-erd.svg" alt="Platform Catalog ERD">
</a>

<div id="fig-pc-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/platform-catalog/platform-catalog-erd.svg" alt="Platform Catalog ERD">
</div>

_Figure 1: Platform Catalog ERD_{.figure-caption}

## Entities
Identity and segmentation
- `tenant_types`, `business_units`, `cost_centers`, `environment_codes`

Location and compliance
- `regions`, `data_residency_policies`, `compliance_profiles`

Plans and limits
- `product_plans`, `plan_features`, `default_limits`

Naming and tags
- `namespace_prefixes`, `tag_taxonomy`

Notifications
- `notification_channels`, `escalation_policies`

Calendars
Moved to Calendar Service. See [Calendar Service](../calendar-service/index.md)

## DBML
```dbml
Table tenant_types {
  code text [pk]
  description text
}

Table business_units {
  code text [pk]
  name text
}

Table cost_centers {
  code text [pk]
  name text
}

Table environment_codes {
  code text [pk]
  description text
}

Table regions {
  code text [pk]
  name text
  active boolean
}

Table data_residency_policies {
  policy_id uuid [pk]
  name text [not null, unique]
  requires_encryption boolean
  effective_from date
}

Table compliance_profiles {
  code text [pk]
  description text
}

Table namespace_prefixes {
  prefix text [pk]
  description text
}

Table tag_taxonomy {
  key text [pk]
  pattern text
}

Table tag_taxonomy_values {
  key text [not null, ref: > tag_taxonomy.key]
  value text [not null]
  Primary Key (key, value)
}

Table notification_channels {
  code text [pk]
  target text
  kind text
}

Table escalation_policies {
  policy_id uuid [pk]
  name text
  rules json
}

Table catalog_audit {
  audit_id uuid [pk]
  actor text
  action text [not null]
  target text
  old_value json
  new_value json
  at timestamp [not null]
}
```

## DDL skeletons
```sql
create table if not exists regions (
  code text primary key,
  name text not null,
  active boolean not null default true
);

create table if not exists data_residency_policies (
  policy_id uuid primary key,
  name text not null unique,
  allowed_regions text[] not null,
  requires_encryption boolean not null default true,
  effective_from date not null default current_date
);

create table if not exists product_plans (
  plan_code text primary key,
  name text,
  active boolean not null default true
);

create table if not exists plan_features (
  plan_code text references product_plans(plan_code),
  feature_key text,
  value jsonb,
  primary key (plan_code, feature_key)
);

create table if not exists default_limits (
  plan_code text references product_plans(plan_code),
  limit_name text,
  limit_value bigint,
  primary key (plan_code, limit_name)
);

create table if not exists namespace_prefixes (
  prefix text primary key,
  description text
);

create table if not exists tag_taxonomy (
  key text,
  allowed_values text[],
  pattern text,
  primary key (key)
);

create table if not exists notification_channels (
  code text primary key,
  target text,
  kind text
);

create table if not exists escalation_policies (
  policy_id uuid primary key,
  name text,
  rules jsonb
);

create table if not exists calendar_definitions (
  calendar_id uuid primary key,
  name text not null unique,
  kind text not null check (kind in ('holiday','business_hours','blackout','maintenance')),
  timezone text not null,
  active boolean not null default true
);

create table if not exists calendar_events (
  event_id uuid primary key,
  calendar_id uuid not null references calendar_definitions(calendar_id),
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  label text not null,
  attributes jsonb
);

create table if not exists calendar_sets (
  set_id uuid primary key,
  name text not null unique,
  members uuid[] not null
);

create table if not exists tenant_calendar_overlays (
  overlay_id uuid primary key,
  tenant_id uuid not null,
  set_id uuid not null references calendar_sets(set_id),
  add_events jsonb,
  suppress_event_ids uuid[]
);

create table if not exists catalog_audit (
  audit_id uuid primary key,
  actor text,
  action text not null,
  target text,
  old_value jsonb,
  new_value jsonb,
  at timestamptz not null default now()
);
create index if not exists idx_catalog_audit_time on catalog_audit(at);
```

## Validation queries
```sql
-- active regions
select code, name from regions where active = true order by code;

-- effective residency policies
select name, allowed_regions from data_residency_policies order by effective_from desc;

-- plan defaults
select p.plan_code, f.feature_key, f.value, l.limit_name, l.limit_value
from product_plans p
left join plan_features f on f.plan_code = p.plan_code
left join default_limits l on l.plan_code = p.plan_code
where p.active = true;

-- resolve calendar set membership
select s.name, d.name as calendar_name
from calendar_sets s
join unnest(s.members) as m(calendar_id) on true
join calendar_definitions d on d.calendar_id = m.calendar_id;
```

## Migration notes
- Use effective dating for policies that change over time
- Keep audit append only; never rewrite history
- Normalize when read patterns need it, otherwise keep tables simple and denormalized


Features and limits moved to Access: [Subscription Enforcement](../../platform-subscription/subscription-enforcement/index.md)
