# Platform Working — Data Plane

## Purpose
The Data Plane defines **where the platform actually does the work**.  
It holds tenant data across all stages — from raw ingestion to governed Golden Data Points (GDP) and derived KPIs — and exposes results through tenant-facing applications.  
In short: the Data Plane turns **approved contracts** into **executed workloads and consumable insights**.

---

## Layers
The Data Plane is organized into four primary layers:

- **Bronze (Raw)**  
  Landing zone for ingested data. Immutable, minimally processed, and often schema-on-read.  
  Supports both global sources (ERP, CRM, HRMS) and tenant-specific proprietary sources.  

- **Silver (Processed)**  
  Standardized staging aligned to business keys.  
  Cleans, deduplicates, and structures Bronze data in preparation for GDP mapping.  

- **Gold (GDP)**  
  Governed Golden Data Points — the standardized, human-readable entities defined in contracts.  
  GDP ensures cross-tenant consistency, serving as the “source of truth” for KPIs.  
  Tenant overlays and extensions are resolved here under governance.  

- **KPI (Results)**  
  Derived metrics based only on GDP entities.  
  Includes thresholds, anomaly checks, and validation results.  
  KPIs are the consumable layer exposed to executives and business teams.  

---

## Components
The Data Plane includes both execution and delivery components:

- **PHS Execution**  
  Executes materialization plans compiled by the Control Plane.  
  Handles transformations, data quality enforcement, and anomaly detection.  

- **Tenant App**  
  The delivery layer where tenants access dashboards, APIs, and exports.  
  Enforces quotas, residency, and RBAC policies inherited from the Control Plane.  
  Hosts tenant-specific overlays, extensions, and configurations.  

---

## Responsibilities
The Data Plane is responsible for:
- Ingesting and storing tenant business data.  
- Executing transformations defined by approved contracts.  
- Applying data quality and anomaly rules at runtime.  
- Delivering KPIs, dashboards, APIs, and exports to tenants.  
- Retaining data in compliance with residency and retention policies.  

---

## Non-Goals
The Data Plane does not:
- Manage contract lifecycle or governance workflows.  
- Approve or validate schema changes.  
- Record audit evidence of approvals.  

All of those functions are the domain of the Control Plane.

---

## Flows
1. **Ingest** — data lands in Bronze, from global and tenant-specific sources.  
2. **Process** — Bronze data is cleaned and standardized into Silver.  
3. **Govern** — Silver is mapped into GDP (Gold), applying overlays and extensions.  
4. **Compute** — KPIs are derived from GDP, with thresholds and anomaly rules enforced.  
5. **Deliver** — Tenant App exposes KPIs and data products via dashboards, APIs, and exports.  

---

## Why This Matters
Without a clear Data Plane, workloads fragment across tenants, leading to inconsistent metrics, shadow IT, and compliance blind spots.  
By structuring data into Bronze, Silver, Gold, and KPI layers, and delivering through the Tenant App:
- **Executives** get consistent, trustworthy metrics.  
- **Tenants** get flexible but governed customizations.  
- **Auditors** get evidence that data handling aligns with approved contracts and policies.  

The Data Plane ensures the platform is **trustworthy, scalable, and consumable**.
