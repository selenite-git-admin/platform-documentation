# Data Plane Layer — KPI (Results)

## Purpose
The KPI layer is the **results layer** of the platform.  
It derives business metrics exclusively from governed Golden Data Points (GDP), ensuring every calculation is explainable, repeatable, and auditable.  
KPIs are the final consumable outputs that executives and business teams rely on for decisions.

## Responsibilities
- **Metric computation** — derive ratios, aggregates, and indicators from GDP entities.  
- **Thresholds & validations** — apply rule packs for acceptable ranges, anomalies, and exceptions.  
- **Traceability** — link every KPI back to the GDP fields and contracts that produced it.  
- **Presentation prep** — structure KPIs for consumption by Tenant App dashboards, APIs, and exports.  
- **Audit evidence** — store calculation lineage and validation results for compliance reporting.

## Non-Goals
- No ingestion or cleaning of raw data — handled in Bronze/Silver.  
- No entity standardization — handled in Gold/GDP.  
- No direct governance workflow — managed in the Control Plane.  

## Flows
1. **Input** — GDP entities feed into KPI pipelines.  
2. **Compute** — metrics (e.g., liquidity ratios, profitability, compliance flags) are calculated.  
3. **Validate** — thresholds, anomaly rules, and DQC packs are applied.  
4. **Store results** — KPIs are stored with lineage metadata linking back to GDP.  
5. **Deliver** — KPIs are exposed to tenants via dashboards, APIs, and exports through the Tenant App.  

## Why This Matters
Without a KPI layer, every consumer would calculate metrics differently, leading to confusion and mistrust.  
By centralizing KPI computation on top of GDP:
- **Executives** receive consistent, board-ready metrics.  
- **Auditors** can verify results against contracts and evidence.  
- **Engineers** avoid duplicating business logic across reports and applications.  

The KPI layer ensures the platform is **decision-ready, consistent, and defensible**.
