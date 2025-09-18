# KPI Services — Data Model

## Purpose
The KPI Data Model defines how KPIs are stored, versioned, and exchanged across the platform.  
It ensures KPI definitions and results are consistent, auditable, and always tied back to GDP inputs.  

---

## Dependency on GDP
- KPI contracts must reference GDP entities (e.g., Calendar, Currency, Org Hierarchy).  
- No KPI definition may reference Raw contracts directly.  
- GDP provides the canonical, business-aware base for all KPI formulas and results.  

---

## Core Entities

### KPI Definition
- Unique identifier, name, description, owner, and purpose.  
- References GDP entities as inputs.  
- Includes version metadata (major, minor, patch).  

### KPI Formula
- Expression built using GDP attributes.  
- Includes dimensional filters (e.g., by region, product).  
- Stored as metadata for reproducibility.  

### KPI Result
- Computed values for a KPI version.  
- Includes timestamp, execution ID, and lineage to GDP inputs.  
- Supports annotations for validation outcomes.  

### Threshold
- Defines acceptable ranges or limits for a KPI.  
- Linked to validation outcomes and alerts.  

---

## Relationships
- **KPI Definition → Formula**: Every KPI definition must have one or more formulas.  
- **KPI Definition → Threshold**: Thresholds are optional but recommended.  
- **KPI Definition → Result**: Each execution produces one or more KPI results.  
- **Result → GDP Inputs**: Every result is linked back to the GDP entities used in the formula.  

---

## Example Schema (Simplified)

| Table | Key Fields | Notes |
|-------|------------|-------|
| **kpi_definitions** | kpi_id, name, version, owner, description | Stores KPI metadata |
| **kpi_formulas** | formula_id, kpi_id, expression, gdp_refs | Stores computation logic |
| **kpi_thresholds** | threshold_id, kpi_id, rule, operator, limit | Stores validation thresholds |
| **kpi_results** | result_id, kpi_id, value, timestamp, lineage_id, validation_status | Stores computed values |
| **kpi_lineage** | lineage_id, gdp_entities, execution_id | Captures GDP inputs used |

---

## Governance Notes
- All entities are versioned; no retroactive edits are allowed.  
- Results without lineage to GDP inputs cannot be published.  
- Schema changes must follow the same contract rules as GDP and KPI services.  

---

## Architectural Reference
The KPI Data Model implements the **ADR-0003 Three-Contract Model**, where:  
- GDP contracts provide canonical inputs.  
- KPI contracts define formulas, thresholds, and results.  
- All relationships are metadata-driven and version-controlled.  

---

This data model ensures that every KPI result is **traceable, reproducible, and auditable**, built only on GDP entities.
