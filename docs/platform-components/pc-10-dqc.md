# Cross-Cutting — Data Quality & Anomalies

## Purpose
The Data Quality & Anomalies module enforces the reliability and integrity of data across all layers of the platform.  
It applies rule-based validations, statistical checks, and anomaly detection to ensure that data flowing through the Data Plane aligns with approved contracts from the Control Plane.  
This capability is cross-cutting: it operates at ingestion, transformation, and KPI computation stages.

---

## Responsibilities
- **Rule enforcement** — validate datasets against constraints defined in Schema Services (e.g., mandatory fields, value ranges, referential integrity).  
- **Anomaly detection** — flag outliers, unexpected patterns, or metric deviations using statistical or ML-driven models.  
- **Threshold checks** — apply KPI-specific tolerance ranges defined in governance.  
- **Evidence capture** — log validation results, anomalies, and remediation steps as audit artifacts.  
- **Feedback loop** — provide status signals to Host App for governance visibility and to Tenant App for transparency.

---

## Non-Goals
- Does not author or define quality rules (these are governed in Schema Services).  
- Does not decide on remediation actions (owners determine business response).  
- Does not deliver tenant dashboards directly (Tenant App presents outputs).  

---

## Flows
1. **Ingest** — raw data entering Bronze is checked for format compliance.  
2. **Process** — Silver transformations apply cleaning and reference integration validations.  
3. **Govern** — Gold/GDP mappings are validated against contracts and overlays.  
4. **Compute** — KPIs are tested against thresholds and anomaly rules.  
5. **Report** — outcomes (pass, fail, anomaly detected) are logged and surfaced to governance and tenant views.  

---

## Interfaces
- **Schema Services** — provides rule packs and thresholds.  
- **Host App** — displays governance-level quality dashboards and approval evidence.  
- **Tenant App** — shows tenant-facing anomaly alerts and validation summaries.  
- **Telemetry & Lineage** — store validation results and link them to execution runs.  

---

## Why This Matters
Without systematic quality checks, downstream KPIs could silently diverge from reality.  
By enforcing rules and anomaly detection at every stage:
- **Executives** trust that metrics are consistent and accurate.  
- **Engineers** can detect and remediate data issues before they corrupt downstream outputs.  
- **Auditors** gain evidence that data quality is actively monitored and enforced.  

The Data Quality & Anomalies module ensures the platform is **accurate, reliable, and defensible**.
