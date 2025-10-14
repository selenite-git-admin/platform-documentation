# Store Policies

**Family:** Data Store  
**Tier:** Core  
**Owner:** Platform Governance  
**Status:** Active  

## Purpose
Store Policies define the governance boundaries applied to PostgreSQL schemas and tables. They ensure consistent retention, classification, and immutability across Raw, GDP, KPI, Dimensional, and Published layers.

## Scope
Applies to all Data Store modules except transient staging schemas.

## Policy Types
| Category | Definition | Enforced By |
|-----------|-------------|-------------|
| **Retention** | Defines persistence duration | Runtime and DRR |
| **Classification** | Assigns sensitivity levels | Governance YAML |
| **Access** | Specifies operation scope | Access Control |
| **Immutability** | Locks certified data | Governance |
| **Schema Evolution** | Controls DDL drift | Schema Registry |

## Retention Policy
| Layer | Retention | Rationale |
|--------|------------|------------|
| Raw Store | 30–90 days | Temporary ingestion staging |
| GDP Store | 1–3 years | Clean, reconciled facts |
| KPI Store | Permanent | Executive and compliance-critical |
| Published Store | 2 years (default) | Shared or API-exposed data |
| SCD / Dimensional | Permanent | History preservation |

## Classification Policy
| Level | Description | Example |
|--------|-------------|----------|
| Public | Shareable | Reference tables |
| Internal | Tenant/Dept restricted | GDP/KPI facts |
| Restricted | Sensitive business data | HR, finance |
| Audit | Immutable logs | Evidence Ledger |

## Access Policy
| Layer | Write Authority | Read Scope |
|--------|-----------------|-------------|
| Raw | Runtime only | Validation & ingestion |
| GDP | Runtime only | Analytics & DRR |
| KPI | Governance | Dashboards |
| Published | Runtime | API consumers |
| SCD | Runtime | PIT queries |

## Immutability and Certification
- Certified GDP/KPI datasets are frozen.  
- Catalog stores checksum and timestamp.  
- Recertification requires Governance approval and audit entry.

## Schema Evolution
- All DDL via Schema Registry.  
- Non-breaking changes only after DRR and Catalog sync.

## YAML Definition Example
```yaml
layer: gdp
retention_days: 1095
classification: internal
write_authority: runtime
certified: true
last_reviewed: 2025-10-01
```

## Enforcement
- Retention cleanup by Lambda.  
- Access verified by Authorization layer.  
- DRR annotated with classification metadata.  
- Evidence Ledger records all policy events.

## Ownership
| Function | Responsibility |
|-----------|----------------|
| Governance | Define and review policies |
| Runtime | Execute enforcement |
| Platform | Implement hooks |
| SRE | Monitor compliance |

## Summary
Store Policies unify data lifecycle and access governance. They make the Data Store self-governing, compliant, and auditable — without introducing new services or warehouses.