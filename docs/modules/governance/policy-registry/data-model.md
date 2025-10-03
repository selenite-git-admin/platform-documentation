# Data Model

## Scope
This page defines the persistent data structures for Policy Registry.
It covers entities, relationships, DBML, DDL skeletons, seed examples, and migration notes.

## Conventions
- Database: PostgreSQL
- Identifiers: snake_case
- Primary keys: surrogate `uuid` unless noted
- Timestamps: `timestamptz` in UTC
- Soft delete is not used. Use status fields and history tables instead.

## ERD
<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/policy-registry/policy-registry-erd.svg" alt="Policy Registry Entity Relationship Diagram">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/policy-registry/policy-registry-erd.svg" alt="Policy Registry Entity Relationship Diagram">
</div>

_Figure 1: Policy Registry Entity Relationship Diagram_{.figure-caption}

## Entities
- `policies`
  Logical policy objects. Human owned and named.
- `policy_versions`
  Immutable serialized policy definitions. One policy can have many versions.
- `policy_bindings`
  Attachment of a policy or a specific version to a scope such as tenant, schema, or workflow.
- `evaluations`
  Decisions produced when the registry evaluates a subject against a binding.
- `evaluation_evidence`
  Artifacts and references that justify a decision.
- `audit_log`
  Administrative actions on policies and bindings.

## Relationships
- One `policies` to many `policy_versions`
- One `policies` to many `policy_bindings`
- One `policy_bindings` to many `evaluations`
- One `evaluations` to many `evaluation_evidence`

## Status and enums
- Policy status: `draft`, `active`, `archived`
- Binding status: `active`, `disabled`
- Decision: `allow`, `deny`, `require_approval`, `warn`
- Scope type: `tenant`, `schema`, `workflow`
- Evidence type: `log`, `receipt`, `artifact`, `reference`

## DBML
```dbml
Project BareCount_PolicyRegistry {
  database_type: "PostgreSQL"
}

Table policies {
  policy_id uuid [pk]
  name text [not null, unique]
  category text
  status text [not null, note: 'draft|active|archived']
  created_at timestamptz [not null, default: `now()`]
  created_by text
}

Table policy_versions {
  version_id uuid [pk]
  policy_id uuid [not null, ref: > policies.policy_id]
  version int [not null]
  definition_json jsonb [not null]
  is_current boolean [not null, default: false]
  created_at timestamptz [not null, default: `now()`]
  created_by text
  Indexes {
    (policy_id, version) [unique]
  }
}

Table policy_bindings {
  binding_id uuid [pk]
  policy_id uuid [not null, ref: > policies.policy_id]
  version_id uuid [ref: > policy_versions.version_id]
  scope_type text [not null, note: 'tenant|schema|workflow']
  scope_ref text [not null, note: 'identifier of the target scope']
  status text [not null, default: 'active']
  created_at timestamptz [not null, default: `now()`]
  created_by text
  Indexes {
    (scope_type, scope_ref)
  }
}

Table evaluations {
  eval_id uuid [pk]
  binding_id uuid [not null, ref: > policy_bindings.binding_id]
  subject_type text [not null, note: 'schema_change|workflow_run|tenant_event']
  subject_ref text [not null]
  decision text [not null, note: 'allow|deny|require_approval|warn']
  reason_code text
  evaluator_version text
  evaluated_at timestamptz [not null, default: `now()`]
  Indexes {
    (binding_id, evaluated_at)
    (subject_type, subject_ref, evaluated_at)
  }
}

Table evaluation_evidence {
  evidence_id uuid [pk]
  eval_id uuid [not null, ref: > evaluations.eval_id]
  evidence_type text [not null, note: 'log|receipt|artifact|reference']
  evidence_ref text [not null]
  captured_at timestamptz [not null, default: `now()`]
  Indexes {
    (eval_id)
  }
}

Table audit_log {
  audit_id uuid [pk]
  actor text
  action text [not null]
  target text
  old_value jsonb
  new_value jsonb
  at timestamptz [not null, default: `now()`]
  Indexes {
    (at)
  }
}
```

## DDL skeletons
```sql
-- policies
create table if not exists policies (
  policy_id uuid primary key,
  name text not null unique,
  category text,
  status text not null check (status in ('draft','active','archived')),
  created_at timestamptz not null default now(),
  created_by text
);

-- policy_versions
create table if not exists policy_versions (
  version_id uuid primary key,
  policy_id uuid not null references policies(policy_id),
  version int not null,
  definition_json jsonb not null,
  is_current boolean not null default false,
  created_at timestamptz not null default now(),
  created_by text,
  unique (policy_id, version)
);

-- policy_bindings
create table if not exists policy_bindings (
  binding_id uuid primary key,
  policy_id uuid not null references policies(policy_id),
  version_id uuid references policy_versions(version_id),
  scope_type text not null check (scope_type in ('tenant','schema','workflow')),
  scope_ref text not null,
  status text not null default 'active' check (status in ('active','disabled')),
  created_at timestamptz not null default now(),
  created_by text
);
create index if not exists idx_policy_bindings_scope on policy_bindings(scope_type, scope_ref);

-- evaluations
create table if not exists evaluations (
  eval_id uuid primary key,
  binding_id uuid not null references policy_bindings(binding_id),
  subject_type text not null check (subject_type in ('schema_change','workflow_run','tenant_event')),
  subject_ref text not null,
  decision text not null check (decision in ('allow','deny','require_approval','warn')),
  reason_code text,
  evaluator_version text,
  evaluated_at timestamptz not null default now()
);
create index if not exists idx_evaluations_binding_time on evaluations(binding_id, evaluated_at);
create index if not exists idx_evaluations_subject_time on evaluations(subject_type, subject_ref, evaluated_at);

-- evaluation_evidence
create table if not exists evaluation_evidence (
  evidence_id uuid primary key,
  eval_id uuid not null references evaluations(eval_id),
  evidence_type text not null check (evidence_type in ('log','receipt','artifact','reference')),
  evidence_ref text not null,
  captured_at timestamptz not null default now()
);
create index if not exists idx_evidence_eval on evaluation_evidence(eval_id);

-- audit_log
create table if not exists audit_log (
  audit_id uuid primary key,
  actor text,
  action text not null,
  target text,
  old_value jsonb,
  new_value jsonb,
  at timestamptz not null default now()
);
create index if not exists idx_audit_time on audit_log(at);
```

## Seed examples
```sql
insert into policies (policy_id, name, category, status)
values
  (gen_random_uuid(), 'Export Requires Approval', 'export', 'active');

insert into policy_versions (version_id, policy_id, version, definition_json, is_current)
select gen_random_uuid(), p.policy_id, 1,
       '{"rule":"require_approval","applies_to":"export"}'::jsonb,
       true
from policies p
where p.name = 'Export Requires Approval';

insert into policy_bindings (binding_id, policy_id, version_id, scope_type, scope_ref, status)
select gen_random_uuid(), p.policy_id, v.version_id, 'tenant', 'tenant-acme', 'active'
from policies p
join policy_versions v on v.policy_id = p.policy_id and v.is_current = true
where p.name = 'Export Requires Approval';
```

## Validation queries
```sql
-- list current policies and versions
select p.name, v.version, v.is_current
from policies p
join policy_versions v on v.policy_id = p.policy_id
order by p.name, v.version desc;

-- bindings by scope
select scope_type, scope_ref, count(*) as bindings
from policy_bindings
group by 1,2;

-- decisions by result
select decision, count(*) from evaluations group by 1 order by 2 desc;
```

## Migration notes
- Treat `policy_versions` as immutable. Do not update `definition_json` in place. Create a new version and flip `is_current`.
- Allow `policy_bindings.version_id` to be null when a binding targets a policy by name. Resolve to `is_current` at evaluation time.
- Keep `audit_log` append only. Use the module runbook for correction procedures.
- Add indexes only when query patterns are stable. Review with observability signals after initial rollout.
