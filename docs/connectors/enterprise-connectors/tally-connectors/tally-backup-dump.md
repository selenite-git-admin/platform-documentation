# TALLY BACKUP DUMP CONNECTOR

## Purpose
Describe development requirements for the Tally Backup / Dump File connector. 
This connector ingests periodic Tally backup or export files after they are restored or exported into common formats. 
It treats the ingestion as a file source problem, ensuring idempotent and incremental loading.

## Scope
Ingests CSV, XML, or other export files produced from Tally backups or scheduled exports. 
Supports discovery by file pattern, incremental processing by file path and checksum, and idempotent landing.

## Supported Formats
- CSV, XML, or Parquet produced from exports
- Compressed archives such as gzip or zip containing the above

## Authentication
- IAM role or service account for object storage (S3, Blob, GCS)
- Key-based auth for SFTP drops
- Secrets retrieved from platform secrets store

## Network and Deployment
Supported runners
- AWS Lambda for small to medium files
- AWS Fargate for larger files
- AWS Glue for very large historical backfills

Supported network patterns
- VPC endpoints for cloud object stores
- VPN for on-prem SFTP
- NAT allowlist for public SFTP if allowed

## Discovery
List files under configured prefixes and match patterns. 
Emit streams such as file.s3.tally.ledgers_csv or file.s3.tally.vouchers_xml. 

## Incremental Processing
Use a checkpoint consisting of file path + checksum. 
Process only new or changed files. 
Ensure idempotency by generating compound keys (stream_id + file path + row index).

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::tally::backup::file_dump
name: Tally Backup Dump Connector
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: tally
  product: backup
  method: file_dump
runtime:
  supported_runners: [lambda, fargate, glue]
  network_patterns: [vpc_endpoint, vpn, nat_allowlist]
streams:
  strategy: discovery_by_pattern
  patterns:
    - id: file.s3.tally.ledgers_csv
      path: s3://org/tally/ledgers/*.csv
    - id: file.s3.tally.vouchers_xml
      path: s3://org/tally/vouchers/*.xml
defaults:
  key_strategy: synthetic_file_row
  cursor_strategy: file_checkpoint
```

## Throttling and Retries
Throttle file listing and downloads to avoid overloading endpoints. 
Retry transient failures and resume partial downloads.

## Error Handling
Classify errors by file. 
Skip corrupt files with an error record but continue processing others.

## Schema Handling
Infer schema from CSV headers or XML structure. 
Register inferred schemas in schema registry. 
Raise drift alerts when schema changes are detected.

## Observability
Metrics include files discovered, processed, bytes read, rows emitted, errors, retries. 
Logs must include file path, size, checksum, and run id.

## Testing
Unit tests for file pattern matching and checkpoint logic. 
Integration tests with sample Tally exports. 
Certification in Lambda and Fargate; Glue for backfills.

## Limits and Considerations
- Backup files are proprietary; connector cannot parse them directly
- Always restore and export into supported formats
- Export coverage depends on TDL scripts or definitions

## Relationships
Uses state registry for file checkpoints. 
Uses schema registry for inferred schemas. 
Cross-links with global file connectors.

## Exclusions
No business mappings or onboarding flows.
