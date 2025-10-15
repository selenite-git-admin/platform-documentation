# SCD SQL Templates (PostgreSQL)

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

> Replace placeholders before use:
> - `{{schema}}` target schema, default `kpi` or `gdp`
> - `{{entity}}` entity name, e.g., `customer`
> - `{{staging}}` staging table name, e.g., `stg_customer_delta`
> - `{{key_cols}}` comma separated list of natural key columns (if composite, set `business_key` as concatenation in staging)
> - `{{attr_cols}}` comma separated list of tracked attribute columns (exclude audit columns)
> - `{{asof_ts}}` timestamp for point in time reads

## Utility: Hash function
Use md5 over a stable concat of attribute values. Nulls coalesced to a marker.

```sql
-- Computes md5 over selected columns
create or replace function {{schema}}.hash_row({{attr_cols}}) returns text language sql immutable as $$
  select md5(concat_ws('||', {{attr_cols}}));
$$;
```

## SCD1: Table and merge

```sql
-- Table
create table if not exists {{schema}}.dim_{{entity}}_s1 (
  business_key text primary key,
  -- attributes
  {{attr_cols}},
  scd_hash text not null,
  last_updated_at timestamptz not null default now()
);

create index if not exists dim_{{entity}}_s1_hash_idx on {{schema}}.dim_{{entity}}_s1 (scd_hash);
```

```sql
-- Merge from staging with change detection
-- Staging must provide: business_key, {{attr_cols}}
with incoming as (
  select s.business_key,
         s.{{attr_cols}},
         {{schema}}.hash_row(s.{{attr_cols}}) as scd_hash
  from {{schema}}.{{staging}} s
),
changed as (
  select i.*
  from incoming i
  left join {{schema}}.dim_{{entity}}_s1 d using (business_key)
  where d.business_key is null or d.scd_hash <> i.scd_hash
)
insert into {{schema}}.dim_{{entity}}_s1 (business_key, {{attr_cols}}, scd_hash, last_updated_at)
select business_key, {{attr_cols}}, scd_hash, now() from changed
on conflict (business_key) do update
set {{ ', '.join([f'{col}=excluded.{col}' for col in ['scd_hash']]) }},  -- keep scd_hash
    {attr_updates},
    last_updated_at = excluded.last_updated_at;
```

> Replace `{attr_updates}` with assignments for each attribute column, e.g. `name=excluded.name, city=excluded.city`.

## SCD2: Table, constraints, triggers, views, merge

```sql
-- Table
create table if not exists {{schema}}.dim_{{entity}} (
  dim_id bigserial primary key,
  business_key text not null,
  -- attributes
  {{attr_cols}},
  scd_hash text not null,
  valid_from timestamptz not null,
  valid_to timestamptz not null default '9999-12-31',
  is_current boolean not null default true,
  last_updated_at timestamptz not null default now(),
  unique (business_key, valid_from)
);

create index if not exists dim_{{entity}}_bk_current_idx on {{schema}}.dim_{{entity}} (business_key) where is_current;
create index if not exists dim_{{entity}}_valid_idx on {{schema}}.dim_{{entity}} (business_key, valid_from, valid_to);
create index if not exists dim_{{entity}}_hash_idx on {{schema}}.dim_{{entity}} (scd_hash);
```

```sql
-- Prevent overlapping ranges for the same business_key
create or replace function {{schema}}.dim_{{entity}}_no_overlap() returns trigger language plpgsql as $$
begin
  if new.valid_from >= new.valid_to then
    raise exception 'valid_from must be < valid_to';
  end if;
  if exists (
    select 1
    from {{schema}}.dim_{{entity}} d
    where d.business_key = new.business_key
      and tstzrange(d.valid_from, d.valid_to) && tstzrange(new.valid_from, new.valid_to)
      and (tg_op <> 'UPDATE' or d.dim_id <> old.dim_id)
  ) then
    raise exception 'overlapping validity for business_key %', new.business_key;
  end if;
  return new;
end;
$$;

drop trigger if exists trg_dim_{{entity}}_no_overlap on {{schema}}.dim_{{entity}};
create trigger trg_dim_{{entity}}_no_overlap
before insert or update on {{schema}}.dim_{{entity}}
for each row execute function {{schema}}.dim_{{entity}}_no_overlap();
```

```sql
-- Current view
create or replace view {{schema}}.vw_dim_{{entity}}_current as
select *
from {{schema}}.dim_{{entity}}
where is_current = true;

-- As-of helper (point-in-time)
create or replace view {{schema}}.vw_dim_{{entity}}_asof as
select *
from {{schema}}.dim_{{entity}} d
where d.valid_from <= now() and now() < d.valid_to;
```

```sql
-- Merge for SCD2 using staging
-- Staging must provide: business_key, {{attr_cols}}, event_ts (as candidate valid_from)
with incoming as (
  select s.business_key,
         s.{{attr_cols}},
         coalesce(s.event_ts, now()) as valid_from,
         {{schema}}.hash_row(s.{{attr_cols}}) as scd_hash
  from {{schema}}.{{staging}} s
),
joined as (
  select i.*, d.dim_id, d.scd_hash as curr_hash, d.valid_from as curr_from, d.valid_to as curr_to
  from incoming i
  left join {{schema}}.dim_{{entity}} d
    on d.business_key = i.business_key and d.is_current = true
),
to_close as (
  -- rows where value changed or not present; close current if exists and hash differs
  select j.* from joined j
  where j.curr_hash is not null and j.curr_hash <> j.scd_hash
),
closed as (
  update {{schema}}.dim_{{entity}} d
  set valid_to = (select greatest(j.valid_from, d.valid_from) from to_close j where j.dim_id = d.dim_id),
      is_current = false,
      last_updated_at = now()
  where d.dim_id in (select dim_id from to_close)
  returning d.business_key
),
to_insert as (
  -- new keys or changed values become new current rows
  select j.business_key, j.valid_from, j.scd_hash, j.{{attr_cols}}
  from joined j
  where j.curr_hash is null or j.curr_hash <> j.scd_hash
)
insert into {{schema}}.dim_{{entity}} (
  business_key, {{attr_cols}}, scd_hash, valid_from, valid_to, is_current, last_updated_at
)
select business_key, {{attr_cols}}, scd_hash, valid_from, '9999-12-31', true, now()
from to_insert
on conflict (business_key, valid_from) do nothing;
```

## Idempotency pattern
- Ensure staging only contains the latest delta for this batch.
- Repeatable runs will not duplicate rows due to `(business_key, valid_from)` uniqueness and hash checks.
- Wrap merge in `begin; ... commit;` with `set transaction isolation level serializable;` and retry on code `40001`.

## Validation queries

```sql
-- Overlap check should return zero rows
select business_key, count(*) as segs
from {{schema}}.dim_{{entity}}
group by business_key
having count(*) <> count(distinct tstzrange(valid_from, valid_to));

-- Current rows have open-ended valid_to
select count(*) from {{schema}}.dim_{{entity}} where is_current and valid_to <> '9999-12-31'::timestamptz;

-- No duplicate current rows per business_key
select business_key
from {{schema}}.dim_{{entity}}
where is_current
group by business_key
having count(*) > 1;
```