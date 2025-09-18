# Data Plane Layer — Bronze (Raw)

## Purpose
The Bronze layer is the **landing zone** for all incoming data.  
It captures raw, immutable copies of source data as close to the original form as possible, ensuring nothing is lost before transformation or validation.  
Bronze is the foundation of trust: every downstream dataset can trace lineage back to here.

---

## Responsibilities
- **Ingestion** — capture data from ERP, CRM, HRMS, and tenant-specific sources.  
- **Immutability** — preserve original data without edits or deletions.  
- **Schema-on-read** — allow inspection and exploration of raw structures without forcing early transformation.  
- **Auditability** — maintain full lineage and source metadata for every record.  
- **Staging** — provide a stable base for Silver processing, without being queried directly for business use.

---

## Non-Goals
- No business logic or KPI computation.  
- No data standardization or key alignment (that happens in Silver).  
- No tenant-facing reports or dashboards.  

---

## Flows
1. **Source connect** — ingestion pipelines pull or receive data from external systems.  
2. **Store raw** — data lands in Bronze storage with metadata tags (source, time, version).  
3. **Lock** — data is marked immutable; any corrections are handled through new loads, not edits.  
4. **Trace** — lineage records link Bronze to Silver transformations for audit.  

---

## Why This Matters
Without a Bronze layer, organizations risk losing raw evidence of data.  
By keeping an untouchable copy:
- **Engineers** can reprocess or fix downstream errors without asking sources to resend.  
- **Auditors** can verify that GDP and KPIs are derived faithfully.  
- **Business teams** gain confidence that insights are based on a provable chain of data custody.  

The Bronze layer ensures the platform is **trustworthy, reproducible, and defensible**.
