# BareCount™ Glossary

## A
**Action Panel**  
*Deprecated.* Earlier term for the Tenant UI surface used to trigger KPI-based activations. See **Data Action Console**.

**Action Plane**  
*Deprecated.* Earlier term for the architectural activation layer. See **Data Action Layer**.

**ADR (Architecture Decision Record)**  
A short document that records an important design choice, its context, alternatives considered, and consequences.

**Alert**  
A notification emitted when a rule, threshold, or service objective is breached. May include a runbook link and deduplication window.

**Anomaly Detection**  
Data quality technique that flags unusual patterns (point, contextual, or collective anomalies) based on rules or models.

**Approval Gate**  
A governance checkpoint where a contract, plan, or KPI lifecycle change requires explicit approval before promotion.

**Availability (SLO)**  
The percentage of time a service or artifact meets its uptime target over a window (e.g., 99.5%).

## B
**Backfill**  
A controlled replay that builds historical artifacts (e.g., Silver tables or KPIs) from a given start date.

**BareCount™**  
The Data Action Platform that turns enterprise data into consistent, explainable, and actionable outcomes.

**BCDR (Business Continuity & Disaster Recovery)**  
Policies and mechanisms that ensure the platform can continue operating and be restored after failures or disasters.

**Bronze / Silver / Gold**  
Refinement stages in the Data Plane: raw/landing (Bronze), standardized & reconciled (Silver), curated & governed (Gold).

## C
**Catalog (KPI Catalog)**  
A governed collection of KPIs with definitions, ownership, contracts, lineage, and lifecycle state.

**Compensation**  
A corrective step that reverses or mitigates side effects when a Data Action fails after partial completion.

**Compliance**  
Capabilities that ensure numbers and actions satisfy regulatory, audit, and policy obligations; backed by evidence.

**Config Artifact (Configuration Artifact)**  
A portable, versioned specification (YAML/JSON) that defines contracts, plans, schedules, or policy bindings.

**Contract**  
A formal artifact that binds a number to its **origin**, **logic**, **validation**, and **delivery** (including owners and SLOs).

**Contract Registry**  
The authoritative store for contract versions, states, approvals, and deprecations.

**Control Plane**  
The governance layer for creating, approving, versioning, and rolling out contracts and plans. Enforces RBAC, policies, and SLOs.

**Cost & Quota Management**  
Controls that limit and track compute, storage, and action volume per tenant, with enforcement and budgeting.

**Cross-Cutting Services**  
Platform capabilities that apply across layers: security, secrets/KMS, telemetry, lineage, DQC, alerts, BCDR, cost/quota.

## D
**Data Action**  
A governed, contract-bound unit that links a KPI to an outcome (workflow, approval, alert, or system update). Supports event, schedule, and manual triggers.

**Data Action Console**  
Tenant-facing UI where business users see, configure, and trigger Data Actions, and review evidence & status.

**Data Action Layer**  
Architectural execution environment that runs Data Actions with governance, idempotency, compensation, and evidence capture.

**Data Plane**  
Layer that refines data through Bronze → Silver → Gold → KPI; applies validation, lineage, and contract enforcement.

**Data Residency**  
Placement rules for where data and evidence are stored/processed (cloud, tenant, on-prem); includes hybrid patterns.

**Data Source Adapter**  
Connector that ingests or writes back to systems of record (ERP/CRM/MES/HRMS), handling auth, schema, and drift.

**Deduplication Window (Alerting)**  
Time window used to suppress alert floods by grouping repeated incidents.

**Delivery (Contract Dimension)**  
The when/where commitment of a contract (freshness window, availability target, delivery channel, and recipients).

**Discovery (Service)**  
Service that catalogs schemas, contracts, KPIs, lineage nodes, and actions for search and impact analysis.

**Drift (Schema/Metric Drift)**  
Unexpected change in source structure or metric distribution that can break pipelines or trust; detected via DQC or monitoring.

**Dual-Run**  
A rollout mode that runs new and old versions in parallel to compare results before switching traffic.

## E
**Encryption**  
Protection of data at rest and in transit using tenant-scoped keys and KMS policies.

**Enforcement (Schema/Policy Enforcement)**  
Compile-time or runtime checks that ensure artifacts and actions comply with contracts, policies, and security.

**Evidence**  
Auditable artifacts (hash, timestamp, actor, lineage) emitted by contracts and actions to prove compliance and correctness.

**Evidence Pack**  
A curated bundle of evidence records for a period, KPI, or audit request.

**Executive Packs**  
Modular business offerings (CFO/Finance, CGO/Sales, CMO/Marketing, COO/Operations) with curated KPIs, contracts, and Data Actions.

## F
**Feature Flag**  
A toggle used to enable/disable features or contract versions at runtime without redeployments.

**Freshness (SLO)**  
The maximum acceptable staleness of a number (e.g., KPI must be updated within 15 minutes of source change).

## G
**Gateway (API Gateway)**  
The entry point that authenticates, rate-limits, and routes API requests; applies tenant isolation and policy.

**Golden Data Points (GDP)**  
Canonical, business-ready fields that form the foundation for KPIs (e.g., `invoice_amount_net`).

**Governance Policy**  
A rule or constraint applied to contracts, plans, KPIs, or actions (e.g., approval gates, segregation of duties).

## H
**Hard-Fail / Soft-Fail**  
Execution policy: hard-fail blocks promotion or serving; soft-fail logs and alerts but allows continued operation under conditions.

**Health Endpoint**  
An API path exposing liveness/readiness of services or actions for monitoring and orchestration.

**Host App**  
Admin application used to define and approve contracts, manage tenants, observe health/SLOs, and handle rollouts.

## I
**Idempotency**  
A guarantee that re-running the same task with the same key yields the same side effects (no duplicates).

**Impact Analysis**  
An assessment of downstream effects when a contract, plan, or schema changes; powered by lineage.

**Integration (Reverse Connector)**  
A write-back or trigger to systems of record (e.g., ERP credit-hold) initiated by a Data Action.

**Isolation (Tenant Isolation)**  
Logical or physical separation of data, keys, and resources per tenant (multi-tenant, single-tenant, on-prem hybrid).

## K
**KPI (Key Performance Indicator)**  
A governed, contract-backed metric used for decisions and actions; published with lineage and evidence.

**KPI Lifecycle**  
States and transitions for KPIs (draft → validated → approved → published → deprecated → archived).

**KPI System**  
Data Plane components responsible for modeling, validating, publishing, and serving KPIs and their evidence.

**KMS (Key Management Service)**  
Managed service for generating, storing, rotating, and auditing cryptographic keys per tenant or environment.

## L
**Latency (SLO)**  
Time for a request or job to complete; tracked for contracts, pipeline steps, APIs, and actions.

**Lineage**  
A graph that traces numbers from sources through transformations to published KPIs and actions; used for trust and impact analysis.

**Logging (Structured Logging)**  
Machine-parseable logs emitted with trace IDs, plan IDs, tenant IDs, and severity for observability and audits.

## M
**Materialization**  
The act of producing a dataset or KPI (table, view, cache, or API response) per a plan.

**Messaging (Event Bus)**  
Asynchronous transport used for triggers, retries, and decoupled workflows in plans and actions.

**Metric Contract**  
A contract instance applied to a specific KPI or metric family, including owners, rules, and service objectives.

**Multi-Tenant (Deployment)**  
Shared runtime with strong per-tenant isolation and cost controls; contrasted with **Single-Tenant**.

## N
**Non-Functional Requirements (NFRs)**  
Quality attributes: performance, scale, availability, security, usability, operability, portability, and cost.

## O
**Observability**  
Metrics, logs, and traces instrumented across planes to monitor health, detect incidents, and meet SLOs.

**Offerings**  
Commercial packaging: Executive Packs, Value-Added Packs, and Deployment options.

**On-Prem Hybrid (Deployment)**  
Model where control/services run in cloud but sensitive data/processes remain on customer infrastructure.

**Owner (Service/Artifact Owner)**  
The accountable team or role responsible for a contract, KPI, plan, or action.

## P
**PHS (Platform Host System)**  
Grouping of control-plane capabilities (contracts, modules, services, infra, compliance, runbooks, SLOs).

**Plan Artifact**  
The versioned handoff from Control Plane to Data Plane; defines materializations, triggers, rollout/rollback, and observability.

**Policy (Governance Policy)**  
A rule or constraint applied to contracts, plans, KPIs, or actions (e.g., approval gates, segregation of duties).

## Q
**Quarantine**  
A containment state where an artifact (dataset, KPI) or action is withheld from serving due to quality or policy violations.

**Quota**  
A configured limit on resources or actions per tenant or artifact.

## R
**RBAC (Role-Based Access Control)**  
Permissions model defining who can view or change contracts, plans, KPIs, actions, data, and evidence.

**Reconciliation**  
Rule-based checks that verify internal consistency (e.g., subledger to GL, CRM to ERP) across stages.

**Red Flags**  
Operational risks and anti-patterns to avoid, documented in v1 risk section.

**Residency**  
See **Data Residency**.

**Retry (Backoff/Limit)**  
Automated re-execution policy for transient failures, with backoff and cap.

**Rollback**  
A controlled reversal to a previous version using dual-run evidence and policy criteria.

**Runbook**  
Operational steps for handling a class of incidents, linked from alerts and dashboards.

## S
**Scheduler**  
Service that runs plans and actions on defined cron/rate schedules with SLAs and concurrency limits.

**Schema Drift**  
Unexpected change to a source or intermediate schema; handled via detection, quarantine, and change management.

**Schema Services**  
Design and migration practices for schemas; includes meta-schema, naming, versioning, and enforcement.

**Secrets Management**  
Secure handling of credentials, tokens, and keys with rotation and least-privilege access.

**Security (Platform Security)**  
Controls spanning identity, RBAC, encryption, network boundaries, and audit logging.

**Service Level Agreement (SLA)**  
A contractual performance commitment published to customers.

**Service Level Objective (SLO)**  
An internal reliability target used to manage and report service health.

**Serving Layer**  
Interfaces (APIs, caches, exports, dashboards) from which KPIs and evidence are consumed.

**Single-Tenant (Deployment)**  
Isolated runtime and data plane per tenant; higher control and separation than multi-tenant.

**System of Action (SoA)**  
The BareCount™ platform layer that unifies fragmented systems of record and activates governed outcomes.

**System of Record (SoR)**  
Transactional systems (ERP/CRM/HRMS/MES) that capture business events with local integrity.

**Synthetic Data Utility**  
Tooling to seed representative, non-sensitive data for development and testing.

## T
**Tenant**  
A logically isolated customer environment within a shared or dedicated deployment.

**Tenant App**  
Customer-facing application that exposes governed KPIs, Data Actions, roles, and health.

**Traceability Matrix**  
A mapping from KPIs to their contracts, GDPs, validations, and lineage nodes.

**Trace ID / Plan ID**  
Identifiers used to correlate logs, metrics, and evidence across services and runs.

**Trigger (Action Trigger)**  
A condition that starts a Data Action: event-driven, scheduled, or manual.

## U
**Universal Date Table**  
A standardized enterprise time dimension with fiscal calendars, holidays, and cutoffs used across KPIs.

**Upgrade Path**  
Supported steps to move tenants or artifacts to newer versions, with deprecation and rollback rules.

**User Roles & Permissions**  
Defined access rights for Host App and Tenant App features and artifacts.

## V
**Validation (Contract Dimension)**  
Rules and thresholds that make a number trustworthy; includes schema, nullity, range, drift, anomaly, and reconcile checks.

**Value-Added Packs**  
Optional modules such as Advisory & Compliance, Analytics-as-a-Service, and BI Accelerators.

**Versioning**  
Lifecycle control for contracts, plans, and KPIs: draft → proposed → approved → dual-run → active → deprecated → archived.
