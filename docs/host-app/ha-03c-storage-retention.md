# Host App — Storage & Retention

## Purpose
Defines how governance metadata and artifacts are stored and retained over time.  
Storage policies ensure data durability, residency compliance, and defensibility.

## Storage Design
- **Relational DB** — tenants, approvals, RBAC, reference data.  
- **Object Store** — artifacts (diffs, approval bundles, exports).  
- **No canonical contracts** — contracts remain in Schema/PHS; Host App holds references only.  

## Retention Policies
- **Approvals & Audit Events** — retained indefinitely or per compliance policy.  
- **Tenant Metadata** — retained until retirement + compliance hold period.  
- **Artifacts (exports, diffs)** — retained based on regulatory requirements (e.g., 7 years).  

## Residency & Compliance
- Data partitioned by residency region.  
- Enforcement at both DB and object store level.  
- Retention aligned with GDPR, SOC2, or industry frameworks.  

## Why This Matters
Retention policies balance compliance and cost.  
Governance data must be available for audits years after publication, but must also be purged responsibly to meet privacy laws.
