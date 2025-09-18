# Host App — Responsibilities & Boundaries

## Purpose
Defines the boundaries of the Host App.  
By clarifying responsibilities and exclusions, this document ensures governance teams know exactly what the Host App owns and what remains external.

---

## Responsibilities
- **UI/control for contracts lifecycle** (draft, review, approve, publish) by invoking platform APIs.  
- Governance metadata: approvals, audit logs, RBAC assignments, tenants, reference data.  
- Read-only observability dashboards for health and usage.

---

## Exclusions
- **Storing or versioning contract bodies** (canonical contracts live in Schema/PHS stores).  
- Enforcing transformations or computations (handled by Schema/KPI/PHS).  
- Infrastructure mutation, pipeline execution, or retries.

---

## Interactions
- **Schema Services** — contract validation and GDP enforcement.  
- **KPI Services** — consumption of KPI definitions.  
- **Platform Services (PHS)** — provisioning and orchestration.  
- **APIs / Control Plane** — exchange of desired state and telemetry.  

---

## Why This Matters
Without clear boundaries, governance tools often grow into operational control surfaces, creating confusion and compliance risk.  
By enforcing scope limits, the Host App provides clarity for auditors, operators, and business users alike.
