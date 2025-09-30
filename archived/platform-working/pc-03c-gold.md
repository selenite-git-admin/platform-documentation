# Data Plane Layer — Gold (GDP)

## Purpose
The Gold layer holds the **Golden Data Points (GDP)** — standardized, human-readable entities that represent the organization’s source of truth.  
This is where processed data (Silver) is mapped into governed business concepts that CFOs, auditors, and executives can trust.  
GDP is the bridge between raw system data and the KPIs that drive decisions.

## Responsibilities
- **Entity definition** — represent key business concepts (customers, vendors, accounts, invoices, orders) in standardized form.  
- **Governance enforcement** — apply approved contracts from Schema Services; ensure transformations follow validated rules.  
- **Tenant overlays and extensions** — allow each tenant to extend global GDP definitions with local fields or proprietary sources, under governance.  
- **Consistency** — provide uniform semantics across tenants, regions, and time.  
- **Audit traceability** — preserve full lineage back to Silver and Bronze records.

## Non-Goals
- No direct KPI computation — GDP is the input to KPI, not the output.  
- No raw data storage — that is Bronze.  
- No direct tenant-facing dashboards or APIs — delivery happens through the Tenant App.  

## Flows
1. **Input** — standardized Silver data flows into GDP pipelines.  
2. **Map** — fields are transformed and mapped to governed GDP entities.  
3. **Overlay** — tenant-specific extensions are layered in, preserving global standards while allowing customization.  
4. **Validate** — GDP contracts and rule packs ensure conformity and completeness.  
5. **Publish** — GDP entities become the only permissible source for KPI derivation.  

## Why This Matters
GDP is where the platform earns the “gold” in data quality.  
By creating governed, standardized entities:
- **Executives** can compare metrics across time, regions, and tenants without ambiguity.  
- **Engineers** can build KPI pipelines without reinterpreting business logic each time.  
- **Auditors** can verify that KPIs are derived from approved, immutable contracts.  

The Gold layer ensures the platform is **standardized, governed, and business-aligned**.
