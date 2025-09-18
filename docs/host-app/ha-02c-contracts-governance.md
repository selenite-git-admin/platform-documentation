# Host App — Contracts Governance

## Purpose
Defines how contracts are authored, validated, and published through the Host App.  
Contracts are the authoritative definition of platform state across Raw, GDP, and KPI layers.

---

## Governed Objects
- **Contract lifecycle actions** (draft/review/approve/publish) executed via control-plane APIs.  
- **Governance metadata** for those actions (who/what/when/why, diffs, approvals).  
- Reference policies surfaced in UI (residency, calendars, FX) but enforced by platform services.

> Note: **Contract bodies and versions are persisted in Schema/PHS metadata stores**, not in Host App.

---

## Lifecycle
1. **Draft** — created/edited in Host App UI; saved as *draft intents*, not authoritative bodies.  
2. **Review** — validations and diffs retrieved from platform; approvers act in Host App.  
3. **Approve** — approvals captured in Host App (governance metadata).  
4. **Publish** — Host App issues publish request to platform APIs; **platform persists the new version**.

All steps are audited in Host App; the **authoritative version** lives in the platform metadata stores.

---

## Guardrails
- KPIs must reference GDP, not Raw.  
- Contracts are immutable once published.  
- Cross-contract validation ensures consistency.  
- Promotion requires explicit approvals.  

---

## Evidence
- Logs capture **who**, **what**, **when**, **why**.  
- Evidence bundles approvals, diffs, and policies.  
- Fully exportable for audits.  

---

## Why This Matters
Contracts sit at the heart of platform trust. Without strict governance, KPI integrity and compliance enforcement would collapse.  
The Host App ensures contracts are transparent, versioned, and auditable across environments.
