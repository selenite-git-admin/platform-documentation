# KPI Materialization

## Purpose
The KPI Materialization stage transforms Golden Data Points (GDPs) into Key Performance Indicators (KPIs). KPIs represent the measurable outcomes that executives and business teams rely on to make decisions. This stage ensures that KPI definitions are consistent, tested, and reproducible across environments.

## Context
Enterprises often define KPIs differently across departments, leading to conflicting reports. BareCount solves this by treating KPIs as code. Each KPI is declared in a manifest, version controlled, tested against expectations, and reconciled with systems of record. KPI materialization is not a one-off report but a governed process that produces reliable metrics for consumption and activation.

## Key Capabilities

### KPI as Code
- Each KPI has a declarative specification in the catalog.  
- Specifications define source GDPs, calculation logic, acceptance thresholds, and output schema.  
- KPI code is stored in version control and deployed through the same pipeline framework as GDPs.

### Versioning and Lineage
- Each KPI has a version tag tied to the manifest and calculation logic.  
- When definitions change, new versions are created without overwriting historical runs.  
- Evidence Ledger entries link KPI outputs to GDP versions, code versions, and contract versions.

### Validation and Testing
- KPIs include validation tests to ensure correctness.  
- Tests cover expected ranges, reconciliation against system totals, and edge-case handling.  
- Runs that fail acceptance tests are flagged, quarantined, and escalated to governance.

### Acceptance Thresholds
- Each KPI defines thresholds for completeness and accuracy.  
- For example, a revenue KPI may require 99.5 percent match with ERP totals.  
- Thresholds are enforced automatically and surfaced in observability dashboards.

### Reconciliation with Systems of Record
- KPI materialization includes reconciliation checks against declared systems of record.  
- Differences beyond thresholds trigger alerts and governance review.  
- Reconciliation results are recorded in the Evidence Ledger.

### Publishing
- KPIs are materialized into the KPI Store, partitioned by time period and version.  
- Published KPIs are accessible through APIs, exports, and activation workflows.  
- Each publication includes metadata for lineage and evidence.

## Operating Model
- KPI definitions are authored in code, peer reviewed, and deployed through pipelines.  
- Each run produces both KPI values and validation artifacts.  
- Failed validations block publication until governance reviews.  
- Consumers always access KPIs from the KPI Store, never directly from transformations.

## Example
The Gross Margin KPI is defined using GDPs for Revenue and Cost of Goods Sold. The specification requires a 99.9 percent match with ERP totals. During a run, the KPI calculation detects a mismatch of 0.3 percent. The run is quarantined, alerts are sent, and governance investigates whether late cost entries caused the variance. Once resolved, the KPI is recomputed and published with full lineage.

## Notes
KPI Materialization transforms governed data into governed outcomes. Treating KPIs as code ensures that definitions are transparent, versioned, and auditable. This prevents misalignment across departments and builds trust in the numbers used for decisions.
