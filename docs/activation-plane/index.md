# Activation Plane — Overview

## Purpose
The Activation Plane is the last-mile execution layer of the platform.  
It ensures that insights produced by KPI Services are not just observed but activated — translated into governed, auditable, and real-world actions inside tenant systems.

## Why It Exists
Most BI and analytics platforms stop at reporting. Decisions remain locked in dashboards, leaving the “action” to fragmented tools or manual follow-up.  
The Activation Plane closes this loop: **Schema → KPI → Tenant → Activation**.

## Responsibilities
- **Flows Engine:** Execute event-driven, scheduled, or manual activations.  
- **Reverse-Connectors:** Safely write outcomes back into tenant core systems (ERP, CRM, HRMS, DMS).  
- **Governance:** Enforce quotas, approvals, RBAC, and policy checks before every action.  
- **Observability:** Log, audit, and replay all actions for compliance.  
- **Tenant Integration:** Surface actions inside the Tenant App as **activation panels**.  

## Boundaries
- **Consumes:** KPI outputs and governed GDP data.  
- **Depends on:** Platform Runtime (PHS) for secrets, retries, DLQ, audit storage.  
- **Peers:** Tenant App (presentation), KPI Services (input), Host App (governance).  
- **Excludes:** Schema definition, KPI computation, infra orchestration (delegated to other layers).

## Non-Goals
- Not a workflow engine for arbitrary processes.  
- Not a replacement for ERP/CRM functionality — it augments them with governed triggers.  
- Not designed for bulk ETL/ELT pipelines (handled by ingestion and processing layers).

## Value
The Activation Plane transforms the platform from descriptive analytics to operational intelligence:  
- Reducing the gap between insight and execution.  
- Embedding governance into every action.  
- Making decisions **real, repeatable, and compliant**.
