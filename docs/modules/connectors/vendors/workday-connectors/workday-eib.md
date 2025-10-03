# WORKDAY EIB CONNECTOR

## Purpose
Describe development requirements for the Workday Enterprise Interface Builder connector. 
It standardizes ingestion of EIB exports delivered as files through SFTP or object storage.

## Scope
Consumes EIB output files such as CSV, XML, or ZIP. 
Treats ingestion as a file connector with Workday specific patterns. 
Supports incremental processing using file checkpoints.

## Supported Versions
- Workday tenants delivering EIB outputs via secure transfer

## Authentication
- SFTP key based authentication
- IAM roles for object storage destinations
- Secrets from platform secrets store

## Network and Deployment
Runners
- AWS Lambda for small to medium files
- AWS Fargate for larger files
- AWS Glue for backfills

Network patterns
- VPN for SFTP
- VPC endpoints for object stores

## Discovery
Configuration defines expected EIB paths and file patterns. 
Emit streams like workday.eib.payroll_csv and workday.eib.benefits_xml.

## Incremental Processing
Use file checkpoint strategy path plus checksum. 
Idempotent landing with compound key stream id file path and row index.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::hcm::workday::cloud::eib
name: Workday EIB Connector
taxonomy:
  origin: enterprise
  source: hcm
  provider: workday
  product: cloud
  method: eib
runtime:
  supported_runners: [lambda, fargate, glue]
  network_patterns: [vpn, vpc_endpoint]
streams:
  strategy: discovery_by_pattern
  defaults:
    key_strategy: synthetic_file_row
    cursor_strategy: file_checkpoint
```

## Throttling and Retries
Throttle listings and downloads. 
Retry transient failures and resume partial downloads.

## Error Handling
Classify failures by file and continue with the next file. 
Log clear messages with file path and reason.

## Schema Handling
Infer schema for CSV or read schema from XML. 
Register in schema registry and raise drift alerts when formats change.

## Observability
Metrics: files discovered, files processed, rows emitted, bytes, errors. 
Logs: file path, size, checksum, run id.

## Testing
Unit tests for pattern matching and checkpoint logic. 
Integration tests with sample EIB outputs. 
Certification in Lambda and Fargate and Glue for backfills.

## Limits and Considerations
- EIB definitions can change without notice
- Large payroll files require streaming parsers
- Timestamps in file names may not reflect content modification time

## Relationships
Uses state registry for file checkpoints and schema registry for inferred schemas.

## Exclusions
No GDP mappings or onboarding flows.
