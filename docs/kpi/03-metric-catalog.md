# Metric Catalog

## Purpose
Provide a curated catalog of metrics and dimensions.
Enable search, tags, tenancy views, and variants.

## Entries
Each entry links to a registry record and a metrics schema contract.
Each entry includes name, description, grain, units, owners, tags, and release channel.

## Search and tags
Allow search by name, tag, domain, grain, and owner.

## Tenancy
Show only entries that the tenant can see.
Apply row level scoping when required.

## Variants
Record parent metric and variant relationship.
Record why the variant exists and how it differs.

## Legacy content
The following sections are imported from legacy documents.

### Structure
# Kpi Structure
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Structure & Flow

## Purpose
This document defines the shape of a KPI in Cxofacts: its metadata, sourcing, validation rules, schedule, and defaults.  
It also provides a canonical ERD (via DBML) and placeholders for diagrams that illustrate the KPI run workflow.

## KPI Entity Model (ERD)

The ERD captures how a KPI is defined at rest (in metadata).  
Use the DBML file below to generate an SVG/PNG via dbdiagram, dbml-cli, or your diagram tool of choice.

![KPI Structure ERD](kpi-structure-erd.svg)

> Core entities:
> - `kpi_contract` (primary key: kpi_id + contract_version)
> - `kpi_variant_lineage` (parent mapping for industry/client variants)
> - `kpi_source` (GDP/KPI inputs and attributes)
> - `kpi_extension` (time/entity/benchmark/scenario/analytical configs)
> - `kpi_pre_validation_rule` and `kpi_post_validation_rule`
> - `kpi_schedule` (frequency, triggers, SLA)
> - `kpi_call_defaults` (time grain, filters, SCD view)
> - `kpi_expression` (formula / query template)

## KPI Run Workflow (Diagram Placeholder)

This section should contain a workflow diagram showing how a single KPI is executed:

```
Definition (kpi_contract) 
  → Sourcing (kpi_source) 
  → Pre-Validation (kpi_pre_validation_rule) 
  → Call (generation/execution using kpi_expression + kpi_call_defaults) 
  → Scheduler (kpi_schedule) 
  → Post-Validation (kpi_post_validation_rule) 
  → Logging & Monitoring 
  → Error Handling & Alerts/Reports 
  → Consumption (dashboards/agents)
```

**SVG Placeholder:**  
![KPI Run Workflow]#(../assets/diagrams/kpi-run-workflow.svg)

## Example: Liquidity Ratio (Illustrative)

- kpi_contract: `CFO-LQ-07`, version `1.0.0`, owners: CFO Office / Platform Eng.  
- kpi_source: `CFO-LQ-04` (Cash Balance), `CFO-LQ-05` (Current Liabilities).  
- kpi_extension: Time = MoM/YoY; Benchmark = Budget vs Actual.  
- kpi_pre_validation_rule: availability for last 6 months; freshness < 24h; non-negative liabilities.  
- kpi_expression: SQL template computing Cash ÷ Liabilities with guards on denominator > 0.  
- kpi_post_validation_rule: range ≥ 0; MoM change < 50%; verdict alignment.  
- kpi_schedule: daily at 02:00, SLA 1h, timezone = Asia/Kolkata.  
- kpi_call_defaults: `time_grain=day`, `scd_view=as_reported`.  

## Notes

- The ERD focuses on definition-time structures. Run-time surfaces (logging/monitoring) are defined in their respective framework docs.  
- All entities are multi-version aware (every link includes `kpi_id + contract_version`).  
- Enforce row-level security and tenant scoping in your physical schema.

## Diagrams

None

## Tables

None



## Glossary

None

### Layers
# Kpi Layers
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Layers

## Purpose
The KPI Layers Framework defines how KPIs are structured into logical layers within Cxofacts.  
It ensures clear separation between GDP-based KPIs and derived/composite KPIs, providing consistency for design, scheduling, and validation.

## Core Layers

- Primary KPIs (GDP-Sourced)
  - Operate directly on Golden Data Points (facts and dimensions).
  - Represent reconciled, base-level business measures.
  - Examples:
    - Cash Balance (GDP_CashBalance)
    - Receivables (GDP_Receivables)
    - Headcount (GDP_Employees)

- Secondary KPIs (KPI-Sourced / Derived)
  - Derived from one or more other KPI outputs.
  - Typically ratios, percentages, or composites.
  - Examples:
    - Days Sales Outstanding (Receivables ÷ Sales × Days)
    - Gross Margin % (Revenue – COGS) ÷ Revenue
    - Liquidity Ratio (Cash Balance ÷ Current Liabilities)

- Composite / Index KPIs
  - Higher-level aggregations or indices, often blending multiple KPIs into a score.
  - Examples:
    - Financial Health Index (weighted blend of liquidity, leverage, profitability ratios)
    - Sales Effectiveness Score (pipeline conversion, win rates, revenue per rep)

## Layered Dependency Graph (DAG)

- Leaves = Primary KPIs (GDP-sourced).
- Intermediate nodes = Secondary KPIs (KPI-on-KPI).
- Higher nodes = Composite KPIs (indices, scores).
- Scheduler executes DAG topologically:
  - Primary first → Secondary → Composite.

## Governance & Execution Implications

- Sourcing Framework
  - Primary → GDP mappings only.
  - Secondary → KPI contract references required.

- Pre-Validation
  - Primary → GDP readiness checks.
  - Secondary → Upstream KPI freshness & SLA checks.

- Scheduler
  - Executes DAG respecting KPI-on-KPI dependencies.

- Post-Validation
  - Rules adapted by layer:
    - Primary → data plausibility (no negative receivables).
    - Secondary → ratio rules (denominator >0, % range checks).
    - Composite → distribution/weighting sanity checks.

## Example: Liquidity KPI Set

1. Cash Balance (Primary)  
   - Source: GDP_CashBalance  
   - Frequency: Daily  

2. Current Liabilities (Primary)  
   - Source: GDP_Liabilities  
   - Frequency: Daily  

3. Liquidity Ratio (Secondary)  
   - Source: CFO-LQ-04 (Cash Balance), CFO-LQ-05 (Current Liabilities)  
   - Formula: Cash ÷ Liabilities  
   - Frequency: Daily (post dependencies)  

4. Liquidity Health Index (Composite)  
   - Source: CFO-LQ-07 (Liquidity Ratio), CFO-LQ-08 (Quick Ratio), CFO-LQ-09 (Cash Flow Coverage)  
   - Formula: Weighted index  
   - Frequency: Weekly  

## Why It Matters

- Clarity – Developers and pack designers know which layer a KPI belongs to.  
- Trust – CFOs see not just the ratio, but also the underlying validated KPIs.  
- Governance – Lifecycle and validation rules adapt to layer context.  
- Scalability – DAG execution allows hundreds of KPIs without chaos.  
- Future-Proof – Lays the groundwork for KPI indices, AI scoring, and industry benchmarks.  

## Diagrams

None

## Tables

None



## Glossary

None
