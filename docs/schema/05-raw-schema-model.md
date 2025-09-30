# Raw Schema Model

## Purpose
Define Bronze tables with near source fidelity.
Normalize types and keys.
Preserve change markers and operational fields.

## Header
- contract_id
- contract_type: raw
- business_domain
- data_source_vendor
- data_source_instance_id
- source_module
- source_table
- target_schema_name
- target_table_name
- version
- owner_team
- steward
- lineage_id
- dependencies: extraction contract when explicit

## Payload
- columns: name, semantic_type, physical_type, nullable, default, description, pii_flag, key_flag, surrogate_key_flag
- primary_key
- unique_keys
- foreign_keys
- indexes
- constraints
- change_capture: source_cdc_fields and strategy
- mapping_anchor: source_fqn and natural_keys

## Procedure
1. Introspect the source table.
2. Author header and payload.
3. Validate and register.
4. Generate DDL.
5. Load idempotent batches.
6. Record evidence and lineage.

## Example
```yaml
header:
  contract_id: raw.sap.fi.bkpf.v1
  contract_type: raw
  business_domain: finance
  data_source_vendor: SAP
  data_source_instance_id: sap-s4p-01
  source_module: FI
  source_table: BKPF
  target_schema_name: raw_sap_fi
  target_table_name: bkpf
  version: "1.0.0"
  owner_team: data-foundation
  lineage_id: sap-s4p-01:FI:BKPF
payload:
  columns:
    - name: bukrs
      semantic_type: company_code
      physical_type: CHAR(4)
      nullable: false
      key_flag: true
    - name: belnr
      semantic_type: document_number
      physical_type: CHAR(10)
      nullable: false
      key_flag: true
    - name: gjahr
      semantic_type: fiscal_year
      physical_type: NUMC(4)
      nullable: false
      key_flag: true
  primary_key: ["bukrs", "belnr", "gjahr"]
  change_capture:
    source_cdc_fields: ["cpudt", "cputm"]
    strategy: append_only
```
