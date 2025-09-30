# Observability and Admin

## Purpose
Give operators and admins a clear view of health and usage.
Record logs and metrics for audits and root cause analysis.

## Dashboards
Show freshness, completeness, cost, error rate, and usage.

## Logs and Traces
Record request logs and internal traces.
Link logs to evidence and lineage by run id.

## Admin Workflows
Approve releases, manage schedules, and assign ownership.
Review alerts and breach reports.

## Legacy content
The following sections are imported from legacy v1 documents.

### Monitoring
# Kpi Monitoring
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Establish observability for the KPI System across logs, metrics, and traces.  
- Scope: Includes telemetry, alerting, SLOs, dashboards. Excludes business KPI definitions.  
- Target Readers: SRE/ops, platform owners, engineers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Monitoring Framework

## Purpose
The KPI Monitoring Framework provides real-time visibility into KPI health, SLA adherence, and validation results.  
It builds on the KPI Logging Framework by surfacing curated metrics, views, dashboards, and alerts for CFOs, business leaders, and technical operators.  

This ensures KPIs are not just executed and logged, but also continuously monitored, visualized, and governed.

## Core Concepts

- Views over Logs
  - Abstract raw log tables into compact, query-friendly SQL views.
  - Expose only the most relevant run, validation, lineage, and SLA fields.

- Dashboards
  - Executive dashboards → SLA compliance %, KPI health index, top failing KPIs.  
  - Operational dashboards → validation failures by rule type, retry success rates.  
  - Developer dashboards → SQL hash lineage, error distributions, runtime anomalies.  

- Alerting
  - SLA breaches → CFO office + ops.  
  - Validation failures → Data quality team.  
  - Runtime anomalies → Platform engineering.  

- Governance
  - Monitoring views enforce tenant-aware access controls.  
  - Metrics and definitions are published in a KPI dictionary for consistency.  

## SQL Views Layer

### 1. Run Overview
One row per run with verdicts, timings, SLA, and key metadata.

```sql
CREATE OR REPLACE VIEW vw_kpi_run_overview AS
SELECT
  r.run_id,
  r.tenant_id,
  r.environment,
  r.kpi_id,
  r.contract_version,
  r.variant_label,
  r.started_at,
  r.finished_at,
  EXTRACT(EPOCH FROM (r.finished_at - r.started_at))::BIGINT AS duration_sec,
  r.status,
  r.sla_breached,
  d.verdict,
  d.time_grain,
  d.time_range,
  d.extensions
FROM kpi_log_run r
LEFT JOIN kpi_log_delivery d ON d.run_id = r.run_id;
```

### 2. Validation Summary
Rollup of pre/post validation outcomes for quick health checks.

```sql
CREATE OR REPLACE VIEW vw_kpi_validation_summary AS
WITH pre AS (
  SELECT run_id,
         COUNT(*) FILTER (WHERE result='fail') AS pre_fail_count
  FROM kpi_log_pre_validation
  GROUP BY run_id
),
post AS (
  SELECT run_id,
         COUNT(*) FILTER (WHERE result='fail') AS post_fail_count
  FROM kpi_log_post_validation
  GROUP BY run_id
)
SELECT
  r.run_id,
  r.tenant_id,
  r.kpi_id,
  r.contract_version,
  r.status,
  COALESCE(pre.pre_fail_count,0) AS pre_fail_count,
  COALESCE(post.post_fail_count,0) AS post_fail_count
FROM kpi_log_run r
LEFT JOIN pre  ON pre.run_id  = r.run_id
LEFT JOIN post ON post.run_id = r.run_id;
```

### 3. Lineage Sources
Dependency view showing GDP tables and KPI references per run.

```sql
CREATE OR REPLACE VIEW vw_kpi_lineage_sources AS
SELECT
  r.run_id,
  r.tenant_id,
  r.kpi_id,
  r.contract_version,
  s.source_type,
  s.source_object,
  s.source_version
FROM kpi_log_run r
JOIN kpi_log_sourcing s ON s.run_id = r.run_id;
```

### 4. SLA Violations
Focused list of runs breaching SLA.

```sql
CREATE OR REPLACE VIEW vw_kpi_sla_violations AS
SELECT
  r.run_id,
  r.tenant_id,
  r.kpi_id,
  r.contract_version,
  r.started_at,
  r.finished_at,
  r.status,
  r.error_code,
  r.error_message
FROM kpi_log_run r
WHERE r.sla_breached = TRUE;
```

## Dashboards

- Executive View
  - SLA compliance rate (% of runs within SLA).  
  - KPI health index (weighted by failures, verdicts).  
  - Top failing KPIs (by failure count).  

- Ops View
  - Validation failure trends by rule type.  
  - Retry success/failure rates.  
  - Runs skipped due to pre-validation.  

- Dev View
  - Error code distribution.  
  - SQL hash diffs for lineage debugging.  
  - Run duration anomalies vs historical baseline.  

## Alerting Strategy

- SLA breach → high-severity alert to CFO office & ops channel.  
- Validation fail (hard stop) → medium-severity alert to data quality team.  
- Unusual runtime anomaly (duration, row count) → medium-severity alert to platform engineering.  
- Alerts include deep links to `vw_kpi_run_overview` and `vw_kpi_validation_summary`.  

## Governance & Operations

- Tenant Isolation
  - All monitoring views scoped by tenant; RLS enforced.  

- Retention & Archiving
  - Inherits logging retention policy (e.g., 24 months active, then cold archive).  

- Data Dictionary
  - Published definitions of monitoring fields (status, SLA, verdict) to avoid ambiguity.  

- Materialization
  - Heavy views (e.g., run overview) may be materialized in the warehouse for performance.  

## Why It Matters

- Transparency – KPIs aren’t black boxes; every run’s health is visible.  
- Trust – CFOs and auditors can inspect KPI monitoring dashboards as assurance.  
- Resilience – Ops teams can act on alerts before business impact grows.  
- Efficiency – BI dashboards bind to simple views instead of complex joins.  
- Future-Proof – Monitoring can expand with anomaly detection, ML scoring, or KPI reliability indices.  

## Diagrams

None

## Tables

None



## Glossary

None

### Logging
# Kpi Logging
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

# KPI Logging Framework

## Purpose
The KPI Logging Framework defines dedicated, business-aware logging for KPI executions in Cxofacts.  
It records what KPI ran, with which sources and contract version, what validations occurred, and what was delivered-separately from generic ETL or infrastructure logs.  
This provides CFO-grade transparency, auditability, and tenant-safe traceability.

## Core Concepts

- Business-Facing Logs
  Logs are organized around KPI semantics (KPI ID, contract version, verdicts) rather than low-level pipeline steps.

- End-to-End Coverage
  One run entry spans sourcing → pre-validation → execution → post-validation → delivery.

- Tenant Isolation
  All logs are scoped to tenant/environment/region; no cross-tenant exposure.

- Immutability
  Historical log entries are append-only; corrections create new entries linked via lineage refs.

## Minimal Data Model (DDL Sketch)

```sql
-- One row per executed attempt (including retries).
CREATE TABLE kpi_log_run (
  run_id            BIGSERIAL PRIMARY KEY,
  tenant_id         TEXT NOT NULL,
  environment       TEXT CHECK (environment IN ('dev','stg','prod')) NOT NULL,
  region            TEXT,
  kpi_id            TEXT NOT NULL,
  contract_version  TEXT NOT NULL,
  variant_label     TEXT,                      -- e.g., SaaS, ClientA
  trigger_type      TEXT CHECK (trigger_type IN ('time','event','manual')) NOT NULL,
  triggered_by      TEXT,                      -- scheduler id / user / event name
  schedule_cron     TEXT,
  started_at        TIMESTAMPTZ NOT NULL,
  finished_at       TIMESTAMPTZ,
  status            TEXT CHECK (status IN ('success','failed','partial','skipped')) NOT NULL,
  rows_processed    BIGINT,
  sla_breached      BOOLEAN DEFAULT FALSE,
  retry_seq         INT DEFAULT 0,             -- 0 for first attempt, increment on retry
  error_code        TEXT,
  error_message     TEXT,
  lineage_ref       TEXT                       -- pointer to lineage store
);

-- Sourcing lineage resolved for this run.
CREATE TABLE kpi_log_sourcing (
  run_id            BIGINT REFERENCES kpi_log_run(run_id),
  source_type       TEXT CHECK (source_type IN ('gdp','kpi')) NOT NULL,
  source_object     TEXT NOT NULL,             -- GDP table or KPI ID
  source_version    TEXT,                      -- KPI contract version (when source_type='kpi')
  attributes        TEXT,                      -- optional: list of GDP attributes
  sql_hash          TEXT,                      -- hash of generated SQL (if any)
  UNIQUE (run_id, source_type, source_object)
);

-- Pre-validation outcomes.
CREATE TABLE kpi_log_pre_validation (
  run_id            BIGINT REFERENCES kpi_log_run(run_id),
  rule_id           TEXT,
  rule_type         TEXT,                      -- availability/readiness/quality
  severity          TEXT CHECK (severity IN ('warn','error')),
  result            TEXT CHECK (result IN ('pass','fail')),
  details           TEXT
);

-- Post-validation outcomes.
CREATE TABLE kpi_log_post_validation (
  run_id            BIGINT REFERENCES kpi_log_run(run_id),
  rule_id           TEXT,
  rule_type         TEXT,                      -- value_range/variance/verdict_alignment/cross_kpi
  severity          TEXT CHECK (severity IN ('warn','error')),
  result            TEXT CHECK (result IN ('pass','fail')),
  details           TEXT
);

-- What was delivered to consumers.
CREATE TABLE kpi_log_delivery (
  run_id            BIGINT REFERENCES kpi_log_run(run_id),
  time_grain        TEXT,
  time_range        TEXT,
  scd_view          TEXT,                      -- as_reported/restated
  extensions        TEXT,                      -- e.g., ["MoM","unit","budget_vs_actual"]
  verdict           TEXT,                      -- Adequate/Low/Critical
  output_sample     TEXT                       -- small JSON sample or reference to blob
);
```

> Note: Table names are illustrative; adapt to warehouse/OLTP conventions.

## Governance & Operations

- Append-Only Policy
  No updates to past rows except appending corrective entries; maintain audit correctness.

- PII/PHI Avoidance
  KPI logs store metric metadata, not sensitive personal data.

- Retention Strategy
  Keep full logs for a defined period (e.g., 24 months), then archive cold storage.

- Access Control
  Row-level security by `tenant_id`; restricted columns for sensitive operational context.

- Indexing & Queryability
  Index by (tenant_id, kpi_id, started_at) for quick drill; expose views for CFO/ops dashboards.

- Alert Integration
  Error/warn results can trigger Slack/Email/Opsgenie with deep links to log runs.

## Integration Points

- KPI Scheduler Framework
  Creates `kpi_log_run` at trigger time; updates status on completion.

- KPI Sourcing Framework
  Writes resolved GDP/KPI lineage into `kpi_log_sourcing`.

- KPI Pre-Validation Framework
  Writes rule results into `kpi_log_pre_validation`; can set run status to `skipped` on hard fail.

- KPI Call Framework
  Provides SQL hash/lineage refs and rows processed.

- KPI Post-Validation Framework
  Writes rule results into `kpi_log_post_validation`; controls delivery gating.

- Consumption Layer
  Summarizes delivered context into `kpi_log_delivery` for end-user transparency.

## Example Flow

1. Scheduler triggers CFO-EF-02 v1.0.0 for tenant *Acme* at 02:00 UTC → inserts `kpi_log_run`.  
2. Sourcing resolves GDP_Receivables + GDP_Sales → inserts `kpi_log_sourcing`.  
3. Pre-Validation checks *availability, freshness <24h, no negative receivables* → all pass → records in `kpi_log_pre_validation`.  
4. KPI Call runs; SQL hash & lineage saved; rows_processed recorded.  
5. Post-Validation checks *ratio bounds & volatility* → pass; verdict = Adequate → recorded.  
6. Delivery row captures time range, extensions, verdict; run marked success.  

## Why It Matters

- Transparency & Trust
  A CFO-readable trail explains *what ran, on what data, and why the result is valid*.

- Audit & Compliance
  Immutable logs satisfy internal/external audits and financial governance requirements.

- Faster Triage
  Clear separation from pipeline logs speeds root-cause analysis for KPI issues.

- Tenant Safety
  Strong isolation minimizes risk in multi-tenant environments.

## Diagrams

None

## Tables

None



## Glossary

None

### Admin Dashboard
# Kpi Admin Dashboard
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

# KPI Admin Dashboard Framework

## Purpose
The KPI Admin Dashboard is the control plane for Cxofacts.  
It centralizes catalog management, deployment, versioning, monitoring, and operational control for KPIs across tenants.  
Both platform admins and client admins can safely publish, pause, resume, roll back, and decommission KPIs with full audit trails.

## Personas & RBAC

- Platform Admin (Cxofacts Ops)  
  Global view across tenants; manages platform-wide settings, templates, rollouts, and incident response.

- Client Admin (Tenant Owner / Controller)  
  Manages KPIs for their tenant: approvals, schedules, SLA, alert routes, variants, and maintenance actions.

- Read-Only Roles (CFO/Exec, Auditors)  
  View health, versions, lineage, and SLA reports; cannot change state.

**RBAC model**: action-level permissions on KPI objects (create, approve, publish, pause, resume, rollback, retire), scoped by tenant and environment.

## Core Capabilities

1. KPI Catalog & Search
   - Browse by pack, layer (Primary/Secondary/Composite), owner, status, version.
   - Full-text search across purpose, formula, sources, and rules.

2. Versioning & Promotion
   - Draft → Approved → Active → Deprecated → Retired (per Lifecycle).  
   - Promote across environments (dev → stg → prod) with approvals.  
   - Rollback to previous contract_version with one click.

3. Deployment Controls
   - Publish/Unpublish KPI version.  
   - Pause/Resume a KPI (global or scoped by entity/time).  
   - Maintenance Mode with banner reasons and ETA.  
   - Canary Release (% traffic / subset of entities).

4. Scheduling & SLA
   - Edit frequency, triggers, windows.  
   - Configure SLA targets and grace windows.  
   - Preview impact of schedule changes on dependencies.

5. Validation & Error Policies
   - Manage pre/post validation rules and severities.  
   - Set error-handling policies (retry, fallback, suppression).

6. Alerts & Reports
   - Route alerts (Slack/Email/Opsgenie) per KPI or pack.  
   - Subscribe stakeholders to daily/weekly/monthly reports.

7. Lineage & Impact Analysis
   - Visual DAG: GDP → KPIs → Derived KPIs → Dashboards.  
   - Pre-change impact report (who/what is affected).

8. Tenant & Secret Management
   - Data connections (RDS/Redshift) and credentials (via AWS Secrets Manager).  
   - Tenant-level configuration (time zone, currency, calendars).

9. Audit & Compliance
   - Immutable event log: who changed what, when, and why.  
   - Evidence bundle exports for audits.

## Key Workflows

### A) Publish a New KPI Version
1. Author definition → submit for approval.  
2. Validation of sources & rules; generate impact analysis.  
3. Approver signs off → Promote to env → Publish to Active.  
4. Monitor with canary (optional) → full rollout.

### B) Pause/Resume for Maintenance
1. Admin selects KPI → Pause (global or scoped).  
2. Scheduler skips runs; dashboards show maintenance badge.  
3. Fix deployed → Resume → post-validation enforced on first run.

### C) Hotfix / Rollback
1. Issue detected → Rollback to last healthy version.  
2. Error handling routes alerts; logs capture rollback event.  
3. Post-mortem auto-snapshot: runs, failures, rules triggered.

### D) Decommission a KPI
1. Mark Deprecated → warn consumers.  
2. After grace period → Retire; archive lineage and mappings.  

## UI Modules (Suggested)

- Catalog (table & filters)  
- KPI Detail (tabs: Overview, Versions, Sourcing, Validation, Schedule/SLA, Lineage, Monitoring, Alerts, Audit)  
- Change Requests (approval queue)  
- Rollouts (canary status, environment promotions)  
- Incidents (active failures, paused KPIs, SLA breaches)  
- Settings (tenant configs, secrets, alert channels)

**Diagram placeholders:**  
- Catalog & Detail Wireframes → `../assets/diagrams/kpi-admin-catalog.svg`  
- Rollout/Approval Flow → `../assets/diagrams/kpi-admin-rollout.svg`

## Backend APIs (Control Plane)

- `POST /kpis/{kpi_id}/versions/{ver}/publish`  
- `POST /kpis/{kpi_id}/versions/{ver}/pause` (scope: global/entity/time)  
- `POST /kpis/{kpi_id}/versions/{ver}/resume`  
- `POST /kpis/{kpi_id}/versions/{ver}/rollback`  
- `POST /kpis/{kpi_id}/versions/{ver}/schedule`  
- `POST /kpis/{kpi_id}/versions/{ver}/sla`  
- `POST /kpis/{kpi_id}/versions/{ver}/validation`  
- `GET  /kpis/{kpi_id}/lineage`  
- `GET  /kpis/{kpi_id}/impact?change=...`  
- `POST /approvals/{request_id}/decision`

All write operations append events to the audit log and update the version catalog.

## Governance & Safety

- Dual-approval for high-criticality KPIs (4-eyes principle).  
- Change window enforcement for production.  
- Policy guardrails (cannot publish without active SLA & validation rules).  
- Scoped pause to avoid unintended global outages.  
- RBAC & RLS for tenant isolation and least privilege.

## NFRs

- Availability 99.9% for control plane UI/APIs.  
- Auditability 100% of admin actions stored with reason & approver.  
- Performance Catalog search < 1s P95 (indexed, cached).  
- Security SSO/OIDC, fine-grained RBAC, secrets in AWS Secrets Manager.  
- Scalability 10k+ KPIs across tenants; bulk actions supported.  
- Usability All critical actions are reversible (rollback) and explainable (impact analysis).

## AWS Integration (Phase 1)

- UI: hosted on S3 + CloudFront.  
- APIs: API Gateway + Lambda (control plane) with Step Functions integration.  
- Jobs: ECS Fargate for KPI runs; EventBridge for triggers.  
- Storage: RDS/Redshift for KPI results; DynamoDB for KPI logs & audit events.  
- Observability: CloudWatch metrics/logs; SNS/SQS for alerts & approvals.  
- Security: Cognito (or enterprise SSO), IAM-per-tenant roles, KMS encryption.

## Why It Matters

- One control surface to manage KPI lifecycle end-to-end.  
- Operational safety with pause/resume, rollback, and canary releases.  
- Governance with approvals, audit logs, and impact analysis.  
- Speed - shipping and fixing KPIs becomes a managed, repeatable process.

## Diagrams

None

## Tables

None



## Glossary

None
