# Notifications Data Model

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Represent notifications as immutable requests with per‑channel delivery attempts, while keeping templates, destinations, and policy separate. Optimized for append‑only writes, fast status reads, and privacy safety in PostgreSQL.

## Design Goals
- Append‑only core tables with clear lineage from request → attempts → provider outcomes
- Tenant‑safe by default: redact variables at rest, store only what is needed to render and support
- Efficient read paths for status and dashboards without scanning hot tables
- Versioned templates and localizable content
- Idempotent writes using client‑supplied keys and server correlation ids

## Entities

### template
Canonical logical template id.

| Column | Type | Notes |
|---|---|---|
| id | text pk | stable key such as `password-reset` |
| name | text | human readable |
| description | text | authoring note |
| created_at | timestamptz | registry timestamp |
| updated_at | timestamptz | last change |

### template_version

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/notifications/notifications-erd.svg" alt="Platform Overview">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/notifications/notifications-erd.svg" alt="Platform Overview">
</div>

_Figure 2: Notifications ERD_{.figure-caption}

### template
Canonical logical template id.

| Column | Type | Notes |
|---|---|---|
| id | text pk | stable key such as `password-reset` |
| name | text | human readable |
| description | text | authoring note |
| created_at | timestamptz | registry timestamp |
| updated_at | timestamptz | last change |

### template_version
Versioned, localized content and schema.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| template_id | text fk | → template.id |
| locale | text | e.g. `en-US` |
| subject | text | for email |
| body_html | text | nullable |
| body_text | text | required fallback |
| variables_schema | jsonb | JSON Schema for variables |
| policy | jsonb | flags: priority, rate limits, retention |
| is_active | boolean | only one per locale active |
| created_at | timestamptz |  |

### destination
Tenant‑level channel configuration (masked).

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| tenant_id | uuid | hashed or tokenized if required |
| channel | text | `email`, `slack`, `webhook`, `inapp` |
| config | jsonb | masked settings; secrets not stored here |
| verified | boolean | true if provider/domain verified |
| created_at | timestamptz |  |
| updated_at | timestamptz |  |

### suppression
Bounce, complaint, or tenant opt‑out rules.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| tenant_id | uuid |  |
| channel | text |  |
| target | text | email address, slack channel id, webhook id, or `user:{uuid}` |
| reason | text | `bounce`, `complaint`, `optout`, `manual` |
| expires_at | timestamptz | nullable for permanent |
| created_at | timestamptz |  |

### notification_request
Immutable record created by API.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| tenant_id | uuid | cohort joins |
| template_id | text | logical template |
| template_version_id | uuid | pinned version at render time |
| variables | jsonb | minimal, redacted copy used for rendering and support |
| channels | jsonb | array of channels requested |
| to | jsonb | array of recipients (user ids, system URLs) |
| priority | text | `normal` or `high` |
| schedule_at | timestamptz | nullable |
| idempotency_key | text | unique per tenant per 24h |
| correlation_id | uuid | trace key |
| created_at | timestamptz |  |
| status | text | derived: `queued` `partially_delivered` `delivered` `failed` |

### notification_attempt
One row per channel fan‑out attempt.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| request_id | uuid fk | → notification_request.id |
| channel | text |  |
| state | text | `pending` `delivered` `failed` `dead_lettered` |
| retry_count | int |  |
| provider_message_id | text | nullable |
| last_error_code | text | canonical error code if failed |
| last_error_details | jsonb | redacted |
| first_attempt_at | timestamptz |  |
| last_attempt_at | timestamptz |  |
| delivered_at | timestamptz | nullable |

### webhook_endpoint
Registered webhook destinations owned by the tenant.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| tenant_id | uuid |  |
| name | text |  |
| url | text | https url |
| secret_hint | text | non‑secret hint only |
| enabled | boolean |  |
| created_at | timestamptz |  |
| updated_at | timestamptz |  |

### notification_aggregate_daily
Rollups for dashboards.

| Column | Type | Notes |
|---|---|---|
| day | date |  |
| tenant_id | uuid |  |
| template_id | text |  |
| channel | text |  |
| delivered | bigint | count |
| failed | bigint | count |
| bounced | bigint | count |
| latency_p95_ms | int | optional |

## DDL

```sql
create table if not exists template (
  id text primary key,
  name text not null,
  description text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists template_version (
  id uuid primary key,
  template_id text not null references template(id),
  locale text not null,
  subject text,
  body_html text,
  body_text text not null,
  variables_schema jsonb not null,
  policy jsonb not null default '{}'::jsonb,
  is_active boolean not null default false,
  created_at timestamptz not null default now()
);

create unique index if not exists template_version_active_locale_idx
  on template_version (template_id, locale) where is_active;

create table if not exists destination (
  id uuid primary key,
  tenant_id uuid not null,
  channel text not null,
  config jsonb not null,
  verified boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists suppression (
  id uuid primary key,
  tenant_id uuid not null,
  channel text not null,
  target text not null,
  reason text not null,
  expires_at timestamptz,
  created_at timestamptz not null default now()
);

create unique index if not exists suppression_unique_idx
  on suppression (tenant_id, channel, target) where expires_at is null;

create table if not exists notification_request (
  id uuid primary key,
  tenant_id uuid not null,
  template_id text not null,
  template_version_id uuid not null references template_version(id),
  variables jsonb not null,
  channels jsonb not null,
  to jsonb not null,
  priority text not null default 'normal',
  schedule_at timestamptz,
  idempotency_key text,
  correlation_id uuid not null,
  created_at timestamptz not null default now(),
  status text not null default 'queued'
);

create unique index if not exists notification_idem_idx
  on notification_request (tenant_id, idempotency_key)
  where idempotency_key is not null;

create index if not exists notification_request_tenant_cts_idx
  on notification_request (tenant_id, created_at);

create table if not exists notification_attempt (
  id uuid primary key,
  request_id uuid not null references notification_request(id),
  channel text not null,
  state text not null default 'pending',
  retry_count int not null default 0,
  provider_message_id text,
  last_error_code text,
  last_error_details jsonb,
  first_attempt_at timestamptz,
  last_attempt_at timestamptz,
  delivered_at timestamptz
);

create index if not exists notification_attempt_req_idx
  on notification_attempt (request_id);

create index if not exists notification_attempt_state_idx
  on notification_attempt (state, channel);

create table if not exists webhook_endpoint (
  id uuid primary key,
  tenant_id uuid not null,
  name text not null,
  url text not null,
  secret_hint text,
  enabled boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists notification_aggregate_daily (
  day date not null,
  tenant_id uuid not null,
  template_id text not null,
  channel text not null,
  delivered bigint not null default 0,
  failed bigint not null default 0,
  bounced bigint not null default 0,
  latency_p95_ms int,
  primary key (day, tenant_id, template_id, channel)
);
```

## DBML
```dbml
Project Notifications { database_type: "PostgreSQL" }

Table template {
  id text [pk]
  name text
  description text
  created_at timestamptz
  updated_at timestamptz
}

Table template_version {
  id uuid [pk]
  template_id text [ref: > template.id]
  locale text
  subject text
  body_html text
  body_text text
  variables_schema jsonb
  policy jsonb
  is_active boolean
  created_at timestamptz
}

Table destination {
  id uuid [pk]
  tenant_id uuid
  channel text
  config jsonb
  verified boolean
  created_at timestamptz
  updated_at timestamptz
}

Table suppression {
  id uuid [pk]
  tenant_id uuid
  channel text
  target text
  reason text
  expires_at timestamptz
  created_at timestamptz
}

Table notification_request {
  id uuid [pk]
  tenant_id uuid
  template_id text
  template_version_id uuid [ref: > template_version.id]
  variables jsonb
  channels jsonb
  to jsonb
  priority text
  schedule_at timestamptz
  idempotency_key text
  correlation_id uuid
  created_at timestamptz
  status text
}

Table notification_attempt {
  id uuid [pk]
  request_id uuid [ref: > notification_request.id]
  channel text
  state text
  retry_count int
  provider_message_id text
  last_error_code text
  last_error_details jsonb
  first_attempt_at timestamptz
  last_attempt_at timestamptz
  delivered_at timestamptz
}

Table webhook_endpoint {
  id uuid [pk]
  tenant_id uuid
  name text
  url text
  secret_hint text
  enabled boolean
  created_at timestamptz
  updated_at timestamptz
}

Table notification_aggregate_daily {
  day date
  tenant_id uuid
  template_id text
  channel text
  delivered bigint
  failed bigint
  bounced bigint
  latency_p95_ms int
  indexes { (day, tenant_id, template_id, channel) [pk] }
}
```

## Privacy and Redaction
- Variables stored at rest must be redacted and limited to what support needs to diagnose issues. Do not store email bodies or full webhook payloads.
- Secrets live in the Secrets module, referenced by handle only. Destination `config` is masked.
- Suppression targets may contain PII (emails). Restrict reads by role and tenant.

## Retention
- `notification_request` and `notification_attempt`: 90 days hot, then archive or purge per Store Policies.
- `notification_aggregate_daily`: 2 years for trends.
- `suppression`: until `expires_at` or manual clear.
- `template_version`: keep all versions; mark inactive when superseded.

## Query Patterns

Latest status for a request
```sql
select nr.id, nr.status, na.channel, na.state, na.retry_count, na.delivered_at
from notification_request nr
left join lateral (
  select channel, state, retry_count, delivered_at
  from notification_attempt a
  where a.request_id = nr.id
) na on true
where nr.id = $1;
```

Top failing templates last 7 days
```sql
select template_id, channel, count(*) as failures
from notification_attempt a
join notification_request r on r.id = a.request_id
where a.state = 'failed' and r.created_at >= now() - interval '7 days'
group by template_id, channel
order by failures desc;
```

Bounce rate by tenant
```sql
select tenant_id,
       sum(case when a.last_error_code = 'bounce' then 1 else 0 end)::bigint as bounces,
       count(*)::bigint as sent
from notification_attempt a
join notification_request r on r.id = a.request_id
where a.channel = 'email' and r.created_at >= now() - interval '30 days'
group by tenant_id;
```

## Operational Notes
- Upserts only for metadata tables; core flows are insert‑only.
- Populate aggregates via daily job.
- Consider monthly partitions for `notification_request` and `notification_attempt` if volume is high.
- Enforce idempotency in `notification_request` writer using the unique index.

## Summary
This schema cleanly separates authoring (templates), configuration (destinations, suppression), and execution (requests, attempts), while keeping the hot path append‑only and privacy‑safe. It supports efficient status queries, reliable audit trails, and scalable rollups without introducing new infrastructure.