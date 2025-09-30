# Cross-Cutting — Residency & Compliance

## Purpose
The Residency & Compliance module enforces where and how data can be stored, processed, and retained.  
It ensures that tenant workloads respect regional residency laws, regulatory frameworks (e.g., GDPR, HIPAA, SOX), and contractual obligations.  
This capability spans both Control and Data planes, tying governance decisions to execution environments.

## Responsibilities
- **Residency enforcement** — restrict data to approved geographic regions and cloud accounts.  
- **Retention policies** — enforce deletion timelines, archival rules, and evidence of compliance.  
- **Classification mapping** — apply regulatory classifications (e.g., PII, financial, health data) to datasets.  
- **Access control hooks** — restrict user and service access based on residency and compliance tags.  
- **Audit reporting** — provide evidence of residency, retention, and classification enforcement to auditors.  

## Non-Goals
- Does not define business KPIs or metrics.  
- Does not handle tenant-specific RBAC (covered in Security & RBAC).  
- Does not execute transformations or ingestion pipelines (that is the Data Plane’s role).  

## Flows
1. **Classify** — datasets are tagged with residency, compliance, and classification metadata at ingestion.  
2. **Govern** — Host App enforces quotas and policies based on residency/compliance tags.  
3. **Execute** — Data Plane stores and processes data only in approved regions and services.  
4. **Retain/Delete** — Backup/DR and Retention services enforce deletion timelines.  
5. **Report** — audit logs and compliance dashboards show residency adherence and retention outcomes.  

## Interfaces
- **Host App** — defines residency flags and retention policies.  
- **Data Plane** — enforces residency and retention at storage/compute level.  
- **Backup/DR** — applies retention policies to snapshots and archives.  
- **Audit & Evidence** — logs proof of enforcement for compliance reviews.  

## Why This Matters
Without residency and compliance controls, organizations risk legal penalties, reputational damage, and failed audits.  
By embedding residency and retention into the platform:
- **Executives** gain assurance that regulatory obligations are met.  
- **Tenants** can adopt the platform without violating local laws.  
- **Auditors** receive defensible, immutable evidence of compliance.  

The Residency & Compliance module ensures the platform is **lawful, trusted, and audit-ready**.
