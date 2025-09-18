# Platform Working — Control Plane

## Purpose
The Control Plane defines **how the platform decides what should happen**.  
It is where contracts are authored and validated, governance decisions are captured, and orchestration turns approvals into executable plans.  
In short: the Control Plane transforms **business intent** into **technical reality**.

---

## Components
The Control Plane is made up of three core services:

- **Schema Services**  
  The canonical store for all contracts — Raw, GDP, and KPI.  
  Provides compatibility checks, rule packs (data quality, anomaly detection), and schema validation.  
  Every change here is versioned and immutable.

- **Host App**  
  The governance UI and workflow engine.  
  Allows stakeholders to draft, review, approve, and publish contract changes.  
  Stores governance metadata — approvals, audit trails, RBAC assignments, tenant quotas — but not the contract bodies themselves.

- **PHS Control APIs**  
  The orchestration interface.  
  Compiles approved contracts into materialization plans.  
  Manages rollout to the Data Plane, including dual-run, compare, and rollback capabilities.  
  Provides status back to Host App for governance visibility.

---

## Responsibilities
The Control Plane is responsible for:
- **Contract lifecycle** — drafting, validation, approval, and publication.  
- **Governance enforcement** — ensuring only approved changes reach execution.  
- **Audit evidence** — recording who approved what, when, and why.  
- **Orchestration** — turning approved contracts into actionable deployment plans.  

---

## Non-Goals
The Control Plane does not:
- Store tenant business data.  
- Execute pipelines or transformations.  
- Serve dashboards, APIs, or exports to tenants.  

All of those functions are the domain of the Data Plane.

---

## Flows
1. **Draft** — a contract change is created in Host App.  
2. **Validate** — Schema Services runs compatibility checks and validation rules.  
3. **Approve** — governance workflow in Host App records approvals and audit evidence.  
4. **Orchestrate** — PHS Control APIs compile the contract into an executable plan.  
5. **Rollout** — the plan is deployed to the Data Plane, with status fed back into Host App.  

---

## Why This Matters
Without a Control Plane, decisions about data structures and KPIs would be scattered across scripts, dashboards, and tribal knowledge.  
By centralizing contracts, governance, and orchestration here:
- **Executives** can trust that KPIs are consistent and auditable.  
- **Engineers** can trust that execution is based on validated, approved contracts.  
- **Auditors** can trust that evidence of governance is immutable and defensible.  

The Control Plane ensures the platform is **explainable, repeatable, and compliant**.
