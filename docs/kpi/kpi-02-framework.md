# KPI Services — Framework

## Purpose
The KPI Framework defines how Key Performance Indicators (KPIs) are represented, computed, and governed within the platform.  
It specifies the contract boundaries, the runtime model, and the integration points with GDP data and platform services.

## Inputs and Outputs
- **Inputs:** Canonical entities from GDP contracts (e.g., Calendar, Currency, Org, Headcount).  
- **Outputs:** KPI contracts that include definitions, formulas, thresholds, and computed values.  
- KPI Services never consume Raw contracts directly.

---

## Data Flow Summary

The platform enforces a three-contract model. Each layer has a clear purpose and boundary:

| Layer | Purpose | Example Entities | Used By |
|-------|---------|------------------|---------|
| **Raw Contracts** | Preserve exact source schema for ingestion. Immutable, system-specific. | SAP FI tables, CRM objects, operational logs | Schema Services (ingress) |
| **GDP Contracts** | Canonicalize raw attributes into standardized, human-readable business entities. Serves as the foundation for KPI calculations. | Calendar, Currency, Org Hierarchy, Headcount, Revenue | KPI Services (inputs) |
| **KPI Contracts** | Define and compute metrics, thresholds, and SLOs based on GDP entities. | Gross Margin %, Revenue Growth, Attrition Rate | APIs, reporting, downstream consumers |

**Flow:**  
`Raw → GDP → KPI`  

- Canonicalization happens in Schema Services (Raw → GDP).  
- KPI computation happens in KPI Services (GDP → KPI).  
- Enforcement points are described in [Schema Services — Enforcement & Validation](../schema/enforcement.md).  

---

## Core Components
1. **KPI Definition**  
   - Metadata describing KPI name, description, owner, and purpose.  
   - References GDP attributes as inputs.  
   - Version-controlled to ensure auditability.

2. **KPI Formula Model**  
   - Defines calculation logic, including arithmetic, aggregations, and dimensional filters.  
   - Always expressed in relation to GDP entities.  
   - Supports conformed dimensions for cross-function comparability.

3. **Lifecycle Management**  
   - Creation, update, and deprecation of KPIs follow controlled workflows.  
   - Versioning ensures historical values remain traceable even if definitions change.  

4. **Execution and Computation**  
   - Orchestration services compute KPI values on defined schedules or triggers.  
   - Validation gates check results against thresholds before publishing.  
   - Failures are logged with error codes and escalation rules.

5. **Delivery**  
   - Results published to downstream services (APIs, reports, data marts).  
   - Service-level objectives (SLOs) define delivery timeliness and availability.

---

KPI Framework ensures all metrics are **consistent, auditable, and based on GDP entities**, enabling reliable enterprise-wide reporting and analysis.
