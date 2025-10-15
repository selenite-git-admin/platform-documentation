# Observability, SLO, and Alerts

## Purpose
The Observability, SLO, and Alerts stage provides transparency into pipeline operations in the BareCount Data Action Platform. It defines service level objectives (SLOs) for freshness, completeness, and accuracy, and ensures that deviations are detected and routed to the right teams for action.

## Context
Without observability, pipelines become black boxes. Failures or delays go unnoticed until business users complain. BareCount treats observability as a first-class function. Each pipeline stage emits metrics, logs, and lineage entries. SLOs are declared in manifests, and alerts are tied to owners. This ensures that teams know when pipelines are at risk before KPIs are impacted.

## Key Capabilities

### Metrics Emission
- Each run produces standard metrics: start time, end time, duration, record counts, error counts, and success flags.  
- Metrics are tagged with run ID, contract version, and stage.  
- Metrics are available in dashboards and queryable for trend analysis.

### Logs
- Logs capture detailed execution traces, including schema validation outcomes, drift detection, and retry actions.  
- Logs are indexed and searchable for operators and governance teams.  
- Sensitive data is masked before being stored.

### Service Level Objectives (SLOs)
- Freshness SLOs define maximum allowable lag between source updates and KPI availability.  
- Completeness SLOs define the expected percentage of records ingested or processed.  
- Accuracy SLOs define reconciliation thresholds with systems of record.  
- SLOs are enforced per stage and aggregated across pipelines.

### Alerts
- Violations of SLOs trigger alerts.  
- Alerts are routed to owners defined in manifests: connector developers, governance teams, or KPI owners.  
- Alert payloads include run ID, stage, SLO breached, and recommended actions.  

### Dashboards
- Dashboards display pipeline health, trends, and open issues.  
- Users can view freshness, completeness, and accuracy status for each KPI.  
- Dashboards integrate with lineage to allow drill-down into root causes.

## Operating Model
- Each pipeline manifest declares SLOs and owners.  
- Pipelines emit metrics and logs automatically; no manual instrumentation is required.  
- Alerts are integrated with incident management systems for triage.  
- Weekly reviews track SLO adherence and identify recurring issues.

## Example
A pipeline is expected to process invoices within two hours of ingestion. A freshness SLO breach occurs when processing exceeds three hours. The platform generates an alert routed to the finance data engineering team. The alert includes run ID, duration, and the last successful checkpoint. The team investigates and resolves the bottleneck before KPI publication is delayed further.

## Notes
Observability is not optional. By embedding metrics, logs, SLOs, and alerts into pipelines, BareCount ensures that data quality and timeliness are continuously monitored. This builds confidence for executives relying on KPIs for decision-making.
