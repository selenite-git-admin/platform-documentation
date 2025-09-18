# Host App — Observability (Read-only Health)

## Purpose
Provides read-only visibility into platform health.  
The Host App enables governance users to view health metrics without exposing operational controls.

---

## Scope
- Dashboards for jobs, latency, usage, and storage.  
- Metrics collected from telemetry pipelines.  
- Alerts surfaced with severity and timestamps.  
- Audit linkage between observability and evidence.  

---

## Limits
- No restart, retry, or re-run.  
- No scaling or infra mutation.  
- Operational triage delegated to PHS.  

---

## Data Sources
- Telemetry Collector ingests metrics from PHS and Schema Services.  
- Data is normalized and aggregated for dashboards.  
- Metrics consistent across tenants and environments.  

---

## Design Tenets
- Separation of Duties: governance vs. operations.  
- Consistency: stable metric definitions.  
- Least Privilege: governance needs only view access.  
- Traceability: metrics tied to audit evidence.  

---

## Why This Matters
Observability without control prevents scope creep.  
Governance users gain visibility into health trends, while operational responsibility remains with Platform Services.
