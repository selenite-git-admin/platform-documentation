# Data Quality and Validation

## Purpose
Prevent bad data from moving forward.
Prove conformance to schema contracts.

## Rule catalog
Store rules with an identifier, a description, a severity, and a check expression.

## Severities
- Red blocks promotion
- Amber requires attention
- Green passes

## Gates
Run checks at extraction, raw, GDP, and KPI stages.
Attach evidence for each gate.

## Sampling and profiling
Profile columns and distributions.
Use samples for investigation only.

## Reports
Produce a validation report with counts and rule outcomes.
Store the report in the evidence store.


## Skip semantics

## Skip semantics
When the scheduler skips a stage, DQ gates for that stage do not run.
The system records a validation event with status SKIPPED.
The evidence includes the reason for the skip.


## Rule catalog schema

Rules have an identifier, a description, a severity, and a check.
Rules have a scope that selects stages.
Rules have owners and versions.

```yaml
id: qr_gdp_not_null_pk
name: "Primary key cannot be null"
description: "Check that primary key columns are not null"
severity: red
stage_scope: [extraction, raw, gdp, kpi, outbound]
owner_team: data_quality
version: 1
check:
  type: expression
  expression: "not_null(pk_columns)"
```

## Plugin API

You can implement rules as plugins.
The platform loads plugins at runtime.

```yaml
id: qr_custom_compliance_check
name: "Custom compliance check"
severity: amber
stage_scope: [gdp, kpi]
check:
  type: plugin
  plugin_ref: "com.example.rules.compliance.CheckV1"
  params:
    threshold: 0.95
```

## Execution contract

The engine receives a table reference and a run identifier.
The engine returns counts by rule and a verdict.
The engine stores a report as evidence.

```json
{
  "run_id": "uuid",
  "stage": "gdp",
  "table": "gdp_finance.invoice_line",
  "rules": [
    {"id": "qr_gdp_not_null_pk", "status": "pass", "count": 0},
    {"id": "qr_amount_scale", "status": "warning", "count": 12}
  ],
  "verdict": "amber"
}
```
