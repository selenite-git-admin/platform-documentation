# Data Store

The Data Store family governs all persisted and queryable data within the platform.  
It provides authoritative, PostgreSQL-first storage for structured business data, golden datasets, and analytical outputs.  
Each submodule defines how data is cataloged, versioned, retained, and accessed under metadata-driven control.

The family operates as the core persistence layer that connects acquisition, governance, and intelligence.  
It integrates with Platform Control for schema and evidence registration, with Runtime for controlled writes, and with Data Quality for validation and observability.

---

## Purpose

Data Store maintains the platform’s internal truth — the state of every dataset, its structure, lineage, and history.  
It enforces retention and classification policies, maintains Slowly Changing Dimensions (SCD) for business entities, and guarantees that all persisted data remains discoverable, auditable, and consistent with its contract.

---

## Principles

- **PostgreSQL-first:** A single relational backbone across modules; no reliance on external warehouses.  
- **Metadata-governed:** DRR, Catalog, and Policy tables control discoverability, retention, and freshness.  
- **Declarative operations:** All merges, updates, and compactions are defined by metadata, not code.  
- **Auditable:** Every structural or data change emits evidence to the Evidence Ledger.  
- **Safe by default:** Data is immutable except through controlled Runtime merges or approved retention policies.

---

## Logical Architecture

```
Ingestion → Runtime → DRR → Data Store (Catalog, SCD, GDP, KPI layers) → Evidence Ledger → Consumption
```

---

## Core Entities

| Layer | Description |
|--------|-------------|
| **Bronze** | Raw extracted and minimally processed data. |
| **Silver** | Clean, validated business facts aligned with GDP models. |
| **Gold** | Curated, analytics-ready KPI datasets. |
| **Dimensional** | SCD-modeled entities that maintain history over time. |

---

## Schema Conventions

| Convention | Example |
|-------------|----------|
| Schema naming | `bronze`, `gdp`, `kpi`, `dim` |
| Table naming | `fact_<domain>`, `dim_<entity>` |
| Views | `vw_<table>_current`, `vw_<table>_asof` |
| Retention | Bronze (90d), Silver (3y), Gold/Dim (permanent) |

---

## Integration with Governance

| System | Role |
|---------|------|
| **DRR** | Declares dataset freshness and source lineage. |
| **Catalog** | Defines and registers schema metadata. |
| **Evidence Ledger** | Audits structural and data changes. |
| **Runtime** | Executes merges, transformations, and policy checks. |
| **Governance** | Reviews and enforces retention and classification rules. |

---

## Modules

[Storage](storage/index.md)  
Implements persistence, partitioning, and catalog management for multi-layer datasets.

[Data Read Registry (DRR)](../data-read-registry/index.md)  
Tracks dataset freshness, lineage, and read status for consumers.

[Data Store Catalog](../catalog/index.md)  
Provides canonical metadata for schemas, retention, and dataset attributes.

[Slowly Changing Dimensions (SCD)](../scd/index.md)  
Implements history tracking and merge templates for dimensional entities.

[Store Policies](store_policies.md)  
Defines declarative governance for retention, classification, and immutability.

[Observability](observability.md)  
Publishes metrics for latency, load, and data availability.

---

## Summary

The Data Store family forms the backbone of DataJetty’s persistence strategy — a metadata-driven layer that guarantees every dataset is findable, current, and historically correct.  
Catalog defines the **what**, DRR the **when**, SCD the **how**, and the Evidence Ledger the **proof**.  
Together they maintain the single version of truth across the entire platform.
