# Host App — Summary

## Purpose
Summarizes the role of the Host App (PHA) in the platform architecture.  
The Host App provides the **UI and control plane for governance**, covering contract lifecycle orchestration, tenant management, reference data, audit, and RBAC.  
It does **not** persist or enforce contracts — those functions belong to Schema Services and Platform Services (PHS).

## Responsibilities
- **UI & Control for Contracts** — draft, review, approve, publish (via APIs).  
- **Governance Metadata** — approvals, audit events, RBAC, tenants, and reference data.  
- **Read-only Observability** — health dashboards and telemetry views.  
- **SLAs & Error Model** — service-level targets and consistent error handling.  
- **Non-goals** — no infrastructure provisioning, no pipeline execution, no contract persistence.

## Architecture Highlights
- **UI Layer** — governance console for lifecycle workflows.  
- **API Gateway** — exposes control-plane endpoints.  
- **Admin DB (ADR-0004)** — relational store for governance metadata (tenants, approvals, audit, refdata, RBAC) and linkages to Schema/PHS contracts.  
- **Object Store** — artifacts such as approval bundles and evidence exports.  
- **Observability** — dashboards with strict read-only boundaries.

## Integration
- **Schema Services** — validate contracts; store canonical versions.  
- **Platform Services (PHS)** — enforce contracts; run provisioning/orchestration.  
- **KPI Services** — consume KPI definitions (hosted in Schema/PHS).  
- **Tenant App** — handles onboarding and infra; Host App governs metadata only.

## Why This Matters
The Host App ensures governance processes are consistent, auditable, and transparent.  
By centralizing control-plane interactions and metadata, it gives compliance and executive teams confidence while leaving enforcement to the platform core.

## Next Steps
- Ensure diagrams reflect separation: *Host App (UI/governance)* vs *Schema/PHS (persistence/enforcement)*.  
- Cross-link summary with schema-summary.md and phs-summary.md for end-to-end lifecycle traceability.  
