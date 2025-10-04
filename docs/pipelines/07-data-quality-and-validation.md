# Data Quality and Validation

## Purpose
The Data Quality and Validation stage enforces trust in the BareCount Data Action Platform. It applies systematic checks across ingestion, GDP transforms, and KPI materialization to ensure data is complete, accurate, and aligned with contracts. This stage prevents poor data from propagating downstream.

## Context
In many enterprises, data quality is treated as an afterthought, checked only when users complain. BareCount integrates validation into every pipeline stage. Each contract defines rules, and violations are detected immediately. Quality checks are classified by severity, with clear actions such as blocking, quarantining, or alerting. This allows enterprises to prevent issues before they affect KPIs or decision-making.

## Key Capabilities

### Contract-Level Checks
- Ingestion validates extractor schemas against registered contracts.  
- Field types, required attributes, and enumerations are verified at the boundary.  
- Drift or violations trigger governance events and block downstream progression.

### GDP Shape Checks
- GDP transforms enforce structural integrity of conformed entities.  
- Checks ensure referential integrity, survivorship consistency, and late-arrival handling.  
- Null or inconsistent joins are flagged with severity tags.

### KPI Acceptance Gates
- KPI runs include acceptance thresholds that must be satisfied before publication.  
- Examples: total revenue KPI must reconcile within 0.5 percent of ERP totals.  
- Runs that fail thresholds are quarantined and escalated.

### Severity and Escalation
- Violations are classified as **blocking** (pipeline stops), **warning** (pipeline continues but alerts), or **informational** (logged only).  
- Blocking errors require governance intervention.  
- Warning errors trigger alerts routed to owners.  
- Informational checks support observability and trend analysis.

### Automated Enforcement
- Quality checks are codified in manifests alongside contracts.  
- Each run executes validation rules automatically.  
- Failures are tied to lineage and recorded in the Evidence Ledger for audit.

## Operating Model
- Validation rules are authored and reviewed alongside contracts and KPI definitions.  
- Quality dashboards track frequency, severity, and resolution time for violations.  
- Metrics such as pass rate, false positives, and remediation cycle time are monitored.  
- Governance teams refine rules as new issues are discovered.

## Example
A GDP for invoices enforces that each record has a valid `CustomerID` and non-null `InvoiceAmount`. During a run, 2 percent of records fail due to missing customer keys. The violation is classified as blocking because referential integrity is broken. The pipeline halts, a governance ticket is raised, and evidence is logged. Once the root cause is addressed, the GDP is recomputed and downstream KPIs proceed.

## Notes
Data quality is not optional. By embedding validation into every stage and linking it to governance, BareCount ensures that KPIs are based on trustworthy data. Quality rules evolve over time, but enforcement is always consistent and auditable.
