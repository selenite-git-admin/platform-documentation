# GDP Transform

## Purpose
Create conformed Silver tables from Raw.
Use the GDP mapping spec to define transformations.

## Mapping spec
Each target column maps from one or more raw columns.
Declare a transform expression or a named rule.
Declare tests for each mapping.

## Transform types
- Type casts and normalization
- Business key construction
- Reference data joins
- SCD handling
- Deduplication

## Incremental strategy
Use dates or keys to process only new data.
Handle late arriving records with correction runs.

## Evidence
Record mapping coverage.
Record rule hits and severity.

## Example mapping entry
```yaml
- target: company_id
  from_raw_contract: raw.sap.fi.bseg.v1
  source_column: bukrs
  transform: map_company_code(bukrs)
  tests: [t_company_code_exists]
```


## Behavior when GDP is not ready

## Behavior when GDP is not ready
If there is no Active GDP contract, the pipeline skips this stage.
The system records a SKIPPED status for GDP.
The system continues to run ingestion and Raw.
