# SCD Validation and QA

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
Operational checklist and SQL snippets to validate SCD1/SCD2 correctness in PostgreSQL. Use after initial setup and on each pipeline change.

## Preconditions
- Staging tables loaded with latest delta
- Dimension tables created via templates in `scd_sql_templates.md`
- DRR reporting enabled for affected datasets

## Smoke Checks
### Row counts
```sql
-- Expect non-zero current rows
select count(*) as current_rows
from {{schema}}.dim_{{entity}}
where is_current = true;
```

### Key coverage
```sql
-- Every business_key must have at least one row
select business_key
from {{schema}}.dim_{{entity}}
group by business_key
having count(*) = 0;  -- expect zero rows returned
```

## Integrity Checks (SCD2)
### Non-overlapping validity
```sql
-- No overlapping ranges per key
select business_key
from (
  select business_key,
         tstzrange(valid_from, valid_to) as r
  from {{schema}}.dim_{{entity}}
) s
group by business_key
having count(*) <> count(distinct r);
```

### Single current row per key
```sql
select business_key
from {{schema}}.dim_{{entity}}
where is_current
group by business_key
having count(*) > 1;  -- expect zero
```

### Open-ended current intervals
```sql
select count(*) as not_open_ended
from {{schema}}.dim_{{entity}}
where is_current and valid_to <> '9999-12-31'::timestamptz;  -- expect 0
```

### Change detection sanity
```sql
-- Current and previous hash for changed keys
with c as (
  select business_key, scd_hash, valid_from,
         lag(scd_hash) over (partition by business_key order by valid_from) as prev_hash
  from {{schema}}.dim_{{entity}}
)
select * from c
where prev_hash is not null and prev_hash = scd_hash;  -- expect zero
```

## Point-in-Time (PIT) Checks
### As-of query matches current when time is now
```sql
select count(*) as diff
from {{schema}}.vw_dim_{{entity}}_current c
full outer join {{schema}}.vw_dim_{{entity}}_asof a
  on c.business_key = a.business_key
where (c.scd_hash is distinct from a.scd_hash);  -- expect 0
```

### As-of consistency for sample timestamp
```sql
-- replace {{asof_ts}} with a historic timestamp that is mid-interval
select *
from {{schema}}.dim_{{entity}}
where business_key = '{{sample_key}}'
  and valid_from <= '{{asof_ts}}'::timestamptz
  and '{{asof_ts}}'::timestamptz < valid_to;
```

## Performance Checks
```sql
-- Index usage on validity lookup
explain analyze
select *
from {{schema}}.dim_{{entity}}
where business_key = '{{sample_key}}'
  and valid_from <= now()
  and now() < valid_to;
```

## Common Pitfalls
- **Staging duplicates:** ensure one row per business_key per batch; dedupe upstream.
- **Clock skew:** prefer event time (`event_ts`) for `valid_from`; default to `now()` only when missing.
- **Hash drift:** include all tracked attributes in `scd_hash`; avoid non-deterministic formatting.
- **Late-arriving data:** merging with older `valid_from` can cause overlaps; trigger prevents it.
- **Timezone mismatches:** standardize to UTC; store timestamps as `timestamptz`.
- **Multi-source joins:** create a canonical business_key; avoid concatenation ambiguity.
- **Deletes:** represent logical deletes with a terminal row (set a `deleted = true` attribute) instead of hard deletes.

## QA Exit Criteria
- All integrity and PIT checks return zero diffs.
- Merge job emits audit and DRR shows updated freshness.
- p95 PIT queries < 100 ms on indexed sample.
- No overlaps detected after at least two change batches.

## Ownership
- Store: validation queries and table constraints
- Runtime: merge execution and retries
- Governance: acceptance of QA results and retention policy