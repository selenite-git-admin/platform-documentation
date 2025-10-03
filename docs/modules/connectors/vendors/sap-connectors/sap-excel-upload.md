# SAP EXCEL UPLOAD

## Purpose
Describe the development requirements for the SAP Manual Excel Upload connector used when data is exported from SAP into spreadsheets and uploaded manually or via folder drop.

## Scope
Processes Excel files that represent SAP exports. 
Supports discovery by folder pattern, incremental processing by file checkpoint, and schema inference from headers and data types.

## Supported Formats
- XLSX files with header rows
- CSV files when Excel is converted to CSV

## Authentication
If files arrive through S3 or shared storage use IAM role or service account. 
If uploads are manual the UI provides the upload path and the connector reads from the staging bucket.

## Network and Deployment
Supported runners
- AWS Lambda for small to medium files
- AWS Fargate for larger files or complex parsing

Supported network patterns
- VPC endpoints for object storage
- NAT allowlist only if required for public storage services

## Discovery
List files under the configured path and identify streams per pattern such as sap_excel.gl_accounts. 
Infer schema from header names and sample rows.

## Incremental Processing
Use file path plus checksum as the cursor. 
Ensure idempotency by using row index as part of the compound key when no business key exists.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::erp::sap::sap_excel::upload
name: SAP Excel Upload Connector
taxonomy:
  origin: enterprise
  source: erp
  provider: sap
  product: excel
  method: upload
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [vpc_endpoint, nat_allowlist]
streams:
  strategy: discovery_by_pattern
  defaults:
    key_strategy: synthetic_file_row
    cursor_strategy: file_checkpoint
```

## Throttling and Retries
Limit concurrent file parsing to control memory. 
Retry transient read errors and skip corrupt rows with error records.

## Error Handling
Log file level errors with context. 
Stop only on repeated failures for the same file to avoid loops.

## Schema Handling
Infer schemas and store them in the schema registry. 
Do not embed schemas in the manifest. 
Raise drift alerts when column sets change.

## Observability
Metrics should include files discovered, files processed, rows emitted, and parse errors. 
Logs record file names, sizes, and parsing steps.

## Testing
Unit tests for header inference, type coercion, and checkpoint logic. 
Integration tests with sample Excel exports. 
Certification in Lambda and Fargate.

## Limits and Considerations
- Excel date and number formats can be ambiguous
- Large sheets require streaming parsers
- Header names may vary across exports

## Relationships
Uses state registry for file checkpoints and schema registry for inferred schemas.

## Exclusions
No business mappings or onboarding steps.
