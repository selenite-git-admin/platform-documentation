# Control Plane Component — Host App

## Purpose
The Host App is the **governance UI** of the Control Plane.  
It provides the workflows and evidence model for drafting, reviewing, approving, and publishing contracts, while also managing tenant-level governance metadata.

## Responsibilities
- **Governance workflows** — draft → review → approve → publish contract lifecycle.  
- **Audit evidence** — record who approved what, when, and why.  
- **Tenant metadata** — quotas, residency flags, calendars, RBAC assignments.  
- **Read-only visibility** — surface orchestration status from PHS Control APIs.

## Non-Goals
- Do not define or store canonical contracts (Schema Services owns this).  
- Do not compile or deploy plans (PHS Control APIs handle this).  
- Do not execute data workloads or deliver dashboards (Data Plane scope).  

## Why This Matters
Governance cannot live in emails, spreadsheets, or memory.  
The Host App ensures that approvals, evidence, and tenant governance metadata are captured in one defensible system, giving executives, auditors, and engineers a single source of governance truth.
