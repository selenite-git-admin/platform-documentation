# Anomaly and DQ Integration

## Purpose
Use anomaly detection and data quality checks to protect metrics.
Gate releases when severity is high.

## Modes
- Shadow: detect only
- Gate: block on severity
- Feedback: capture human labels

## Inputs
GDP and Metrics tables.

## Outputs
Findings, tickets, and evidence records.

## Cross references
See Pipeline anomaly integration: ../pipeline/16-anomaly-integration.md
See DQ engine: ../pipeline/07-data-quality-and-validation.md

## Legacy content
The following sections are imported from legacy pre and post validation.

### Pre validation
# Kpi Pre Validation
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

# KPI Pre-Validation Framework

## Purpose
The KPI Pre-Validation Framework ensures that every KPI computation runs only on ready, complete, and trustworthy input data.  
It acts as the gatekeeper before KPI execution, verifying that required GDPs or upstream KPIs are available, fresh, and high quality.  

This prevents CFOs and business users from seeing half-baked or misleading KPIs due to stale or incomplete data.

## Core Concepts

- Data Availability  
  - Are all declared GDP tables or KPI sources present for the requested time range?  
  - Do they cover the expected entities (company, units, geographies)?  

- Data Readiness  
  - Are upstream pipelines and dependencies complete?  
  - Is data within freshness SLA (e.g., <24h for DSO, <1h for Cash Balance)?  

- Data Quality Checks  
  - Null / missing value ratios.  
  - Out-of-range checks (e.g., negative receivables).  
  - Reconciliation checks (e.g., trial balance equality).  
  - Record count consistency vs historical baseline.  

## Pre-Validation Schema (YAML/JSON)

```yaml
kpi_id: CFO-EF-02
contract_version: 1.0.0
pre_validation:
  availability:
    sources: [GDP_Receivables, GDP_Sales]
    time_range: last_6m
  readiness:
    freshness_sla: "24h"
    dependency_signals: [erp_eod_sync]
  quality_rules:
    - rule: "no_nulls"
      field: receivable_amount
    - rule: "value_range"
      field: receivable_amount
      min: 0
    - rule: "reconciliation"
      type: trial_balance_check
```

## Governance & Lineage

- Fail-Fast Policy  
  If pre-validation fails, KPI execution is skipped. Error is logged, alert fired, lineage updated.  

- Transparency  
  Each KPI run stores pre-validation results (pass/fail + rules applied).  
  Users can inspect failures in observability dashboards.  

- Audit Trail  
  Pre-validation outcomes are recorded in KPI history tables for auditors.  

- Configurable Severity  
  Some checks may be warnings (allow execution), others are hard stops.  

## Integration with Other Frameworks

- KPI Sourcing Framework  
  Defines the GDPs or KPI IDs to validate.  

- KPI Scheduler Framework  
  Scheduler checks pre-validation results before executing KPI Calls.  

- KPI Call Framework  
  Only executed if pre-validation passes.  

- KPI Post-Validation Framework  
  Complements pre-validation by checking plausibility of outputs.  

## Example

**Days Sales Outstanding (CFO-EF-02)**  
- Sources: GDP_Receivables, GDP_Sales.  
- Pre-Validation Rules:  
  - Availability → both tables must have data for last 6 months.  
  - Readiness → SLA <24h, dependency = ERP EOD sync complete.  
  - Quality → no negative receivables, trial balance reconciles.  
- If GDP_Sales is missing for March, the KPI run is skipped, with an error surfaced to the CFO dashboard.  

## Why It Matters
- Trust – CFOs only see KPIs computed on validated inputs.  
- Consistency – standardized checks across all KPIs.  
- Resilience – prevents broken dashboards/AI activations on missing data.  
- Auditability – logs every validation for future reference.  
- Governance – enforces enterprise-wide data discipline before numbers go live.  

## Diagrams

None

## Tables

None



## Glossary

None

### Post validation
# Kpi Post Validation
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

# KPI Post-Validation Framework

## Purpose
The KPI Post-Validation Framework ensures that KPI outputs are plausible, consistent, and trustworthy before they are consumed by dashboards, reports, or AI agents.  
It acts as the final safeguard after KPI execution, catching anomalies, impossible values, or rule violations that could mislead business decisions.

## Core Concepts

- Rule-Based Checks
  - Validate KPI outputs against predefined business rules.
  - Examples:
    - Liquidity ratios must be >= 0.
    - Gross Margin % between -100% and +100%.
    - DSO cannot be negative.

- Statistical & Historical Checks
  - Compare outputs to historical baselines or thresholds.
  - Examples:
    - Variance outside 3σ (standard deviation).
    - Month-over-Month change exceeds defined tolerance.
    - Outlier detection using rolling averages.

- Business Verdict Alignment
  - Ensure verdicts (Adequate / Low / Critical) are consistent with raw numbers.
  - Flag mismatches (e.g., ratio is “Critical” but verdict marked “Adequate”).

- Cross-KPI Consistency
  - Reconcile related KPIs to avoid contradictions.
  - Example: Net Income = Revenue – Expenses must hold true across packs.

## Post-Validation Schema (YAML/JSON)

```yaml
kpi_id: CFO-LQ-07
contract_version: 1.0.0
post_validation:
  rules:
    - type: value_range
      field: liquidity_ratio
      min: 0
      max: 10
    - type: variance_check
      field: liquidity_ratio
      max_change_pct: 50
    - type: verdict_alignment
      rule_set: liquidity_generic_v1
    - type: cross_kpi
      expression: "CFO-PR-01 = CFO-RV-01 - CFO-EX-01"
```

## Governance & Lineage

- Audit Trail
  - Each KPI run stores post-validation results.
  - Failures flagged with severity and logged in KPI history.

- Configurable Actions
  - Warning: Display KPI but flag in UI.
  - Hard Stop: Suppress KPI delivery until reviewed.

- Transparency
  - Users can inspect validation outcomes alongside KPI results.
  - Alerts raised to both technical and business owners.

- Versioned Rules
  - Validation rulesets are version-controlled and linked to KPI contracts.

## Integration with Other Frameworks

- KPI Call Framework
  Supplies the raw output to be validated.

- KPI Scheduler Framework
  Ensures post-validation completes before marking job success.

- KPI Lifecycle Framework
  Validation results feed into audit & compliance records.

- KPI Extensions Framework
  Post-validation may run per extension (e.g., per unit, per currency).

## Example

**Liquidity Ratio (CFO-LQ-07)**  
- Computed as Cash Balance ÷ Current Liabilities.  
- Post-Validation Rules:  
  - Must be ≥ 0.  
  - Cannot change >50% MoM.  
  - Verdict must align with liquidity rule set.  
- If ratio = -0.2, KPI is suppressed and alert raised to CFO Office.

## Why It Matters
- Trust – invalid or misleading KPIs are caught before delivery.  
- Resilience – protects dashboards and AI agents from “garbage out.”  
- Governance – audit trail of validation results.  
- Business Alignment – ensures KPI verdicts match financial reality.  
- Future-Proof – supports statistical, ML, and rule-based checks.  

## Diagrams

None

## Tables

None



## Glossary

None
