# FILE CONNECTOR (GLOBAL)

## Purpose
Provide a vendor independent connector for ingesting files from object storage or file drops. 
It handles discovery by path patterns, incremental processing by file checkpoints, and idempotent landing.

## Scope
Supports CSV, JSON, Parquet, Avro, Excel, and compressed archives where applicable. 
Works with S3, Azure Blob, GCS, SFTP, and local staging. 
Covers authentication, networking, schema inference, retries, and observability.

## Supported Formats
- CSV with headers
- JSON lines and JSON files
- Parquet and Avro
- Excel XLSX
- Gzip or Zip of the above

## Authentication
- IAM roles or service accounts for cloud object stores
- Key based auth for SFTP
- Secrets retrieved from the platform secrets store

## Network and Deployment
Runners
- AWS Lambda for small to medium files
- AWS Fargate for large files
- AWS Glue for heavy backfills

Network patterns
- VPC endpoints for S3, Blob, GCS proxies
- VPN for SFTP
- NAT allowlist when public endpoints are required

## Discovery
List files under configured prefixes and match patterns to define streams. 
Example streams
- file.s3.sales_orders_csv from s3://org/sales/orders/*.csv
- file.sftp.invoices_json from sftp://partner/invoices/*.json

## Incremental Processing
Use a checkpoint composed of file path plus checksum. 
Only process new or changed files. 
Guarantee idempotency by using a compound key of stream id, file path, and row index.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::file::object_store::ingest
name: Global File Connector
taxonomy:
  origin: third_party
  source: file
  provider: generic
  product: object_store
  method: ingest
runtime:
  supported_runners: [lambda, fargate, glue]
  network_patterns: [vpc_endpoint, vpn, nat_allowlist]
streams:
  strategy: discovery_by_pattern
  patterns:
    - id: file.s3.sales_orders_csv
      path: s3://org/sales/orders/*.csv
defaults:
  key_strategy: synthetic_file_row
  cursor_strategy: file_checkpoint
```

## Throttling and Retries
Throttle listings and downloads. 
Retry transient errors and resume partial downloads. 
Use backoff with jitter.

## Error Handling
Classify failures by file. 
Skip corrupt files with an error record and continue.

## Schema Handling
Infer schema for CSV and JSON. 
Read embedded schema for Avro and Parquet. 
Register schemas in the schema registry and raise drift alerts on change.

## Observability
Metrics: files discovered, processed, bytes, rows, errors, retries. 
Logs: file path, size, checksum, run id.

## Testing
Unit tests for pattern matching, checkpointing, and parsers. 
Integration tests across supported stores.

## Limits and Considerations
- Excel requires streaming parsers for large sheets
- Mixed schemas across files require per file validation
- Time based partitioned paths should be included in patterns

## Relationships
Uses state registry for checkpoints and schema registry for inferred schemas.

## Exclusions
No business mappings or tenant onboarding.
