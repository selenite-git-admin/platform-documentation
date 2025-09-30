# Host App — Reference Data (Calendars, FX, Organization)

## Purpose
Defines how the Host App manages enterprise reference data for governance purposes.  
Reference data provides context for contracts and KPIs (e.g., fiscal calendars, exchange rates, org hierarchies) but is **not operationally authoritative**.  
The Host App captures governance-approved settings that are consumed downstream by Schema/PHS.

## Reference Data Types
- **Fiscal Calendars** — start/end dates, fiscal periods, holidays, and cut-offs.  
- **Foreign Exchange (FX) Policies** — reference currencies, update frequency, governance of rates.  
- **Organizational Hierarchies** — companies, divisions, cost centers, reporting structures.  

## Governance Model
- Data stewards propose updates in Host App UI.  
- Approvers validate and authorize changes.  
- Metadata stored in Admin DB; authoritative values fetched or validated in PHS/Schema.  
- Evidence of every approval logged for audit.  

## Why This Matters
CFO packs, KPI thresholds, and compliance reports depend on consistent reference data.  
By governing calendars, FX, and org structures centrally, the Host App ensures alignment without duplicating operational systems.
