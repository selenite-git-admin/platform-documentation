# Metric Schema Model

## Purpose
Define Gold serving tables or views.
Provide stable and testable metrics.
Support analytics, APIs, and put back pipelines.

## Header
- contract_id
- contract_type: kpi
- business_domain
- target_schema_name
- target_table_name
- version
- owner_team
- steward
- lineage_id
- dependencies: GDP contracts
- classification
- rls_scope when needed

## Payload
- grain
- dimensions: name, data_type, description
- metrics: name, metric_type, data_type, description
- filters
- primary_key and unique_keys
- indexes
- retention_policy
- refresh_strategy
- materialization
- quality_rules_ref

## Mapping
For each KPI column:
- target
- from_gdp_contract
- source_columns
- transform
- tests

## Time and Currency
State calendars and time windows.
State currency conversion policy.

## Example
```yaml
header:
  contract_id: kpi.finance.ar.receivables_month_company.v1
  contract_type: kpi
  business_domain: finance
  target_schema_name: kpi_finance
  target_table_name: ar_receivables_month_company
  version: "1.0.0"
  owner_team: finance-analytics
  lineage_id: kpi:finance:ar:receivables_month_company
  dependencies: ["gdp.finance.ar.invoice_line.v1"]
payload:
  grain: company_id_month
  dimensions:
    - name: company_id
      data_type: VARCHAR(16)
      description: Conformed company id
    - name: month_id
      data_type: INT
      description: YYYYMM
  metrics:
    - name: closing_ar
      metric_type: derived
      data_type: DECIMAL(18,2)
      description: AR at end of month
  primary_key: ["company_id", "month_id"]
  materialization: table
```
