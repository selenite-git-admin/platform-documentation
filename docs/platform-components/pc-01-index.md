# Platform Working — Overview

## Purpose
The Platform Working section explains **what the platform is composed of and why it is structured this way**.  
It describes the Control Plane, Data Plane, and Cross-Cutting services — their responsibilities, flows, and boundaries.  
This section is intentionally **about the “what” and “why”**: the high-level flows and integration points.

The **“how”** — detailed mechanics, schemas, KPIs, UIs, and APIs — are documented in their respective component sections:

- [Schema Services](../schema/index.md) — how contracts are defined and validated.  
- [KPI Services](../kpi/kpi-01-overview.md) — how GDP entities translate into KPIs and thresholds.  
- [Host App](../host-app/ha-01-overview.md) — how governance, approvals, and evidence are managed.  
- [Tenant App](../tenant/index.md) — how tenants consume KPIs and apply overlays.  
- [PHS](../phs/phs-01-overview.md) — how orchestration and plan execution are carried out.  
- [APIs](../apis/) — how integration is exposed to external systems.  

---

## Sections
The Platform Working documentation is organized into three domains:

- **Control Plane**  
  Governance and intent-setting: 
- [Schema Services](../schema/index.md), 
- [Host App](../host-app), 
- [PHS Control APIs](pc-02a-phs-control.md).  

- **Data Plane**  
  Execution and delivery: 
- Bronze → Silver → [Gold/GDP](pc-03c-gold.md) → KPI → [Tenant App](../tenant/index.md).  

- **Cross-Cutting**  
  Shared services: 
- [Data Quality & Anomalies](pc-10-dqc.md), 
- [Alerts & Monitoring](pc-11-alerts.md), 
- [Residency & Compliance](pc-12-residency.md), 
- [Security & RBAC](pc-13-security.md), and 
- [Runtime Foundations](pc-14-orchestration.md).  

---

## Why This Matters
Separating **“what/why” (Platform Working)** from **“how” (component docs)** makes the documentation navigable and sustainable.  
Readers can understand the big picture first, then drill into the mechanics only when needed.  
This mirrors AWS’s architectural style — principle-driven overviews, backed by deep-dive component references.
