# GDP Schema Model

## Purpose
Define Silver tables with conformed dimensions.
Create a source agnostic semantic layer.
Enable KPI materialization and activation.

## Header
- contract_id
- contract_type: gdp
- business_domain
- target_schema_name
- target_table_name
- version
- owner_team
- steward
- lineage_id
- dependencies: raw contracts

## Payload
- columns with clear business names and types
- primary_key and foreign_keys
- indexes for common access paths
- quality_rules_ref
- mapping section from raw

## Mapping Specification
For each target column:
- target
- from_contract
- source_columns
- transform expression or rule id
- tests

## SCD and Reference Data
Declare SCD handling.
Declare conforming joins to reference data.

## Example
```yaml
header:
  contract_id: gdp.finance.ap.invoice_line.v1
  contract_type: gdp
  business_domain: finance
  target_schema_name: gdp_finance
  target_table_name: ap_invoice_line
  version: "1.0.0"
  owner_team: finance-foundation
  lineage_id: domain:finance:ap:invoice_line
  dependencies: ["raw.sap.fi.bseg.v1"]
payload:
  columns:
    - name: company_id
      semantic_type: company
      physical_type: VARCHAR(16)
      nullable: false
      key_flag: true
  primary_key: ["company_id", "invoice_id", "line_id"]
mapping:
  - target: company_id
    from_contract: raw.sap.fi.bseg.v1
    source_column: bukrs
    transform: map_company_code(bukrs)
    tests: ["t_company_code_exists"]
```
