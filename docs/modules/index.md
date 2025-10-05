# Modules

> **Audience:** Builders and operators. Short, prescriptive, and testable.  
> **Contract:** Each module owns a capability, exposes stable interfaces, and integrates with Pipelines (the backbone).

## Tenets
- **Pipelines first.** Modules exist to feed, govern, execute, store, expose, and secure pipeline work.
- **Contracts over code.** Every surface is documented, versioned, and additive.
- **Evidence by default.** Material events emit receipts, lineage, and metrics.
- **Least surprise.** Shared patterns: 7-file docs set, cursor paging, idempotent writes, standard errors.

## How Modules Relate to Pipelines
Pipelines move data from **ingestion → raw → GDP → KPI → published**. Modules wrap that motion with platform capabilities:

- **Feed:** Host, Connectors
- **Constrain:** Governance (contracts, policies, obligations)
- **Execute:** Runtime (orchestrator, compute, streaming), Runners
- **Store:** Storage (raw, GDP, KPI, published, calendar)
- **Expose:** **Delivery** (APIs, catalog, exports, webhooks, dashboards)
- **Secure & Prove:** Access, Security, Trust & Integrity

See the full pipeline lifecycle: [Pipelines](../pipelines/index.md).

---

## Module Families

### Host
Administrative surface for the platform. Hosts tenants, catalogs, and operational controls.

**Pipeline touchpoints**
- Tenant creation, connector onboarding, and resource assignment prepare streams for ingestion.
- Platform Catalog exposes pipeline, contract, and dataset metadata for operators and auditors.

**Start here**
- [Host Overview](host/index.md) · [Platform Catalog](host/platform-catalog/index.md) · [Tenant Management](host/tenant-management/index.md)

---

### Access
Identity and permissions for people and systems that invoke pipeline surfaces.

**Pipeline touchpoints**
- Authentication and Authorization protect pipeline APIs, manifests, and outputs.
- Subscription Enforcement ties tenant entitlements to pipeline features.

**Start here**
- [Access Overview](access/index.md) · [Authentication](access/authentication/index.md) · [Authorization](access/authorization/index.md) · [Subscription Enforcement](access/subscription-enforcement/index.md)

---

### Governance
Defines and enforces policies that make pipelines trustworthy.

**Pipeline touchpoints**
- **Data Contract Registry** validates extractor schemas during ingestion.
- **Policy Registry** and **Lineage Obligations** set blocking/warning rules for runs and publication.

**Start here**
- [Governance Overview](governance/index.md) · [Policy Registry](governance/policy-registry/index.md) · [Data Contract Registry](governance/data-contract-registry/index.md) · [Lineage Obligations](governance/lineage-obligations/index.md)

---

### Trust & Integrity
Integrity guarantees and operational secrets for pipeline runs.

**Pipeline touchpoints**
- **Evidence Ledger** records lineage and evidence at every stage.
- **Secrets** and **Encryption** secure credentials and data at rest/in transit.

**Start here**
- [Trust Overview](trust/index.md) · [Evidence Ledger](trust/evidence-ledger/index.md) · [Secrets](trust/secrets/index.md) · [Encryption](trust/encryption/index.md)

---

### Security
Edge and network defenses on all pipeline-accessible surfaces.

**Pipeline touchpoints**
- **Gateway** secures API access to pipeline products.
- **Network Security** enforces runner connectivity (PrivateLink, VPN, egress control).

**Start here**
- [Security Overview](security/index.md) · [Gateway](security/gateway/index.md) · [Network Security](security/network-security/index.md)

---

### Connectors
Standardized ingestion/egress into enterprise systems and public data sources.

**Pipeline touchpoints**
- Connector deployments initialize ingestion streams and schemas under contract.
- Health, state, and backpressure are emitted for orchestration.

**Start here**
- [Connectors Overview](../connectors/index.md) (family lives under Connectors)

---

### Runtime
Shared platform services that keep pipelines reliable.

**Pipeline touchpoints**
- **Orchestrator** schedules and coordinates runs and events.
- **Compute Fabric** executes tasks with isolation and quotas.
- **Streaming Bus** handles events, DLQ, and retries.
- **Observability, Error Handling, Metering** provide health and cost signals.

**Start here**
- [Runtime Overview](runtime/index.md) · [Orchestrator](runtime/orchestrator/index.md) · [Compute Fabric](runtime/compute-fabric/index.md) · [Streaming Bus](runtime/streaming-bus/index.md) · [Observability](runtime/observability/index.md) · [Error Handling](runtime/error-handling/index.md) · [Metering](runtime/metering/index.md)

---

### Storage
Durable stores for each pipeline checkpoint to preserve lineage and reproducibility.

**Pipeline touchpoints**
- **Raw Store** captures immutable ingested data.
- **GDP Store** holds conformed entities.
- **KPI Store** and **Published Store** expose governed outputs.
- **GDP Calendar** provides time scaffolding for backfills and KPI windows.

**Start here**
- [Storage Overview](storage/index.md) · [Raw Store](storage/raw-store/index.md) · [GDP Store](storage/gdp-store/index.md) · [KPI Store](storage/kpi-store/index.md) · [Published Store](storage/published-store/index.md) · [GDP Calendar](storage/gdp-calendar/index.md)

---

### Delivery
Delivers published outputs to applications and users with zero engineering lift.

**Pipeline touchpoints**
- **Delivery APIs**, **Exports**, and **Webhooks** publish GDP/KPI products from the Published Store.
- **Delivery Catalog** provides searchable access to datasets and versions produced by pipelines.
- **Dashboards** render governed views on top of Delivery APIs.

**Start here**
- [Delivery Overview](delivery/index.md) · [Delivery APIs](delivery/apis/index.md) · [Exports](delivery/exports/index.md) · [Webhooks](delivery/webhooks/index.md) · [Delivery Catalog](delivery/catalog/index.md) · [Dashboards](delivery/dashboards/index.md)

---

### Action
Turns published outputs into enterprise actions.

**Pipeline touchpoints**
- **Action Engine** consumes KPI events/thresholds and evaluates guardrails.
- **Action Delivery** pushes outcomes to enterprise systems and captures receipts.

**Start here**
- [Action Overview](action/index.md) · [Action Engine](action/action-engine/index.md) · [Action Catalog](action/action-catalog/index.md) · [Action Delivery](action/action-delivery/index.md)

---

### Runners
Execution contexts abstracting AWS Lambda, Fargate, Glue, and EC2 so logic remains portable.

**Pipeline touchpoints**
- Pipeline manifests select runner type and network profile.
- Orchestration triggers runs on chosen runners with consistent telemetry and evidence.

**Start here**
- [Runners Overview](runners/index.md) · (see specific runner classes under Runners)

---

### Data Utilities
Shared reference data and helpers that pipelines depend on.

**Pipeline touchpoints**
- **Calendar Service** standardizes fiscal calendars, holidays, and working days for backfills and KPI windows.

**Start here**
- [Utilities Overview](utilities/index.md) · [Calendar Service](utilities/calendar-service/index.md)

---

## Responsibilities & Non‑Goals (checklist per module)
- **Owns**: clear capability surface, SLIs/SLOs, and runbooks.
- **Exposes**: stable APIs, schemas, and UI where applicable.
- **Integrates**: emits traces/metrics/logs; participates in evidence and lineage.
- **Does not**: duplicate pipeline logic, bypass governance, or leak cross‑tenant data.

## Operational Readiness (gate)
- Contracts reviewed and versioned · Access scopes mapped · Evidence on writes · Alerts wired · Rollback steps documented.
