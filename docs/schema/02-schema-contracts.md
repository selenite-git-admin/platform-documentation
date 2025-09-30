# Schema Contracts

## Purpose
Define standard contracts for all schema types.
Provide header and payload sections that tools can parse.
Ensure uniform identity, governance, and structure.

## Contract Types
- extraction
- raw
- gdp
- kpi
- outbound

## Header Fields
- contract_id
- contract_type
- business_domain
- data_source_vendor or destination_vendor when relevant
- data_source_instance_id or destination_instance_id when relevant
- source_module and source_object or source_table for extraction and raw
- target_schema_name and target_table_name when the target is a table
- version in SemVer
- owner_team and steward
- lineage_id
- dependencies as a list of contract_id values
- classification
- rls_scope when row level security applies
- notes

## Payload Fields
- columns with name, semantic_type, physical_type, nullable, default, description, pii_flag, key_flag, surrogate_key_flag
- primary_key
- unique_keys
- foreign_keys with referenced table and columns
- indexes
- constraints
- quality_rules_ref as rule ids
- change_capture for extraction and raw
- mapping for GDP and KPI
- retention_policy when needed

## YAML Template
```yaml
header:
  contract_id: ""
  contract_type: extraction|raw|gdp|kpi|outbound
  business_domain: ""
  data_source_vendor: ""
  data_source_instance_id: ""
  source_module: ""
  source_table: ""
  target_schema_name: ""
  target_table_name: ""
  version: "1.0.0"
  owner_team: ""
  steward: ""
  lineage_id: ""
  dependencies: []
  classification: restricted|public
  rls_scope: ""
  notes: ""

payload:
  columns: []
  primary_key: []
  unique_keys: []
  foreign_keys: []
  indexes: []
  constraints: []
  quality_rules_ref: []
```

## Minimal Examples

### Extraction (table landing)
```yaml
header:
  contract_id: extraction.sap.fi.bseg.v1
  contract_type: extraction
  business_domain: finance
  data_source_vendor: SAP
  data_source_instance_id: sap-s4p-01
  source_module: FI
  source_object: BSEG
  target_landing_name: sap_fi_bseg_landing
  version: "1.0.0"
  owner_team: data-foundation
  steward: finance-data
  lineage_id: sap-s4p-01:FI:BSEG
payload:
  landing_format: table
  columns:
    - name: bukrs
      physical_type: CHAR(4)
      nullable: false
      description: Company code
  partitioning: []
  cdc_markers: ["cpudt", "cputm"]
```

### Raw (Bronze table)
```yaml
header:
  contract_id: raw.sap.fi.bseg.v1
  contract_type: raw
  business_domain: finance
  data_source_vendor: SAP
  data_source_instance_id: sap-s4p-01
  source_module: FI
  source_table: BSEG
  target_schema_name: raw_sap_fi
  target_table_name: bseg
  version: "1.0.0"
  owner_team: data-foundation
  steward: finance-data
  lineage_id: sap-s4p-01:FI:BSEG
  dependencies: ["extraction.sap.fi.bseg.v1"]
  classification: restricted
payload:
  columns:
    - name: bukrs
      semantic_type: company_code
      physical_type: CHAR(4)
      nullable: false
      key_flag: true
      surrogate_key_flag: false
      pii_flag: false
      description: Company code
  primary_key: ["bukrs", "belnr", "gjahr", "buzei"]
  change_capture:
    source_cdc_fields: ["cpudt", "cputm"]
    strategy: append_only
  mapping_anchor:
    source_fqn: "SAP.S4P.FI.BSEG"
    natural_keys: ["bukrs", "belnr", "gjahr", "buzei"]
```

### GDP (Silver table)
```yaml
header:
  contract_id: gdp.finance.ar.invoice_line.v1
  contract_type: gdp
  business_domain: finance
  target_schema_name: gdp_finance
  target_table_name: invoice_line
  version: "1.0.0"
  owner_team: finance-foundation
  steward: cfo-office
  lineage_id: domain:finance:invoice_line
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

### KPI (Gold table)
```yaml
header:
  contract_id: kpi.finance.ar.receivables_month_company.v1
  contract_type: kpi
  business_domain: finance
  target_schema_name: kpi_finance
  target_table_name: ar_receivables_month_company
  version: "1.0.0"
  owner_team: finance-analytics
  steward: cfo-office
  lineage_id: kpi:finance:ar:receivables_month_company
  dependencies:
    - gdp.finance.ar.invoice_line.v1
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
```

### Outbound (put back)
```yaml
header:
  contract_id: outbound.sap.fi.z_ar_snapshot.v1
  contract_type: outbound
  business_domain: finance
  destination_vendor: SAP
  destination_instance_id: sap-s4p-01
  destination_module: FI
  destination_object: Z_AR_SNAPSHOT
  delivery_mode: db_table
  version: "1.0.0"
  owner_team: finance-ops
  steward: cfo-office
  lineage_id: outbound:sap:fi:z_ar_snapshot
  dependencies: ["kpi.finance.ar.receivables_month_company.v1"]
payload:
  columns:
    - name: company_id
      data_type: VARCHAR(16)
      nullable: false
  idempotency_key: ["company_id", "month_id"]
  write_semantics: merge
  reconciliation_rules:
    - type: count_match
    - type: sum_match
```
