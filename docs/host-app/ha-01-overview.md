# Host App — Overview

## Purpose
The Host App is the control-plane application for the platform.  
It provides governance workflows for contracts, tenants, reference data, and audit evidence.  
The Host App is metadata-driven: it governs state but does not directly provision infrastructure or execute pipelines.

---

## Scope
In scope:
- Contract lifecycle: draft, review, approve, publish (immutable versions).  
- Tenant lifecycle: create, update, suspend, retire.  
- Reference data: fiscal calendars, currencies, organizational hierarchies.  
- RBAC: role assignment and approval workflows.  
- Audit evidence: capture, query, and export.  
- Read-only observability: health dashboards, latency, and usage metrics.  

Out of scope:
- Provisioning or mutating infrastructure.  
- Running or re-running data pipelines.  
- Editing or storing tenant raw business data.  
- Acting as a replacement for Schema Services or Platform Services observability.  

---

## Relationships
- **Schema Services**: enforce Raw → GDP → KPI transformations; Host App governs contract lifecycle.  
- **KPI Services**: consume KPI definitions authored in Host App.  
- **Platform Services (PHS)**: execute provisioning, orchestration, and monitoring.  
- **APIs / Control Plane**: Host App communicates desired state and receives telemetry.  

---

## Document Roadmap
This section is organized into four groups:

- **[Architecture](ha-02-architecture.md)**  
  Core architecture and design, responsibilities and boundaries, RBAC, contracts governance, tenant management, observability, SLAs, and non-goals.  

- **[Database](ha-03-database.md)**  
  Metadata model, reference data, audit evidence, storage and retention policies.  

- **[UI](ha-04-ui.md)**  
  Information architecture, UI screens, UX patterns, and accessibility standards.  

---

## Cross-References
- [Schema Services — GDP Framework](../schema/gdp-framework.md)  
- [KPI Services — Overview](../kpi/kpi-01-overview.md)  
