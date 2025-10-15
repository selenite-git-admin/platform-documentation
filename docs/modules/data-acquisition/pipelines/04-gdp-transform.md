# GDP Transform

## Purpose
The GDP Transform stage standardizes raw data into Golden Data Points (GDPs). GDPs represent the governed, contract-bound entities that form the foundation for KPI materialization. This stage ensures that enterprise data is consistent, reconciled, and ready for analytic consumption.

## Context
Raw data contains inconsistencies, duplicates, and system-specific noise. If KPIs are computed directly from raw inputs, results are unreliable and non-reproducible. BareCount introduces the GDP layer to enforce consistency and contract alignment. GDPs are defined once, centrally, and reused across KPIs and domains. This allows finance, sales, and operations to share the same truth without building parallel pipelines.

## Key Capabilities

### Conformance to Contracts
- GDP definitions are registered in the Data Contract Registry.  
- Transformations ensure each GDP conforms exactly to its schema and semantics.  
- Non-conforming records are flagged and quarantined with lineage references.

### Deterministic Transformations
- Transform logic must be deterministic and idempotent.  
- Each output GDP is derived from an explicit set of raw records with documented logic.  
- Re-runs always yield the same GDPs for a given set of inputs.

### Join Rules
- GDPs are often composed by joining multiple raw streams (for example, invoices and customers).  
- Join rules must be declared in manifests, with clear handling of nulls and missing keys.  
- Late-arriving join records trigger updates to GDPs, with lineage preserved.

### Survivorship Policies
- When multiple raw sources provide conflicting values, survivorship policies define precedence.  
- Policies may be based on system-of-record designation, timestamp freshness, or quality scores.  
- All applied rules are logged in the Evidence Ledger for audit.

### Handling Late Data
- Late-arriving records are merged into GDPs with version control.  
- GDPs are updated in-place, but previous versions remain traceable in lineage and logs.  
- Contract checks ensure that late records cannot introduce schema drift unnoticed.

### Data Quality Enforcement
- GDP transforms enforce data type consistency, mandatory field population, and referential integrity.  
- Quality violations trigger alerts and block progression to KPI build until resolved.

## Operating Model
- GDP transformations are declared in manifests alongside contract references.  
- Each GDP run records inputs, applied rules, and resulting schema hash in the Evidence Ledger.  
- Orchestration ensures GDPs are recomputed when underlying raw partitions or late data arrive.  
- Downstream KPI builds only consume validated GDPs.

## Example
Customer invoice data from SAP and payment records from a banking system are joined to form a GDP called `InvoiceSettlement`. The manifest defines `InvoiceID` as the join key, with survivorship favoring the SAP system as the system of record. When a late payment record arrives, the GDP is updated with the settlement date. The Evidence Ledger records both the original GDP version and the updated version for traceability.

## Notes
The GDP Transform stage is the cornerstone of BareCount’s trust model. By enforcing contracts, deterministic rules, and lineage, GDPs prevent disputes about the
