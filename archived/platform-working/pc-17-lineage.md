# Platform Runtime Foundations — Lineage & Metadata

## Purpose
The Lineage & Metadata service provides **end-to-end traceability** of how data flows through the platform.  
It links raw ingested data, transformations, and KPI outputs back to their originating contracts and execution runs.  
This ensures every metric, report, or export is defensible, reproducible, and audit-ready.

## Responsibilities
- **Data lineage capture** — record transformations from Bronze → Silver → GDP → KPI → Tenant outputs.  
- **Run metadata** — log execution details (job IDs, timestamps, input/output manifests).  
- **Data product registry** — maintain catalog of governed datasets, their definitions, and owners.  
- **Contract linkage** — map outputs back to approved governance contracts in Host App.  
- **Evidence hooks** — expose lineage snapshots as proof for auditors and compliance checks.  

## Non-Goals
- Does not execute or schedule workloads (handled by Orchestration).  
- Does not apply data quality rules (Data Quality module handles this).  
- Does not deliver dashboards or reports (Tenant App function).  

## Flows
1. **Capture** — orchestration and data plane jobs emit lineage events at every stage.  
2. **Enrich** — events are enriched with metadata: contract ID, tenant, run ID, job context.  
3. **Store** — lineage graph persisted with pointers to manifests and logs.  
4. **Query** — auditors, engineers, and governance tools query lineage to answer “where did this metric come from?”  
5. **Expose** — Host App displays lineage evidence; Tenant App may provide scoped views for tenant admins.  

