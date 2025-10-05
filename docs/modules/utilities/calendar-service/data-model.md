# Data Model

## Scope
Persistent data structures for Calendar Service. This page defines entities, relationships, DBML, DDL skeletons, seed examples, validation queries, and migration notes.

## Conventions
- Database: PostgreSQL
- Identifiers: snake_case
- Primary keys: surrogate `uuid` unless noted
- Timestamps: `timestamptz` in UTC
- Keep audit append only

## ERD
<a href="#fig-cal-erd" class="image-link">
  <img src="/assets/diagrams/calendar-service/calendar-service-erd.svg" alt="Calendar Service ERD">
</a>

<div id="fig-cal-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/calendar-service/calendar-service-erd.svg" alt="Calendar Service ERD">
</div>

_Figure 1: Calendar Service ERD_{.figure-caption}

## DBML
```dbml
Table calendar_definitions {
  calendar_id uuid [pk]
  name text [not null, unique]
  kind text [not null] // holiday | business_hours | blackout | maintenance
  timezone text [not null]
  active boolean
}

Table calendar_events {
  event_id uuid [pk]
  calendar_id uuid [not null, ref: > calendar_definitions.calendar_id]
  starts_at timestamp [not null]
  ends_at timestamp [not null]
  label text [not null]
  attributes json
}

Table calendar_sets {
  set_id uuid [pk]
  name text [not null, unique]
}

Table calendar_set_members {
  set_id uuid [not null, ref: > calendar_sets.set_id]
  calendar_id uuid [not null, ref: > calendar_definitions.calendar_id]
  Primary Key (set_id, calendar_id)
}

Table tenant_calendar_overlays {
  overlay_id uuid [pk]
  tenant_id uuid [not null]
  set_id uuid [not null, ref: > calendar_sets.set_id]
}

Table tenant_overlay_added_events {
  added_event_id uuid [pk]
  overlay_id uuid [not null, ref: > tenant_calendar_overlays.overlay_id]
  starts_at timestamp [not null]
  ends_at timestamp [not null]
  label text [not null]
  attributes json
}

Table tenant_overlay_suppressed_events {
  overlay_id uuid [not null, ref: > tenant_calendar_overlays.overlay_id]
  event_id uuid [not null, ref: > calendar_events.event_id]
  Primary Key (overlay_id, event_id)
}

Table fiscal_calendars {
  fiscal_id uuid [pk]
  name text [not null, unique]
  timezone text [not null]
  start_month int [not null] // 1..12
}

Table fiscal_periods {
  period_id uuid [pk]
  fiscal_id uuid [not null, ref: > fiscal_calendars.fiscal_id]
  year int [not null]
  period int [not null]
  starts_on date [not null]
  ends_on date [not null]
  Primary Key (fiscal_id, year, period)
}

Table calendar_audit {
  audit_id uuid [pk]
  actor text
  action text [not null]
  target text
  old_value json
  new_value json
  at timestamp [not null]
}

Table tenant_org_settings {
  tenant_id uuid [pk]
  week_start int // 1..7 (1=Mon)
  weekend_mask int // bitmask: 1=Mon ... 7=Sun
  default_set_id uuid [ref: > calendar_sets.set_id]
  default_timezone text
  business_hours json // per-day windows
  updated_at timestamp
}
Table date_table_profiles {
  profile_id uuid [pk]
  tenant_id uuid [not null]
  name text [not null]
  week_start int // 1..7
  weekend_mask int
  fiscal_id uuid [ref: > fiscal_calendars.fiscal_id]
  pattern text // standard | 445 | 454 | 544
  locale text
  timezone text
  created_at timestamp
  updated_at timestamp
  Indexes { (tenant_id, name) [unique] }
}

Table date_table_columns {
  profile_id uuid [not null, ref: > date_table_profiles.profile_id]
  column_key text [not null]
  enabled boolean
  Primary Key (profile_id, column_key)
}

Table date_table_materializations {
  materialization_id uuid [pk]
  profile_id uuid [not null, ref: > date_table_profiles.profile_id]
  start_date date [not null]
  end_date date [not null]
  format text // csv | parquet
  storage_uri text // optional pointer if persisted externally
  rows bigint
  generated_at timestamp
}

```

## DDL skeletons
```sql
create table if not exists calendar_definitions (
  calendar_id uuid primary key,
  name text not null unique,
  kind text not null,
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
  name text not null unique
);

create table if not exists calendar_set_members (
  set_id uuid not null references calendar_sets(set_id),
  calendar_id uuid not null references calendar_definitions(calendar_id),
  primary key (set_id, calendar_id)
);

create table if not exists tenant_calendar_overlays (
  overlay_id uuid primary key,
  tenant_id uuid not null,
  set_id uuid not null references calendar_sets(set_id)
);

create table if not exists tenant_overlay_added_events (
  added_event_id uuid primary key,
  overlay_id uuid not null references tenant_calendar_overlays(overlay_id),
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  label text not null,
  attributes jsonb
);

create table if not exists tenant_overlay_suppressed_events (
  overlay_id uuid not null references tenant_calendar_overlays(overlay_id),
  event_id uuid not null references calendar_events(event_id),
  primary key (overlay_id, event_id)
);

create table if not exists fiscal_calendars (
  fiscal_id uuid primary key,
  name text not null unique,
  timezone text not null,
  start_month int not null check (start_month between 1 and 12)
);

create table if not exists fiscal_periods (
  period_id uuid primary key,
  fiscal_id uuid not null references fiscal_calendars(fiscal_id),
  year int not null,
  period int not null,
  starts_on date not null,
  ends_on date not null,
  unique (fiscal_id, year, period)
);

create table if not exists calendar_audit (
  audit_id uuid primary key,
  actor text,
  action text not null,
  target text,
  old_value jsonb,
  new_value jsonb,
  at timestamptz not null default now()
);
create index if not exists idx_calendar_audit_time on calendar_audit(at);


create table if not exists tenant_org_settings (
  tenant_id uuid primary key,
  week_start int not null check (week_start between 1 and 7),
  weekend_mask int not null default 96, -- default Sat(6)=32 + Sun(7)=64 -> 96
  default_set_id uuid null references calendar_sets(set_id),
  default_timezone text not null default 'UTC',
  business_hours jsonb, -- e.g. {"mon":[["09:00","18:00"]], ...} in local tz
  updated_at timestamptz not null default now()
);
```

## Validation queries
```sql
-- resolve set membership
select s.name, d.name as calendar_name
from calendar_sets s
join calendar_set_members m on m.set_id = s.set_id
join calendar_definitions d on d.calendar_id = m.calendar_id;

-- count overlays by tenant
select tenant_id, count(*) from tenant_calendar_overlays group by 1;

-- fiscal coverage
select fiscal_id, min(starts_on), max(ends_on), count(*) periods
from fiscal_periods group by 1;
```

## Migration notes
- Keep calendar sets stable and prefer additive changes
- Store overlays per tenant and avoid rewriting history
- Precompute period tables for fiscal calendars if range queries are heavy
