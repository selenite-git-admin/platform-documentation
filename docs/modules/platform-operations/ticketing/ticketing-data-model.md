# Ticketing Data Model

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Provide a minimal, durable schema for storing tickets, conversations, SLA timers, and links to platform resources. The model is optimized for append‑only writes, strong auditability, and efficient searches by category, state, assignee, and time. **Platform‑scoped** storage with RBAC ensures tenant privacy without per‑tenant databases.

## Design goals
- Append‑only event streams for history and comments
- Stable enums for categories, severities, and states
- Idempotent creation using client‑provided keys
- Tenant‑aware filtering with optional `tenant_id`
- `visibility` flag for platform‑only vs tenant content
- Fast list queries using composite indexes
- Attachment metadata only; binaries live in object storage

> ERD placeholder: generate in dbdiagram.io and save to `assets/diagrams/ticketing/ticketing-erd.svg`

## Entities
- **ticket** — primary work item
- **ticket_comment** — threaded conversation and system events
- **ticket_link** — relationships to datasets, connectors, jobs, incidents
- **ticket_attachment** — metadata for uploaded artifacts
- **ticket_sla_timer** — ack, first‑response, resolution clocks
- **ticket_tag** — free‑form labels
- **ticket_history** — normalized state transitions
- **sla_policy** — reusable SLA definitions by category and environment
- **routing_rule** — category/tenant → team assignment hints
- **dedup_group** — correlation‑based grouping for system incidents

## Tables

### ticket
One row per ticket.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk | UUIDv7 |
| key | text unique | Stable external key (e.g., `TCK-2025-00123`) |
| category | text | `incident`, `request` |
| subcategory | text | e.g., `health_readiness`, `schema_change` |
| severity | text | `p1`, `p2`, `p3`, `normal`, `low` |
| priority | text | optional triage priority |
| state | text | `new`, `ack`, `in_progress`, `wait_requester`, `wait_dependency`, `resolved`, `closed`, `canceled` |
| tenant_id | text nullable | null for platform‑only incidents |
| visibility | text | `platform_only`, `tenant`, `mixed` |
| title | text | short subject |
| summary | text | redacted summary suitable for UI |
| sla_policy_id | uuid fk | references `sla_policy.id` |
| requester_user_id | text | platform user id |
| assignee_user_id | text nullable | current human owner |
| assignee_team_id | text nullable | queue/team owner |
| source | text | `health`, `drr`, `runtime`, `user`, `cost`, etc. |
| source_ref | text | correlation to originating system |
| idempotency_key | text | dedupe key from client |
| correlation_id | uuid nullable | trace key |
| environment | text | `prod`, `staging` |
| region | text | e.g., `ap-south-1` |
| created_at | timestamptz |  |
| updated_at | timestamptz |  |
| due_at | timestamptz nullable | SLA target |
| closed_at | timestamptz nullable |  |

Indexes
- `(state, severity, updated_at desc)` list view
- `(tenant_id, updated_at desc)` tenant queries
- `(assignee_team_id, state, updated_at desc)` queue view
- `(assignee_user_id, state, updated_at desc)` my work
- `(category, subcategory, created_at desc)` reporting
- `(visibility, updated_at desc)` privacy filters
- `(idempotency_key)` unique
- `(key)` unique

### ticket_comment
Comments and system events. Store a redacted rendering and a visibility level.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| ticket_id | uuid fk |  |
| author_user_id | text nullable | null for system event |
| visibility | text | `platform_only`, `tenant`, `mixed` |
| body_redacted | text | stripped PII |
| body_render | text | markdown or safe HTML |
| system_event | boolean |  |
| created_at | timestamptz |  |

Index: `(ticket_id, created_at asc)`

### ticket_link
Relates a ticket to platform objects.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| ticket_id | uuid fk |  |
| target_type | text | `dataset`, `connector`, `job`, `incident`, `evidence`, `service` |
| target_ref | text | e.g., `gdp_store.ingest`, `job:orchestrator:123` |
| relation | text | `caused_by`, `blocks`, `duplicate_of`, `relates_to` |
| created_at | timestamptz |  |

Index: `(ticket_id, created_at asc)`

### ticket_attachment
Attachment metadata.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| ticket_id | uuid fk |  |
| filename | text |  |
| media_type | text |  |
| size_bytes | bigint |  |
| storage_ref | text | S3 key or object handle |
| checksum | text | SHA256 |
| created_at | timestamptz |  |

Index: `(ticket_id, created_at asc)`

### ticket_sla_timer
SLA clocks per ticket.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| ticket_id | uuid fk |  |
| kind | text | `ack`, `first_response`, `resolution` |
| start_at | timestamptz |  |
| due_at | timestamptz |  |
| breached_at | timestamptz nullable | set when violated |
| paused_at | timestamptz nullable |  |
| resumed_at | timestamptz nullable |  |

Index: `(ticket_id, kind)` unique

### ticket_tag
Lightweight labels.

| Column | Type | Notes |
|---|---|---|
| ticket_id | uuid fk |  |
| tag | text | lowercased |
Primary key: `(ticket_id, tag)`

### ticket_history
Normalized state transitions for audit.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| ticket_id | uuid fk |  |
| actor | text | user id or `system` |
| action | text | `create`, `ack`, `assign`, `comment`, `update`, `resolve`, `close`, `reopen`, `cancel` |
| from_state | text nullable |  |
| to_state | text nullable |  |
| at | timestamptz |  |
| metadata | jsonb | small envelope |

Index: `(ticket_id, at asc)`

### sla_policy
Reusable SLA definitions.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| name | text unique | e.g., `incident_p1_prod` |
| category | text |  |
| environment | text |  |
| ack_minutes | integer |  |
| first_response_minutes | integer |  |
| resolution_minutes | integer |  |
| timezone | text | IANA name |
| active | boolean |  |
| created_at | timestamptz |  |

Index: `(category, environment)`

### routing_rule
Category/tenant routing hints.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| tenant_id | text nullable |  |
| category | text |  |
| subcategory | text nullable |  |
| severity | text nullable |  |
| team_id | text | destination team |
| priority | integer | rule precedence |
| active | boolean |  |
| created_at | timestamptz |  |

Index: `(tenant_id, category, subcategory, severity, active)`

### dedup_group
Correlation group for incidents from the same cause.

| Column | Type | Notes |
|---|---|---|
| id | uuid pk |  |
| fingerprint | text unique | hash of category + subject + correlation features |
| opened_at | timestamptz |  |
| closed_at | timestamptz nullable |  |
| last_ticket_id | uuid fk | last member |
| count | integer | members |
| hint | text | short description |

Index: `(opened_at desc)`

## PostgreSQL DDL
```sql
-- enums as text for portability

create table if not exists sla_policy (
  id uuid primary key,
  name text unique not null,
  category text not null,
  environment text not null,
  ack_minutes integer not null,
  first_response_minutes integer not null,
  resolution_minutes integer not null,
  timezone text not null,
  active boolean not null default true,
  created_at timestamptz not null default now()
);
create index if not exists sla_policy_cat_env_idx on sla_policy (category, environment);

create table if not exists ticket (
  id uuid primary key,
  key text unique not null,
  category text not null,
  subcategory text not null,
  severity text not null,
  priority text,
  state text not null,
  tenant_id text,
  visibility text not null default 'tenant',
  title text not null,
  summary text not null,
  sla_policy_id uuid references sla_policy(id),
  requester_user_id text not null,
  assignee_user_id text,
  assignee_team_id text,
  source text not null,
  source_ref text,
  idempotency_key text unique not null,
  correlation_id uuid,
  environment text not null,
  region text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  due_at timestamptz,
  closed_at timestamptz
);

create index if not exists ticket_state_sev_updated_idx on ticket (state, severity, updated_at desc);
create index if not exists ticket_tenant_updated_idx on ticket (tenant_id, updated_at desc);
create index if not exists ticket_visibility_updated_idx on ticket (visibility, updated_at desc);
create index if not exists ticket_queue_idx on ticket (assignee_team_id, state, updated_at desc);
create index if not exists ticket_user_idx on ticket (assignee_user_id, state, updated_at desc);
create index if not exists ticket_cat_sub_created_idx on ticket (category, subcategory, created_at desc);

create table if not exists ticket_comment (
  id uuid primary key,
  ticket_id uuid not null references ticket(id) on delete cascade,
  author_user_id text,
  visibility text not null default 'tenant',
  body_redacted text not null,
  body_render text not null,
  system_event boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists ticket_comment_ticket_time_idx on ticket_comment (ticket_id, created_at asc);

create table if not exists ticket_link (
  id uuid primary key,
  ticket_id uuid not null references ticket(id) on delete cascade,
  target_type text not null,
  target_ref text not null,
  relation text not null,
  created_at timestamptz not null default now()
);
create index if not exists ticket_link_ticket_time_idx on ticket_link (ticket_id, created_at asc);

create table if not exists ticket_attachment (
  id uuid primary key,
  ticket_id uuid not null references ticket(id) on delete cascade,
  filename text not null,
  media_type text not null,
  size_bytes bigint not null,
  storage_ref text not null,
  checksum text not null,
  created_at timestamptz not null default now()
);
create index if not exists ticket_attachment_ticket_time_idx on ticket_attachment (ticket_id, created_at asc);

create table if not exists ticket_sla_timer (
  id uuid primary key,
  ticket_id uuid not null references ticket(id) on delete cascade,
  kind text not null,
  start_at timestamptz not null,
  due_at timestamptz not null,
  breached_at timestamptz,
  paused_at timestamptz,
  resumed_at timestamptz,
  unique (ticket_id, kind)
);

create table if not exists ticket_tag (
  ticket_id uuid not null references ticket(id) on delete cascade,
  tag text not null,
  primary key (ticket_id, tag)
);

create table if not exists ticket_history (
  id uuid primary key,
  ticket_id uuid not null references ticket(id) on delete cascade,
  actor text not null,
  action text not null,
  from_state text,
  to_state text,
  at timestamptz not null default now(),
  metadata jsonb
);
create index if not exists ticket_history_ticket_time_idx on ticket_history (ticket_id, at asc);

create table if not exists routing_rule (
  id uuid primary key,
  tenant_id text,
  category text not null,
  subcategory text,
  severity text,
  team_id text not null,
  priority integer not null default 100,
  active boolean not null default true,
  created_at timestamptz not null default now()
);
create index if not exists routing_rule_match_idx on routing_rule (tenant_id, category, subcategory, severity, active);

create table if not exists dedup_group (
  id uuid primary key,
  fingerprint text unique not null,
  opened_at timestamptz not null default now(),
  closed_at timestamptz,
  last_ticket_id uuid references ticket(id),
  count integer not null default 1,
  hint text
);
create index if not exists dedup_group_opened_idx on dedup_group (opened_at desc);
```

## DBML
```dbml
Project Ticketing { database_type: "PostgreSQL" }

Table sla_policy {
  id uuid [pk]
  name text [unique]
  category text
  environment text
  ack_minutes int
  first_response_minutes int
  resolution_minutes int
  timezone text
  active bool
  created_at timestamptz
}

Table ticket {
  id uuid [pk]
  key text [unique]
  category text
  subcategory text
  severity text
  priority text
  state text
  tenant_id text
  visibility text
  title text
  summary text
  sla_policy_id uuid
  requester_user_id text
  assignee_user_id text
  assignee_team_id text
  source text
  source_ref text
  idempotency_key text [unique]
  correlation_id uuid
  environment text
  region text
  created_at timestamptz
  updated_at timestamptz
  due_at timestamptz
  closed_at timestamptz
}

Table ticket_comment {
  id uuid [pk]
  ticket_id uuid
  author_user_id text
  visibility text
  body_redacted text
  body_render text
  system_event bool
  created_at timestamptz
}

Table ticket_link {
  id uuid [pk]
  ticket_id uuid
  target_type text
  target_ref text
  relation text
  created_at timestamptz
}

Table ticket_attachment {
  id uuid [pk]
  ticket_id uuid
  filename text
  media_type text
  size_bytes bigint
  storage_ref text
  checksum text
  created_at timestamptz
}

Table ticket_sla_timer {
  id uuid [pk]
  ticket_id uuid
  kind text
  start_at timestamptz
  due_at timestamptz
  breached_at timestamptz
  paused_at timestamptz
  resumed_at timestamptz
  indexes { (ticket_id, kind) [unique] }
}

Table ticket_tag {
  ticket_id uuid
  tag text
  indexes { (ticket_id, tag) [pk] }
}

Table ticket_history {
  id uuid [pk]
  ticket_id uuid
  actor text
  action text
  from_state text
  to_state text
  at timestamptz
  metadata jsonb
}

Table routing_rule {
  id uuid [pk]
  tenant_id text
  category text
  subcategory text
  severity text
  team_id text
  priority int
  active bool
  created_at timestamptz
}

Table dedup_group {
  id uuid [pk]
  fingerprint text [unique]
  opened_at timestamptz
  closed_at timestamptz
  last_ticket_id uuid
  count int
  hint text
}

Ref: ticket.sla_policy_id > sla_policy.id
Ref: ticket_comment.ticket_id > ticket.id
Ref: ticket_link.ticket_id > ticket.id
Ref: ticket_attachment.ticket_id > ticket.id
Ref: ticket_sla_timer.ticket_id > ticket.id
Ref: ticket_tag.ticket_id > ticket.id
Ref: ticket_history.ticket_id > ticket.id
Ref: dedup_group.last_ticket_id > ticket.id
```

## Query patterns

Open incidents for on‑call
```sql
select id, key, severity, title, updated_at
from ticket
where category = 'incident' and state in ('new','ack','in_progress')
and environment = 'prod' and assignee_team_id = 'oncall'
order by severity asc, updated_at desc
limit 50;
```

Tickets nearing breach
```sql
select t.id, t.key, s.kind, s.due_at
from ticket t
join ticket_sla_timer s on s.ticket_id = t.id
where t.state in ('new','ack','in_progress')
and s.breached_at is null
and s.due_at < now() + interval '30 minutes'
order by s.due_at asc;
```

Group duplicates
```sql
select fingerprint, count, last_ticket_id
from dedup_group
where closed_at is null
order by count desc
limit 20;
```

## Retention
- Tickets and comments kept 24 months
- Attachments 180 days unless evidence; evidence references live in the Ledger
- History and timers retained 24 months for audit

## Notes
- Use UUIDv7 for time‑ordered keys
- Keep `summary` and `body_redacted` safe for multi‑tenant UI
- Consider table partitioning by month for `ticket_comment` and `ticket_history` at high volume

## Summary
A platform‑scoped schema with RBAC and query scoping preserves tenant privacy while enabling cross‑tenant operations and analytics.