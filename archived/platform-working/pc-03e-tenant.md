# Data Plane Component — Tenant App (Delivery & Customization)

## Purpose
The Tenant App is the **delivery interface** of the Data Plane.  
It exposes governed KPIs and datasets to end users through dashboards, APIs, and exports.  
It also provides controlled flexibility, allowing tenants to extend global definitions with local overlays and proprietary sources, without breaking governance.

## Responsibilities
- **User-facing delivery** — provide dashboards, APIs, and exports for tenants to access KPIs and reports.  
- **Customization** — apply tenant-specific overlays and extensions to global GDP/KPI definitions, within approved governance boundaries.  
- **Quota & residency enforcement** — enforce limits and regional residency rules defined in the Control Plane.  
- **RBAC enforcement** — apply tenant-level role and permission models for secure access.  
- **Operational guardrails** — enforce safety rails (e.g., query limits, data export restrictions) to protect system performance and compliance.

## Non-Goals
- No contract authoring or governance workflows — those belong to the Host App in the Control Plane.  
- No canonical contract storage — Schema Services owns contract definitions.  
- No orchestration of execution plans — that is the role of PHS Control APIs.  

## Flows
1. **Provisioning** — tenant environment is instantiated during onboarding, triggered by Host App governance approval.  
2. **Configuration** — quotas, residency, calendars, and RBAC rules are applied.  
3. **Customization** — overlays and extensions are added, enabling tenant-specific schemas or proprietary data sources.  
4. **Access** — tenants consume KPIs and reports through dashboards, APIs, and exports.  
5. **Monitoring** — observability and compliance hooks ensure usage stays within approved guardrails.  

## Why This Matters
Without a controlled delivery layer, tenants would build their own disconnected pipelines, leading to shadow IT and compliance risks.  
By centralizing delivery through the Tenant App:
- **Executives** receive consistent metrics across all tenants.  
- **Tenants** gain flexibility without sacrificing governance.  
- **Auditors** get defensible evidence that every customization and dataset adheres to approved policies.  

The Tenant App ensures the platform is **governed, flexible, and tenant-safe**.
