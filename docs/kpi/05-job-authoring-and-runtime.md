# Job Authoring and Runtime

## Purpose
Provide templates and checks for authoring metric jobs.
Align run control with Pipeline triggers and profiles.

## Authoring
Use templates that reference metrics schema contracts.
Run validations before propose and release.

## Runtime
Select run profiles and stage sets.
Record evidence for each run.

## Legacy content
The following section is imported from legacy job authoring.

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
