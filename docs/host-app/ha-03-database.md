# Host App — Database (Governance Metadata)

## Purpose
Defines the database responsibilities of the Host App.  
The Host App Admin DB is the authoritative store for **governance metadata** — approvals, audit events, tenants, reference data, and RBAC — but it does not persist the canonical contract bodies.  
Contracts themselves live in **Schema Services / Platform Services (PHS)**, with Host App maintaining references for traceability.

## Entities
The Admin DB manages:
- **Approvals** — who approved, when, why (multi-party sign-off).  
- **Audit Events** — immutable evidence of governance actions, linked to contract versions in Schema/PHS.  
- **Draft Intents** — transient states of contracts under authoring; stored as proposals/diffs, not authoritative bodies.  
- **Tenants** — IDs, residency flags, quotas, and lifecycle status.  
- **Reference Data** — calendars, FX policies, organizational hierarchies.  
- **RBAC Assignments** — users, roles, and policies scoped to Host App.  
- **Linkages** — stable IDs pointing to Schema/PHS contract versions for end-to-end lineage.

## Storage Model
- **Relational Database** — structured governance metadata (tenants, approvals, RBAC).  
- **Object Store** — large artifacts such as approval bundles, diffs, or evidence exports.  
- **References, not bodies** — canonical contract content is stored in Schema/PHS; Host App DB only holds linkages and governance metadata.

## Design Tenets
- **Immutability:** approvals and audit events cannot be altered.  
- **Traceability:** every Host App record links to a platform contract version.  
- **Residency-aware:** tenant records carry residency flags enforced at DB level.  
- **Least Privilege:** RBAC metadata enforces strict separation of duties.  

## Integration
- **Schema Services** — provides contract validation and version IDs.  
- **PHS** — consumes published contracts; Host App DB records approval lineage.  
- **UI/API** — workflows for draft, review, approve, publish, all backed by Admin DB.  
- **Audit Exports** — bundles governance metadata + linked platform contracts for compliance.  

## Why This Matters
Without a dedicated governance database, approvals and audits would be scattered across systems, making compliance defensibility impossible.  
By separating governance metadata from canonical contract storage, the Host App maintains clarity: **platform enforces, Host App governs**.
