# TALLY ODBC

## Purpose
Describe development requirements for the Tally ODBC connector.

## Scope
Reads data from Tally ERP systems via ODBC. 
Supports incremental extraction by filtering on modification dates. 
Covers authentication, network, retries, error handling, and observability.

## Supported Versions
- Tally.ERP 9 and TallyPrime with ODBC server enabled

## Authentication
- ODBC DSN with credentials
- Secrets retrieved from platform secrets store

## Network and Deployment
Supported runners
- AWS Fargate or EC2 with ODBC drivers installed

Network patterns
- VPN or site-to-site for on-prem Tally servers

## Discovery
Use ODBC catalog queries to list available tables and columns. 
Emit streams with table names, keys, and cursors.

## Incremental Extraction
Use `LASTMODIFIEDDATE` or similar fields. 
Filter queries accordingly.

Example SQL
```sql
SELECT VoucherID, Date, LastModifiedDate 
FROM Vouchers 
WHERE LastModifiedDate > ? 
ORDER BY LastModifiedDate ASC
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::tally::onprem::odbc
name: Tally ODBC Connector
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: tally
  product: erp9
  method: odbc
runtime:
  supported_runners: [fargate, ec2]
  network_patterns: [vpn]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
ODBC queries must be tuned to avoid overwhelming the Tally server. 
Use smaller batch sizes and backoff on failures.

## Error Handling
- Retryable: timeout, transient network errors
- Terminal: invalid SQL, authentication failure

## Schema Handling
Emit schemas from ODBC metadata and register in schema registry. 
Raise drift alerts when fields change.

## Observability
Log SQL, table names, and run id. 
Metrics for rows read, rows emitted, errors, retries.

## Testing
Unit tests for SQL generation and cursor handling. 
Integration tests against a Tally ODBC server.

## Limits and Considerations
- ODBC server must be enabled and configured properly
- Performance is limited by Tally server resources

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding flows.
