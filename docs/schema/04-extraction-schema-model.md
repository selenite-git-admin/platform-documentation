# Extraction Schema Model

## Purpose
Define the landing artifact produced by a connector.
Describe format, partitioning, CDC markers, and layout.

## Modes
Use explicit Extraction contracts for APIs, files, and streams.
Use derived Extraction contracts for simple database table pulls.

## Header
- contract_id
- contract_type: extraction
- business_domain
- data_source_vendor
- data_source_instance_id
- source_module
- source_object
- target_landing_name
- version
- owner_team
- steward
- lineage_id

## Payload
- landing_format: file or stream or table
- columns: name, physical_type, nullable, description
- partitioning: keys and strategy
- compression and encoding
- path or topic
- cdc_markers and strategy
- extraction_filters when present
- sample_controls when present

## Procedure
1. Discover the source object.
2. Author header and payload.
3. Validate against Meta and Enforcement rules.
4. Register and promote.
5. Run the pipeline ingestion stage.

## Example
```yaml
header:
  contract_id: extraction.sf.account.v1
  contract_type: extraction
  business_domain: sales
  data_source_vendor: Salesforce
  data_source_instance_id: sf-prod-01
  source_module: core
  source_object: Account
  target_landing_name: sf_account_landing
  version: "1.0.0"
  owner_team: data-foundation
  lineage_id: sf-prod-01:Account
payload:
  landing_format: file
  columns:
    - name: Id
      physical_type: STRING
      nullable: false
  partitioning:
    - key: extract_date
  compression: gzip
  cdc_markers: ["SystemModstamp"]
```
