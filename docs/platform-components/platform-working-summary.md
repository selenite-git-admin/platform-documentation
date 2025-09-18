# Platform Working — Summary

## Control Plane
The Control Plane defines **intent and governance**.  
- **Schema Services** store canonical contracts, ensuring transformations and KPIs are derived from governed definitions.  
- **Host App** provides the governance UI, approvals, and audit evidence.  
- **PHS Control APIs** translate contracts into executable plans for orchestration.  

Together, these components answer **what should happen** and record **why it is allowed**.

---

## Data Plane
The Data Plane delivers the **execution of workloads and business outcomes**.  
- **Bronze** preserves immutable raw data.  
- **Silver** standardizes and cleans it into business-ready structures.  
- **Gold (GDP)** transforms data into governed, human-readable entities.  
- **KPI layer** derives consistent, auditable metrics.  
- **Tenant App** exposes results to end users while enforcing quotas, RBAC, and overlays.  

This is where governance intent becomes **actionable results** for tenants.

---

## Cross-Cutting
Cross-Cutting services span both planes, ensuring quality, compliance, and operational maturity:  
- **Data Quality & Anomalies** enforces validation and detects outliers.  
- **Alerts & Monitoring** provides observability and escalation.  
- **Residency & Compliance** ensures lawful data handling and retention.  
- **Security & RBAC** secures access across all services.  
- **Runtime Foundations (PHS Common)** provide orchestration, artifact versioning, telemetry, lineage, secrets, backup/DR, and cost enforcement.  

These services make the platform **trustworthy, resilient, and auditable**.

---

## Why This Matters
Platform Working bridges the gap between high-level contracts and low-level execution.  
It ensures that:
- **Executives** get trustworthy, consistent KPIs.  
- **Tenants** gain flexibility within governance boundaries.  
- **Engineers** work with predictable, reliable infrastructure.  
- **Auditors** can trace every result to an approved contract and reproducible run.  

By documenting Platform Working separately from component details, we preserve a clear line between the **“what/why”** (flows and responsibilities) and the **“how”** (deep component implementations).
