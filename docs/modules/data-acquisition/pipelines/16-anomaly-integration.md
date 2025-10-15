# Anomaly Integration

## Purpose
The Anomaly Integration stage embeds anomaly detection into the BareCount Data Action Platform pipelines. It provides automated detection of outliers, drifts, and unusual patterns at every stage of the pipeline, ensuring that KPIs are trusted and actionable.

## Context
Data pipelines cannot assume that source systems always behave consistently. Schema changes, data entry errors, or operational disruptions may introduce anomalies that degrade KPIs. BareCount integrates anomaly detection directly into pipeline workflows. This ensures that anomalies are detected early, contextualized with evidence, and surfaced to operators and governance teams for resolution.

## Key Capabilities

### Schema Drift Detection
- Compares incoming payloads against contract definitions.  
- Flags new, missing, or type-mismatched fields.  
- Schema anomalies trigger DLQ routing and governance review.  

### Statistical Anomalies
- Detects unusual spikes, drops, or distributions in numeric metrics such as record counts or revenue.  
- Uses thresholds defined in contracts or learned from historical patterns.  
- Alerts include context on expected versus observed values.

### Referential Integrity Checks
- Validates relationships between datasets, such as invoice to payment links.  
- Missing or orphaned records are flagged as anomalies.  
- Integrity anomalies help ensure consistency across GDP and KPI stages.

### Business Rule Anomalies
- Contract-defined business rules are applied during transformation.  
- Violations (e.g., negative revenue, future-dated expenses) are flagged.  
- Governance teams can adjust rules or approve exceptions.

### Evidence and Lineage Integration
- All anomaly events are written to the Evidence Ledger.  
- Each anomaly is linked to the specific run ID, contract version, and affected records.  
- This ensures transparency in how anomalies were identified and resolved.

### Automated Routing
- Anomalies are routed to owners defined in manifests.  
- Critical anomalies escalate to incident management systems.  
- Non-critical anomalies are logged for trend analysis and improvement.

## Operating Model
- Developers declare anomaly checks in pipeline manifests.  
- Operators review anomaly dashboards and triage alerts.  
- Governance teams adjust thresholds or contracts based on recurring anomalies.  
- Anomalies are tracked as evidence, ensuring they are auditable and explainable.

## Example
A daily KPI pipeline for Accounts Receivable detects an unusual spike in overdue invoices. Statistical anomaly detection flags a 300 percent increase compared to the historical mean. The anomaly is logged in the Evidence Ledger and an alert is routed to the finance governance team. After investigation, the spike is confirmed as valid due to a system-wide delay in customer payments.

## Notes
Anomaly detection is not an afterthought in BareCount. By embedding anomaly integration into pipelines, the platform ensures that unusual patterns are caught early, explained transparently, and governed effectively. This preserves trust in KPIs even under unexpected conditions.
