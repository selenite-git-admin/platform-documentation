# Health Data Model

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Persist health signals for services and datasets so operators can audit readiness, trend availability, and correlate incidents over time. Although real-time health flows through metrics and traces, a compact relational schema provides durable history and cross-service rollups.

## Design goals
- Append-only event logs; no rewrites on the hot path
- Compact payloads with stable enums
- Queryable by service, check, and time without full-table scans
- Clean separation of **service health** and **data health**
- No tenant identifiers; this is platform-scoped

## Entity Relationships

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/health/health-erd.svg" alt="Platform Overview">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/health/health-erd.svg" alt="Platform Overview">
</div>

_Figure 2: Health Service ERD_{.figure-caption}


## Entity overview
- `health_check_log` — results of `/readyz`, `/startupz`, and internal dependency probes
- `data_health_log` — dataset freshness and schema validity snapshots
- `health_sla_violation` — normalized SLO breach events for alert forensics
- `health_aggregator_state` — cached rollups for fleet dashboards (optional but useful)
- `health_daily_aggregate` — precomputed counts and latency summaries for trends

> ERD: generate in dbdiagram.io and save to `assets/diagrams/health/health-erd.svg`

## Table definitions

### health_check_log
One row per probe execution.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| service_name | text | logical name, e.g., `notifications`, `schema-registry` |
| environment | text | `prod`, `staging`, etc. |
| probe | text | `readyz`, `startupz`, `liveness`, `dependency` |
| check_name | text | dependency id (`db`, `secrets`, `queue`) or `overall` |
| status | text | `ok`, `degraded`, `fail` |
| latency_ms | integer | probe duration |
| region | text | e.g., `ap-south-1` |
| version | text | deployed version or image tag |
| correlation_id | uuid | trace key if available |
| hint | text | short non-sensitive message |
| ts | timestamptz | probe timestamp |

Indexes:
- `(service_name, ts desc)`
- `(probe, status, ts desc)`
- `(service_name, check_name, ts desc)`

### data_health_log
Freshness and validation snapshot for a dataset owned by a service.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| service_name | text | owning module |
| environment | text |  |
| dataset_name | text | public identifier, e.g., `gdp_store.ingest` |
| status | text | `ok`, `late`, `missing`, `invalid` |
| as_of | timestamptz | data timestamp the service is advertising |
| lag_minutes | integer | derived at write time |
| validator_version | text | schema validator or rule pack id |
| evidence_ref | text | optional Evidence Ledger id |
| region | text |  |
| correlation_id | uuid | if tied to a run |
| ts | timestamptz | probe timestamp |

Indexes:
- `(dataset_name, ts desc)`
- `(service_name, status, ts desc)`

### health_sla_violation
Normalized record when an SLO burn policy opens.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| service_name | text |  |
| environment | text |  |
| slo | text | `availability`, `ready_latency_p95`, `freshness` |
| window | text | e.g., `5m`, `1h` |
| actual | numeric | measured value |
| target | numeric | objective |
| state | text | `open`, `ack`, `closed` |
| opened_at | timestamptz |  |
| closed_at | timestamptz | nullable |
| region | text |  |
| incident_id | text | link to incident tracker |

Indexes:
- `(service_name, state, opened_at desc)`
- `(slo, opened_at desc)`

### health_aggregator_state
Optional cache for fleet rollups. Updated by a scheduled job.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| environment | text |  |
| region | text |  |
| snapshot_ts | timestamptz | rollup time |
| payload | jsonb | compact per-service status array |
| source_count | integer | number of services aggregated |

Index: `(snapshot_ts desc)`

### health_daily_aggregate
Precomputed metrics for dashboards.

| Column | Type | Notes |
|---|---|---|
| day | date pk |  |
| service_name | text pk |  |
| environment | text pk |  |
| region | text pk |  |
| ready_failures | bigint | count of failing `/readyz` checks |
| ready_slow_p95_ms | integer | p95 of readiness latency |
| uptime_minutes | integer | minutes with `ok` overall |
| datasets_late | bigint | count of late data_health entries |
| violations_opened | bigint | SLO breach count |

Primary key `(day, service_name, environment, region)`.

## PostgreSQL DDL

```sql
create table if not exists health_check_log (
  id uuid primary key,
  service_name text not null,
  environment text not null,
  probe text not null,
  check_name text not null,
  status text not null,
  latency_ms integer not null,
  region text not null,
  version text,
  correlation_id uuid,
  hint text,
  ts timestamptz not null default now()
);

create index if not exists hcl_service_ts_idx on health_check_log (service_name, ts desc);
create index if not exists hcl_probe_status_ts_idx on health_check_log (probe, status, ts desc);
create index if not exists hcl_service_check_ts_idx on health_check_log (service_name, check_name, ts desc);

create table if not exists data_health_log (
  id uuid primary key,
  service_name text not null,
  environment text not null,
  dataset_name text not null,
  status text not null,
  as_of timestamptz,
  lag_minutes integer,
  validator_version text,
  evidence_ref text,
  region text not null,
  correlation_id uuid,
  ts timestamptz not null default now()
);

create index if not exists dhl_dataset_ts_idx on data_health_log (dataset_name, ts desc);
create index if not exists dhl_service_status_ts_idx on data_health_log (service_name, status, ts desc);

create table if not exists health_sla_violation (
  id uuid primary key,
  service_name text not null,
  environment text not null,
  slo text not null,
  window text not null,
  actual numeric not null,
  target numeric not null,
  state text not null,
  opened_at timestamptz not null,
  closed_at timestamptz,
  region text not null,
  incident_id text
);

create index if not exists hsv_service_state_opened_idx on health_sla_violation (service_name, state, opened_at desc);
create index if not exists hsv_slo_opened_idx on health_sla_violation (slo, opened_at desc);

create table if not exists health_aggregator_state (
  id uuid primary key,
  environment text not null,
  region text not null,
  snapshot_ts timestamptz not null,
  payload jsonb not null,
  source_count integer not null default 0
);

create index if not exists has_snapshot_idx on health_aggregator_state (snapshot_ts desc);

create table if not exists health_daily_aggregate (
  day date not null,
  service_name text not null,
  environment text not null,
  region text not null,
  ready_failures bigint not null default 0,
  ready_slow_p95_ms integer,
  uptime_minutes integer not null default 0,
  datasets_late bigint not null default 0,
  violations_opened bigint not null default 0,
  primary key (day, service_name, environment, region)
);
```

## DBML

```dbml
Project Health { database_type: "PostgreSQL" }

Table health_check_log {
  id uuid [pk]
  service_name text
  environment text
  probe text
  check_name text
  status text
  latency_ms int
  region text
  version text
  correlation_id uuid
  hint text
  ts timestamptz
}

Table data_health_log {
  id uuid [pk]
  service_name text
  environment text
  dataset_name text
  status text
  as_of timestamptz
  lag_minutes int
  validator_version text
  evidence_ref text
  region text
  correlation_id uuid
  ts timestamptz
}

Table health_sla_violation {
  id uuid [pk]
  service_name text
  environment text
  slo text
  window text
  actual numeric
  target numeric
  state text
  opened_at timestamptz
  closed_at timestamptz
  region text
  incident_id text
}

Table health_aggregator_state {
  id uuid [pk]
  environment text
  region text
  snapshot_ts timestamptz
  payload jsonb
  source_count int
}

Table health_daily_aggregate {
  day date
  service_name text
  environment text
  region text
  ready_failures bigint
  ready_slow_p95_ms int
  uptime_minutes int
  datasets_late bigint
  violations_opened bigint
  indexes { (day, service_name, environment, region) [pk] }
}
```

## Query patterns

Recent readiness failures
```sql
select service_name, check_name, hint, ts
from health_check_log
where status = 'fail' and ts > now() - interval '1 hour'
order by ts desc;
```

Late datasets last 24h
```sql
select dataset_name, count(*) as late_count
from data_health_log
where status = 'late' and ts > now() - interval '24 hours'
group by dataset_name
order by late_count desc;
```

SLA violations currently open
```sql
select service_name, slo, window, actual, target, opened_at
from health_sla_violation
where state = 'open'
order by opened_at desc;
```

## Retention
- `health_check_log`: 30 days hot; archive or summarize afterward
- `data_health_log`: 30–90 days depending on volume
- `health_sla_violation`: 1 year for audit
- `health_daily_aggregate`: 2 years for trends
- Regional retention follows Store Policies

## Operational notes
- Inserts only on hot logs; aggregates populated via scheduled jobs
- Consider monthly partitions on `*_log` tables when volume is high
- Avoid storing stack traces or secrets; keep `hint` short
- Use the same `correlation_id` that flows through traces for easy pivots

## Summary
This schema keeps health signals small, fast to write, and easy to analyze. It complements real-time metrics and traces with durable records for audits, fleet rollups, and long-horizon trends without leaking tenant data.