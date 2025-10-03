# SAP DB DUMP

## Purpose
Describe the development requirements for the SAP Database Dump connector that ingests periodic exports from SAP managed databases.

## Scope
Ingests flat files or dumps produced by SAP systems and delivered to object storage or SFTP. 
Supports discovery by file patterns, incremental processing by file timestamp or checksum, and idempotent landing.

## Supported Formats
- CSV, Parquet, or fixed width as produced by export jobs
- Compressed archives such as gzip or zip

## Authentication
When reading from S3, Azure Blob, or GCS use IAM role or service account based access. 
For SFTP use key based authentication. 
Secrets come from the platform secrets store.

## Network and Deployment
Supported runners
- AWS Lambda for small to medium files
- AWS Fargate for large files or heavy parsing libraries
- AWS Glue for very large backfills or repartitioning

Supported network patterns
- VPC endpoints for object storage services
- VPN for SFTP targets
- NAT allowlist for public SFTP if allowed

## Discovery
List files under configured prefixes and match by pattern. 
Treat each pattern as a stream and emit stable stream ids such as file.s3.sap_gl_accounts_csv.

## Incremental Processing
Use a file checkpoint that includes path and checksum. 
Process only new or changed files. 
Maintain idempotency by using compound keys of file path and row number when no natural key exists.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::erp::sap::sap_generic::db_dump
name: SAP Database Dump Connector
taxonomy:
  origin: enterprise
  source: erp
  provider: sap
  product: generic
  method: db_dump
runtime:
  supported_runners: [lambda, fargate, glue]
  network_patterns: [vpc_endpoint, vpn, nat_allowlist]
streams:
  strategy: discovery_by_pattern
  defaults:
    key_strategy: synthetic_file_row
    cursor_strategy: file_checkpoint
```

## Throttling and Retries
Throttle listing and downloads to protect endpoints. 
Retry transient failures and resume partial downloads when possible.

## Error Handling
Classify failures by file. 
Skip corrupt files with an error record and continue.

## Schema Handling
Infer schema for CSV or read schema from Parquet metadata. 
Store inferred schemas in the schema registry and raise drift alerts when formats change.

## Observability
Report files discovered, files processed, bytes read, and rows emitted. 
Log per file outcomes and checksums.

## Testing
Unit tests for pattern matching and checkpoint logic. 
Integration tests with sample archives. 
Certification in Lambda and Fargate, and Glue for large backfills.

## Limits and Considerations
- Very large files require chunked parsing and memory limits
- Fixed width formats need explicit layouts
- Timestamps in file names can be out of order

## Relationships
Uses state registry for file checkpoints and schema registry for inferred schemas.

## Exclusions
No business mappings or onboarding steps.
