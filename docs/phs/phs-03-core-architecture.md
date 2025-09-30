# Platform Host Services (PHS) — Core Architecture

## Purpose
Describe how PHS operates at runtime across ingress, processing, serving, and egress.  
Focus areas: contract enforcement (Raw, GDP, KPI), Schema Services, shared/common services, outbound controls, audit/lineage.  
PHS does **not** store tenant business data. Lifecycle (seed/modify/approve) happens in **PHA**; PHS only stores and enforces **published** contracts.

## Components (Runtime View)

### 1) Control-Plane Kernel
- Active contract store: Raw, GDP, KPI (published versions only; Major–Minor–Update metadata).
- Policy decision points (PDP) for ingress, normalization, KPI build, delivery, and egress.
- Evidence & lineage ledger (immutable records with `supersedes` pointers; evaluation results).

### 2) Schema Services (Core Differentiator)
- Contract & schema registry for Raw/GDP/KPI.
- Mapping engine for Raw→GDP canonicalization (FX, UoM, calendars, org hierarchies, locations, grades).
- Validation services:
  - **Raw**: schema/keys/partitions/freshness/volume.
  - **GDP**: reference integrity/conformance checks.
  - **KPI**: formula/inputs/grain/thresholds.
- Exposes read-only surfaces to runtime; writes come from PHA on publish.

### 3) Common Shared Services
- Identity & Access (IAM, RBAC/ABAC), Tenancy Manager.
- Configuration service (versioned; env/tenant overlays).
- Secrets & Key Management (issuance, rotation, envelope encryption).
- Observability hub (metrics, logs, traces, SLO dashboards).
- Orchestration & Scheduling (jobs, retries, idempotency).
- Storage fabric controls (object/relational/cache/stream), residency & retention enforcement.
- API Gateway + Ingress/Egress enforcement (authN, quotas, throttling).

> Access model: Only **Platform Super Admin** touches PHS directly (CLI/CDK/CICD). PHA and tenants call via scoped APIs.

## Architecture Flows

### A) Ingress (Raw Contract Enforcement)
**Path:** Connector → API Gateway → Ingress Enforcement → Landing (outside PHS data stores)  
**Checks (PDP):**
- Contract match (source id, contract id/version).
- Schema & key validation; partition/calendar alignment.
- Freshness & volume thresholds; quarantine on breach.
**Outputs:**
- Accept/reject decision; evaluation event with evidence id.
- Lineage record (source→contract version→ingress batch/run id).
**Shared services used:** Gateway, IAM, Secrets, Observability, Schema Services (Raw validations).

### B) Normalization (Raw → GDP)
**Path:** Orchestrator job → Schema Services validations → Canonicalize → GDP zone (tenant domain)  
**Checks (PDP):**
- Mapping tables in effect (FX, UoM, calendars, org hierarchies).
- Conformance to GDP schema; reference integrity.
- Residency and retention policy application.
**Outputs:**
- GDP conformance report; lineage hop (Raw batch → GDP dataset/version).
- Evidence artifacts for audit.
**Shared services used:** Orchestrator, Config, Secrets, Observability, Storage fabric controls, Schema Services (GDP checks).

### C) KPI Build & Serving (GDP → KPI)
**Path:** KPI builder → KPI validation → Publish to serving layer → Deliver to consumers  
**Checks (PDP):**
- KPI contract: formula, inputs (GDP datasets/versions), grain, filters.
- Threshold policies & alert rules.
- Delivery SLOs (latency/freshness).
**Outputs:**
- KPI publish event with contract/version; threshold evaluation events.
- Delivery records per channel (API/BI/export) with lineage pointers.
**Shared services used:** Orchestrator, Observability, Storage fabric controls, Gateway, Schema Services (KPI checks).

### D) Egress (Governed Exports)
**Path:** Serving layer → API Gateway/Egress Enforcement → External target  
**Checks (PDP):**
- Contract present for export (KPI or governed dataset).
- Quotas/rate limits; residency & retention constraints.
- Signature, TLS/mTLS, domain/IP allowlists.
**Outputs:**
- Export audit record (contract id/version, target, volume, checksum).
**Shared services used:** Gateway, IAM/Secrets, Observability, Policy/Compliance.

### E) Operations & Health
- **Observability:** Per-checkpoint SLI/metrics: validation latency, acceptance rate, quarantine rate, KPI build time, egress success rate.
- **Backpressure:** Quarantine queues with TTL; retry budgets and exponential backoff; circuit breakers at gateway.
- **Drift/Config:** Detect drift in contract bindings and reference tables; emit `policy.changed` events.

### F) Provisioning & Change
- **Infra:** Deployed via CDK by Super Admin; no console edits.
- **Contracts:** Published by PHA; PHS persists active versions and begins enforcement immediately (idempotent activation).
- **Versioning:** Major (breaking), Minor (compatible), Update (non-structural). All runtime decisions include the contract version triplet.

## Outbound Connectivity (Data Connectors)
- **Network:** Private subnets + NAT gateways; VPC endpoints for AWS services; PrivateLink to partners; optional egress proxy.
- **Policy:** Deny-by-default egress; per-connector allowlists (domain/IP), TLS/mTLS, DNS pinning, request signing.
- **Controls:** Gateway quotas/throttling; per-connector IAM roles + short-lived creds; audit per request with contract/version id.
- **Observability:** Connector dashboards (latency, error %, throughput); alarms; anomaly detection on volumes/freshness.

## Events & Audit (Illustrative)
- `ingress.validated` (Raw) — result, evidence id, contract/version, batch/run id.
- `gdp.conformed` (GDP) — reference map versions, conformance score, lineage hop id.
- `kpi.published` (KPI) — formula hash, inputs, delivery SLOs, publish id.
- `egress.exported` — destination, volume, checksum, policy result.
- `policy.changed` — affected contracts/mappings, rollout window.
- All events correlate to immutable audit entries and are queryable by contract/version/run.

## Failure Modes & Handling
- **Schema drift at ingress:** Reject/quarantine; raise `ingress.validation_failed`; connector notified.
- **Reference map missing/stale:** Block GDP conformance; emit `gdp.conformance_failed`; roll back to last good map.
- **KPI formula error:** Do not publish; emit `kpi.publish_failed`; keep last known good.
- **Egress policy breach:** Block export; emit `egress.policy_denied`; require allowlist change via CDK.

## Dependencies & Boundaries
- **PHA (Admin App):** Owns contract lifecycle and tenant governance; on publish, writes to PHS.  
- **PHS (this doc):** Enforces only **published** contracts; provides shared/common services.  
- **Tenant infra/app:** Receives governed datasets/KPIs; isolation and residency handled in tenant domain with PHS policy checks at boundaries.

## Diagrams (placeholders)
- **Runtime enforcement map:** Raw→GDP→KPI with PDP checkpoints and event flows.  
  `![PHS Runtime Enforcement](../images/phs-core-architecture-runtime.png)`  
- **Outbound connectivity topology:** NAT/Endpoints/PrivateLink + egress policy points.  
  `![PHS Egress Topology](../images/phs-core-architecture-egress.png)`

## End State
All data paths (ingress, normalization, KPI, egress) are governed by **published** contracts.  
Schema Services delivers contract-aware validations; common services apply identity, policy, secrets, and observability uniformly.  
PHS remains a durable kernel — API-first, automation-friendly, and independent of PHA availability.
