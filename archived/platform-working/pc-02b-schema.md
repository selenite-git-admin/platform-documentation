# Control Plane Component — Schema Services

## Purpose
Schema Services are the **canonical contract store** for the platform.  
They define how raw data, GDP entities, and KPIs are structured, validated, and governed.  
Every contract in Schema Services is immutable and versioned.

## Responsibilities
- **Contract definition** — Raw → Silver, Silver → GDP, GDP → KPI.  
- **Validation** — enforce compatibility rules, DQC checks, and anomaly detection packs.  
- **Versioning** — ensure every change is tracked, with full lineage.  
- **Publication** — provide validated contracts to PHS Control APIs for orchestration.

## Non-Goals
- Do not manage governance workflows (that is Host App).  
- Do not compile or deploy plans (that is PHS Control APIs).  
- Do not store tenant business data (that is Data Plane).  

## Why This Matters
Contracts are the backbone of trust in the platform.  
By centralizing them in Schema Services, we ensure consistency across tenants, prevent drift, and make metrics explainable and auditable.
