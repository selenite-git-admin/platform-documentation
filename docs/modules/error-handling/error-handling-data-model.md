# Error Handling Data Model

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Persist a minimal, privacy-safe record of platform errors for trend analysis, SLO reporting, and forensics. The model complements observability metrics by enabling ad‑hoc queries, cohort analysis, and correlation with DRR/Evidence Ledger. It is PostgreSQL‑native and optimized for append‑only writes and time‑range reads.

## Design Goals
- Append‑only, immutable facts (no updates in the hot path)
- Tenant‑safe: no sensitive payloads stored
- Efficient time + code filtering
- Easy joins with service catalog and DRR data
- Works in serverless and containerized runners

## Non‑Goals
- Storing full request/response bodies
- Per‑request high cardinality attributes beyond a small, governed set
- Replacing metrics (this complements dashboards; it does not duplicate them)

## Entities

### Entity Relationships

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/error-handling/error-handling-erd.svg" alt="Platform Overview">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/error-handling/error-handling-erd.svg" alt="Platform Overview">
</div>

_Figure 1: Error Handling ERD_{.figure-caption}

### error_code
Canonical registry of symbolic error codes and domains.

| Column | Type | Notes |
|--------|------|------|
| code | text primary key | stable code (`validation_failed`, `stale_read`, etc.) |
| domain | text | request, auth, resource, rate, runtime, data |
| description | text | human‑readable summary |
| retryable | boolean | recommended retry behavior |
| http_status | int | default mapping for REST |
| created_at | timestamptz | registry timestamp |
| updated_at | timestamptz | last change |

### error_event
Immutable record of a client‑visible or job‑visible error.

| Column | Type | Notes |
|--------|------|------|
| event_id | uuid primary key | UUIDv7 |
| code | text | fk → error_code.code |
| correlation_id | uuid | end‑to‑end trace id |
| service | text | logical service or job name |
| endpoint | text | optional route or operation |
| http_status | int | when applicable |
| tenant_hash | text | sha256 of tenant_id (avoid plaintext) |
| details | jsonb | redacted, small map of keys (see governance) |
| region | text | deployment region identifier |
| ts | timestamptz | event time |
| day | date | partition key helper (generated column) |

### error_aggregate_daily
Rollup to power dashboards without scanning the event table.

| Column | Type | Notes |
|--------|------|------|
| day | date | primary key with service/code group |
| service | text | dimension |
| code | text | dimension |
| count | bigint | events that day |
| retryable_count | bigint | subset with retryable=true |
| last_seen_at | timestamptz | latest ts for the group |

## DDL (PostgreSQL)
```sql
create table if not exists error_code (
  code text primary key,
  domain text not null,
  description text not null,
  retryable boolean not null default false,
  http_status int,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists error_event (
  event_id uuid primary key,
  code text not null references error_code(code),
  correlation_id uuid not null,
  service text not null,
  endpoint text,
  http_status int,
  tenant_hash text,
  details jsonb,
  region text,
  ts timestamptz not null default now(),
  day date generated always as (date_trunc('day', ts)::date) stored
);

create index if not exists error_event_code_day_idx on error_event (code, day);
create index if not exists error_event_service_day_idx on error_event (service, day);
create index if not exists error_event_ts_idx on error_event (ts);
create index if not exists error_event_retryable_idx on error_event ((details->>'retryable'));
```

## Governance of `details`
Keep `details` small and predictable. Allowed keys:
- `retryable` (bool)
- `field` (string) — safe input label only
- `limit` (int), `window_sec` (int) — for `rate_limited`
- `expected_etag` (string) — short hash value only
- `existing_id` (uuid) — for `already_exists` / `conflict`

Prohibited: raw request bodies, PII, secrets, token strings, SQL, stack traces.

## Ingest Pattern
- Errors emitted by gateway/services via a thin async writer (batch insert).
- Writers must drop oversized `details` or keys outside the allow‑list.
- On backpressure, prefer lossy metrics over blocking request paths; events are best‑effort complements.

## Query Patterns
### Top errors last 24h
```sql
select code, count(*) as c
from error_event
where ts > now() - interval '24 hours'
group by code
order by c desc;
```

### Retryable failure rate by service
```sql
select service,
       sum( (details->>'retryable')::bool::int )::bigint as retryable,
       count(*)::bigint as total,
       round(100.0 * sum( (details->>'retryable')::bool::int ) / nullif(count(*),0), 2) as pct
from error_event
where day >= current_date - 7
group by service
order by pct desc;
```

### Drill into a customer case using correlation id
```sql
select *
from error_event
where correlation_id = '01JAH8ZJ0Z8Z0N7M1X6JZ8QW0T'
order by ts;
```

## DBML
```dbml
Project ErrorHandling { database_type: "PostgreSQL" }

Table error_code as EC {
  code text [pk]
  domain text
  description text
  retryable boolean
  http_status int
  created_at timestamptz
  updated_at timestamptz
}

Table error_event as EE {
  event_id uuid [pk]
  code text [ref: > EC.code]
  correlation_id uuid
  service text
  endpoint text
  http_status int
  tenant_hash text
  details jsonb
  region text
  ts timestamptz
  day date
}

Table error_aggregate_daily as EAD {
  day date
  service text
  code text
  count bigint
  retryable_count bigint
  last_seen_at timestamptz
}

Ref: EC.code < EE.code
```

## Partitions (optional)
For very high volume, partition `error_event` by `day`:
```sql
create table if not exists error_event_y2025m10 partition of error_event
for values from ('2025-10-01') to ('2025-11-01');
```
Rotate monthly and vacuum analyze after bulk loads.

## Security & Privacy
- Store `tenant_hash` instead of plaintext tenant id (HMAC with platform key).
- Redact values in `details` at the writer.
- Row‑level security can restrict reads by service or team if needed.
- Audit export jobs must include only aggregated counts unless explicitly authorized.

## Integration
- Join to service catalog for ownership reporting.
- Join to DRR to correlate freshness incidents with error spikes.
- Evidence Ledger remains the system of record for write attempts; use `correlation_id` to stitch stories across systems.

## Operational Notes
- Vacuum `error_event` weekly (or per partition).
- Daily rollup job populates `error_aggregate_daily`.
- Retention: 90 days for `error_event`, 2 years for aggregates (configurable via Store Policies).
- Backfills should run in off‑peak windows and disable triggers.

## Summary
A compact, governed schema that captures just enough about failures to be useful, without risking data leakage or operational drag. It scales linearly, plays well with DRR/Evidence Ledger, and keeps analysis simple and fast.