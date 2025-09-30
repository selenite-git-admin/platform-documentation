# Meta Schema Model

## Purpose
Define inheritance rules and naming rules.
Provide defaults and allowed values.
Enable contract validation and generation.

## Inheritance
All contracts inherit required fields from Meta.
All contracts inherit allowed values and naming rules.

## Required Header Fields
- contract_id
- contract_type
- business_domain
- version
- owner_team
- lineage_id

## Required Payload Fields
- columns
- primary_key

## Naming Rules
- Tables use snake case.
- Columns use snake case.
- Contract ids use dots to separate parts.

## Allowed Values
- contract_type in [extraction, raw, gdp, kpi, outbound]
- classification in [public, restricted]

## Lineage Model
Record upstream and downstream contract ids.
Record run identifiers and time stamps.
Record storage locations for landing, Bronze, Silver, and Gold.

## Example Meta
```yaml
meta_schema_version: 1.0
required_header_fields:
  - contract_id
  - contract_type
  - business_domain
  - version
  - owner_team
  - lineage_id
required_payload_fields:
  - columns
  - primary_key
naming:
  table_case: snake
  column_case: snake
allowed_contract_types: [extraction, raw, gdp, kpi, outbound]
```
