# Versioning and Lifecycle

## Purpose
Control change to metric definitions and releases.
Keep consumers stable while allowing progress.

## States
- Draft
- Proposed
- Approved
- Released
- Deprecated
- Retired

## Transitions
Require approvals for risky changes.
Use release channels per tenant or environment.
Provide automated rollback steps.

## Authoring
Authors use templates and validations before propose.
Job templates link to Metrics Schema and Pipeline.

## Legacy content
The following sections are imported from legacy v1 lifecycle and versioning.

### Lifecycle
# Kpi Lifecycle
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Lifecycle Management Framework

## Purpose
The KPI Lifecycle Management Framework (KLMF) defines how KPIs are created, approved, evolved, and retired in Cxofacts.  
It ensures that KPIs remain trustworthy, auditable, and relevant across business, industry, and client contexts.

Together with the KPI Call Framework (execution) and KPI Scheduler Framework (freshness),  
the Lifecycle Framework provides the governance backbone for KPI management.

## Lifecycle Stages
1. Draft – KPI proposed by business or technical owner; under review.  
2. Proposed – Submitted for approval; not yet active.  
3. Approved – Validated by CFO (business owner) and Data/Platform team (tech owner).  
4. Active – Available for production runs, dashboards, and AI activations.  
5. Deprecated – Superseded by a newer version; visible but discouraged.  
6. Retired – No longer available for production use. Archived for audit.  

## Ownership & Approval
- Business Owner – typically CFO, Controller, or Finance Leader. Ensures business meaning.  
- Technical Owner – Data Engineering / Product Engineering. Ensures correct mapping to GDP and technical feasibility.  
- Approval Workflow – no KPI moves from Draft → Approved without both business and technical approval.  

## Versioning
- Semantic Versioning applied to every KPI contract:  
  - Major (X.0.0) – breaking changes (e.g., new formula).  
  - Minor (0.X.0) – non-breaking additions (e.g., new extension).  
  - Patch (0.0.X) – technical fixes (e.g., corrected filter).  
- Contract Version stored and returned with every KPI call and response.  
- Dashboards & AI agents must reference a specific contract version.  

## KPI Variants (Industry & Client Specific)
KPIs may diverge from a Parent KPI to adapt to industry norms or client-specific practices.

### Parent KPI (Global)
- Universal definition (e.g., CFO-EF-02: DSO).  
- Baseline purpose, GDP mapping, and formula.  

### Industry Variant
- Derived from parent KPI; adjusted for industry practice.  
  - Example: DSO in SaaS vs. Manufacturing.  
- Tagged as: `CFO-EF-02-SaaS v1.0.0`.  

### Client-Specific Variant
- Derived from parent or industry variant; adjusted for client policies.  
  - Example: Client A excludes intercompany receivables.  
- Tagged as: `CFO-EF-02-SaaS-ClientA v1.0.0`.  

### Variant Rules
- Every variant must reference a Parent KPI ID.  
- Variants inherit contract unless explicitly overridden.  
- Parent → Variant → Client lineage is tracked.  
- Deprecation of Parent prompts review of all active variants.  

## Impact Analysis
- KPI changes automatically produce a list of dependent dashboards, reports, and AI agents.  
- Before deprecation or breaking change, all stakeholders are notified.  
- Dependency metadata stored in KPI catalog for audit.  

## Audit & Lineage
- Each KPI run stores:  
  - KPI ID + Contract Version  
  - Parent KPI (if variant)  
  - GDP tables + SQL lineage  
- Enables full traceability for auditors and CFO office.  

## Governance & Dev Notes
- Preventing KPI Sprawl – all KPIs and variants must be catalogued under lifecycle states.  
- Tenant Isolation – client-specific variants remain within tenant boundaries.  
- Transparency – every dashboard or AI activation surfaces KPI version & variant label.  
- End-of-Life Policy – retired KPIs archived but not deletable.  

## Example

**Parent KPI (Global)**  
- ID: CFO-EF-02  
- Name: Days Sales Outstanding (DSO)  
- Version: 1.0.0  
- Formula: Receivables ÷ Credit Sales × Days  

**Industry Variant (SaaS)**  
- ID: CFO-EF-02-SaaS  
- Name: DSO (SaaS Variant)  
- Version: 1.0.0  
- Formula: Adjusted for subscription billing  

**Client Variant (ClientA)**  
- ID: CFO-EF-02-SaaS-ClientA  
- Name: DSO (Client A Policy)  
- Version: 1.0.0  
- Formula: Excludes intercompany receivables  

## Change Request Management

All KPI lifecycle state transitions (Draft → Proposed → Approved → Active → Deprecated → Retired) must be initiated and tracked as Change Requests.

- Submission: Any modification to KPI definitions, validation rules, schedules, or SLA must be raised as a formal change request.  
- Routing: Requests flow into the Admin Dashboard approval queue.  
- Approvals: Dual sign-off (business + technical) is required for high‑criticality KPIs; configurable for others.  
- Impact Analysis: Automatically generated before decision, showing lineage and affected consumers.  
- Execution: Upon approval, the Admin Dashboard executes the state transition, updates audit logs, and triggers notifications.  
- Auditability: Every change request is immutable, timestamped, and linked to the KPI contract version.

This makes Lifecycle the governance policy and the Admin Dashboard the operational control plane for changes.


## Why It Matters
- Consistency – KPIs evolve in a controlled manner.  
- Flexibility – industry and client variants allowed, without breaking the backbone.  
- Transparency – CFOs and auditors always know *which version* they’re seeing.  
- Governance – no KPI is created or deprecated without business + technical accountability.

## Diagrams

None

## Tables

None



## Glossary

None

### Versioning
# Kpi Versioning
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Versioning Framework

## Purpose
The KPI Versioning Framework defines how KPIs evolve over time while maintaining trust, auditability, and compatibility.  
It ensures that every KPI run, report, or dashboard references an explicit contract version, preventing silent drift and preserving historical comparability.

## Core Concepts

- Semantic Versioning
  - Major (X.0.0) – Breaking changes (formula redefined, new denominator, altered purpose).  
  - Minor (0.X.0) – Non-breaking additions (new extension, optional filter, additional dimension).  
  - Patch (0.0.X) – Technical fixes (typos, corrected field mapping, metadata fix).  

- Contract Binding
  - Every KPI Call must specify a `contract_version`.  
  - Every KPI Response must echo the `contract_version`.  
  - Dashboards and AI agents always reference a specific version.

- Variants & Lineage
  - Parent KPI – Global definition.  
  - Industry Variant – Derived from parent, adapted to industry practice.  
  - Client Variant – Derived from parent or industry variant, adapted to client policy.  
  - Each variant maintains its own version chain but must reference its parent lineage.

- Compatibility
  - Backward compatibility – Old dashboards continue to work until migrated.  
  - Forward compatibility – Variants inherit parent definition unless overridden.  

## Version Catalog (DDL Sketch)

```sql
CREATE TABLE kpi_version_catalog (
  kpi_id            TEXT NOT NULL,
  contract_version  TEXT NOT NULL,
  parent_kpi_id     TEXT,                -- reference if variant
  owner_business    TEXT NOT NULL,
  owner_technical   TEXT NOT NULL,
  release_date      DATE NOT NULL,
  status            TEXT CHECK (status IN ('draft','approved','active','deprecated','retired')) NOT NULL,
  change_log        TEXT,                -- description of what changed
  created_at        TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (kpi_id, contract_version)
);
```

- Stores every KPI contract version with lineage.  
- Exposed in UI for traceability.  
- Enables dependency scans for dashboards, packs, and AI agents.  

## Integration with Other Frameworks

- KPI Lifecycle Framework  
  Lifecycle stages operate *per version* (e.g., v1.0.0 active, v0.9.0 deprecated).  

- KPI Sourcing Framework  
  Sourcing metadata is bound to the contract version (GDP/KPI references may differ between versions).  

- KPI Call Framework  
  Calls and responses must include `contract_version`.  

- KPI Logging & Monitoring Frameworks  
  Every run logged with `kpi_id` + `contract_version`. Monitoring views expose version distribution and failure trends.  

- KPI Error Handling Framework  
  Error codes are tied to specific contract versions for audit.  

## Example

**Days Sales Outstanding (CFO-EF-02)**  

- v1.0.0 (Parent KPI)  
  Formula: Receivables ÷ Credit Sales × Days.  

- v1.1.0 (Minor)  
  Added benchmark extension: Budget vs Actual.  

- v2.0.0 (Major)  
  Formula changed: excludes intercompany receivables.  

- v2.0.0-SaaS (Industry Variant)  
  Adjusted for subscription billing cycles.  

- v2.0.0-SaaS-ClientA (Client Variant)  
  Client-specific adjustment excluding deferred revenue.  

## Visual Timeline

![KPI Versioning Timeline](kpi-versioning-timeline.png)
This diagram illustrates how KPI versions evolve over time:
- Parent KPI starts the lineage.  
- Minor changes evolve within the same lineage (v1.1.0).  
- Major changes create new baselines (v2.0.0).  
- Industry Variants branch from parent versions.  
- Client Variants branch from industry variants, inheriting definitions unless overridden.  

## Why It Matters

- Trust – CFOs and auditors always know exactly *which version* produced a KPI.  
- Consistency – Prevents silent drift when KPI definitions evolve.  
- Comparability – Historical KPI runs remain valid under their original contracts.  
- Governance – Variants inherit lineage but evolve safely.  
- Scalability – Supports hundreds of KPIs across industries and clients with controlled versioning.  

## Diagrams

None

## Tables

None



## Glossary

None

### Job Authoring
# Kpi Job Authoring
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Job Authoring & Materialization

This document specifies how the platform allows users to create/modify KPI jobs in the UI, serialize them as YAML/JSON artifacts, and materialize them into a database for runtime orchestration by the Scheduler.

## Goals
- Great authoring experience: human‑readable YAML/JSON, Git‑friendly, code‑reviewable.
- Strong operations: database holds runtime state, coordinates, and observability.
- Governance: versioning, drift detection, auditability, and SLA enforcement.
- Safety: no secrets in artifacts; tenant isolation and RBAC honored.

## End‑to‑End Flow

1. Author in UI
   - Form captures: job id, tenant, schedule, timezone, dependencies, SLA, retry, alerts, defaults for KPI Call (e.g., scd_view, extensions).
   - Client + server validation (JSON Schema).

2. Serialize to Artifact (YAML/JSON)
   - UI/API serializes to YAML or JSON (same schema).
   - Compute content hash (SHA‑256) for versioning and drift detection.
   - Store artifact (object storage or Git repo).

3. Materialize to DB (runtime coordinates)
   - Upsert definition row (content‑addressed by hash).
   - Upsert binding row (tenant, env, region, schedule cron, active flag).
   - Persist dependencies, alert channels, and runtime state.
   - Scheduler reads DB only at runtime.

4. Execute & Observe
   - Scheduler executes KPI Calls.
   - Lineage + history + SLA status recorded in DB.
   - Alerts fire on failures or SLA breaches.

## Minimal Data Model (DDL Sketch)

```sql
-- Canonical job definition (content-addressed)
CREATE TABLE kpi_job_def (
  def_id          BIGSERIAL PRIMARY KEY,
  content_hash    TEXT UNIQUE NOT NULL,
  format          TEXT CHECK (format IN ('yaml','json')) NOT NULL,
  content         TEXT NOT NULL,                 -- stored artifact
  schema_version  TEXT NOT NULL,
  created_at      TIMESTAMPTZ DEFAULT now()
);

-- Binding = where/how this def runs
CREATE TABLE kpi_job_binding (
  binding_id       BIGSERIAL PRIMARY KEY,
  def_id           BIGINT REFERENCES kpi_job_def(def_id),
  tenant_id        TEXT NOT NULL,
  environment      TEXT CHECK (environment IN ('dev','stg','prod')) NOT NULL,
  region           TEXT,
  job_id           TEXT NOT NULL,
  kpi_id           TEXT NOT NULL,
  contract_version TEXT NOT NULL,
  schedule_cron    TEXT NOT NULL,
  timezone         TEXT NOT NULL,
  active_flag      BOOLEAN DEFAULT TRUE,
  scd_view         TEXT DEFAULT 'as_reported',
  created_at       TIMESTAMPTZ DEFAULT now(),
  UNIQUE (tenant_id, environment, job_id)
);

CREATE TABLE kpi_job_dependency (
  binding_id      BIGINT REFERENCES kpi_job_binding(binding_id),
  dep_type        TEXT CHECK (dep_type IN ('gdp','signal','kpi')) NOT NULL,
  dep_value       TEXT NOT NULL    -- e.g., GDP_Receivables or erp_eod_sync
);

CREATE TABLE kpi_job_alert (
  binding_id      BIGINT REFERENCES kpi_job_binding(binding_id),
  channel_type    TEXT CHECK (channel_type IN ('email','slack','opsgenie')) NOT NULL,
  channel_value   TEXT NOT NULL,   -- e.g., slack:#kpi-alerts
  severity        TEXT CHECK (severity IN ('low','medium','high')) NOT NULL
);

CREATE TABLE kpi_job_runtime (
  binding_id      BIGINT PRIMARY KEY REFERENCES kpi_job_binding(binding_id),
  last_run_at     TIMESTAMPTZ,
  next_run_at     TIMESTAMPTZ,
  last_status     TEXT CHECK (last_status IN ('success','failed','partial')),
  retry_count     INT DEFAULT 0,
  paused_until    TIMESTAMPTZ,
  last_error      TEXT
);

CREATE TABLE kpi_job_history (
  run_id          BIGSERIAL PRIMARY KEY,
  binding_id      BIGINT REFERENCES kpi_job_binding(binding_id),
  started_at      TIMESTAMPTZ,
  finished_at     TIMESTAMPTZ,
  status          TEXT,
  rows_processed  BIGINT,
  sla_breached    BOOLEAN,
  lineage_ref     TEXT,           -- pointer to lineage store entry
  error_message   TEXT
);
```

## YAML/JSON Schema (Authoring Object)

```yaml
# schema_version: 1.0
job_id: dso_daily
tenant: acme
kpi_id: CFO-EF-02
contract_version: 1.1.0
schedule:
  type: cron
  expression: "0 2 * * *"
  timezone: "UTC"
dependencies:
  gdp: [GDP_Receivables, GDP_Sales]
  signals: [erp_eod_sync]
sla:
  freshness: "24h"
retry:
  max_retries: 3
  backoff: exponential
alerts:
  - channel: "slack:#kpi-alerts"
    severity: high
runtime:
  scd_view: as_reported
  extensions:
    time: [MoM]
  filters:
    - field: ledger_type
      op: "="
      value: actual
```

> Store as YAML or JSON; the UI can toggle formats. The same schema underpins both. No secrets in artifacts-use `conn_id` references.

## API Surface (UI ↔ Platform)

- `POST /api/kpi-jobs`  
  Validates artifact → computes `content_hash` → upserts to `kpi_job_def` → creates `kpi_job_binding`, deps, alerts, runtime.  
    **Returns:** `{ binding_id, def_id, content_hash }`.

- `PUT /api/kpi-jobs/{binding_id}`  
  Non‑breaking binding edits (pause/resume, schedule tweak).  
  Breaking changes → create a new def (new hash) and rebind.

- `POST /api/kpi-jobs/{binding_id}/pause` / `/resume`  
  Sets/clears `paused_until` with audit.

- `GET /api/kpi-jobs/{binding_id}/history`  
  Run history + SLA + lineage pointers.

## Drift, Governance & Safety

- Drift detection: compare binding’s `def_id` hash vs latest stored artifact; if mismatch, flag and require reconcile (promote or rollback).
- Hot overrides: allow temporary DB overrides (e.g., pause) with expiry; reconciled on next sync.
- Audit surface: always show `kpi_id`, `contract_version`, `content_hash`, `schedule_cron`, `last/next run` in UI.
- RBAC: only owners (business + tech) can approve changes, aligned with Lifecycle Framework.
- Tenant isolation: bindings scoped by `tenant_id`; no cross‑tenant visibility.
- Secrets: never in artifacts; resolve at runtime via secrets manager (Vault/SM/KeyVault).

## Integration Points
- KPI Call Framework: `runtime` block maps to call payload defaults (e.g., `scd_view`, `extensions`, `filters`).  
- Scheduler Framework: `schedule`, `retry`, `sla`, and `dependencies` feed orchestration.  
- Lifecycle Framework: changes produce new `content_hash` and create lineage for review/approval.

## Provision for Diagram
*Placeholder:* A sequence diagram will be added to depict UI → Artifact → DB → Scheduler → Call → History/Lineage.

## Why this design
- Authoring excellence (YAML/JSON + Git) and operational excellence (DB runtime) together.  
- Traceable, auditable, and easy to promote across environments.  
- Scales to multi‑tenant and variant‑rich deployments without chaos.

## Diagrams

None

## Tables

None



## Glossary

None
