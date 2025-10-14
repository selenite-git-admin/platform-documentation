# Data Store Family

**Tier:** Core  
**Owner:** Platform Foundation  
**Status:** Active  

## Purpose
The Data Store family governs all persisted data within the platform. It provides authoritative PostgreSQL stores that host structured business data, golden datasets, and analytical outputs. Each submodule defines how data is cataloged, versioned, retained, and accessed.

## Principles
- **PostgreSQL-first:** One relational backbone for all modules — no external warehouses.  
- **Governed by metadata:** DRR and Catalog ensure discoverability and freshness.  
- **Zero engineering:** Declarative merges and policies; no manual ETL.  
- **Auditable:** All changes logged to the Evidence Ledger.  
- **Safe by default:** Read-only by design except via controlled Runtime writes.

## Modules
| Module | Description |
|---------|--------------|
| [Data Read Registry (DRR)](../data-read-registry/index.md) | Tracks dataset freshness and lineage. |
| [Data Store Catalog](../catalog/index.md) | Canonical metadata registry for datasets. |
| [Slowly Changing Dimensions (SCD)](../scd/index.md) | PostgreSQL-native history tracking with merge templates. |
| [Store Policies](store_policies.md) | Declarative governance for retention, classification, and immutability. |
| [Observability](observability.md) | Metrics and dashboards for latency and availability. |

## Logical Architecture
```
Ingestion → Runtime → DRR → Data Store (Catalog, SCD, GDP, KPI layers) → Evidence Ledger → Consumption
```

### Core Entities
| Layer | Description |
|--------|-------------|
| Bronze | Raw extracted data |
| Silver | GDP-aligned clean business facts |
| Gold | KPI tables and analytics-ready data |
| Dimensional | SCD-modeled entities |

### Schema Conventions
| Convention | Example |
|-------------|----------|
| Schema naming | `bronze`, `gdp`, `kpi`, `dim` |
| Table naming | `fact_<domain>`, `dim_<entity>` |
| Views | `vw_<table>_current`, `vw_<table>_asof` |
| Retention | Bronze (90d), Silver (3y), Gold/Dim (permanent) |

## Integration with Governance
| System | Role |
|---------|------|
| **DRR** | Declares dataset freshness |
| **Catalog** | Declares schema metadata |
| **Evidence Ledger** | Audits changes |
| **Runtime** | Executes merges |
| **Governance** | Reviews retention and classification policies |

## Summary
The Data Store family is the platform’s core — a metadata-driven layer guaranteeing every dataset is findable, current, and historically correct.  
Catalog defines the “what”, DRR the “when”, SCD the “how”, and Evidence Ledger the “proof.” Together they maintain a single version of truth.