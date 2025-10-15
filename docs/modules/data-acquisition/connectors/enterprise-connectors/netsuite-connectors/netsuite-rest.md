# NETSUITE REST

## Purpose
Describe development requirements for the NetSuite REST API connector.

## Scope
Reads NetSuite records through the official REST API. 
Supports discovery of record types and fields, incremental extraction with `lastModifiedDate`, and pagination.

## Supported Versions
- NetSuite accounts with REST API v2021+ enabled

## Authentication
- OAuth 2.0 with token-based access (preferred)
- Secrets from platform secrets store

## Network and Deployment
Supported runners
- AWS Lambda for typical workloads
- AWS Fargate for larger extracts

Network patterns
- NAT allowlist for NetSuite REST API endpoints

## Discovery
Use `GET /metadata-catalog` to list available record types. 
Emit streams for each record type with keys and cursors.

## Incremental Extraction
Use `lastModifiedDate` as the cursor. 
Filter with `q` parameter where supported.

Example
```
GET /record/v1/salesOrder?q=lastModifiedDate > '2025-01-01T00:00:00Z'
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::netsuite::cloud::rest
name: NetSuite REST API Connector
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: netsuite
  product: cloud
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
NetSuite REST API has governance limits. 
Throttle requests and retry 429s with backoff.

## Error Handling
- Retryable: 429, transient 5xx
- Terminal: permission denied, invalid record type

## Schema Handling
Emit schemas from metadata-catalog and register in schema registry.

## Observability
Log record type, request id, run id. 
Metrics for records read, errors, retries.

## Testing
Unit tests for metadata parsing, SOQL-style queries, and cursor handling. 
Integration tests with sandbox.

## Limits and Considerations
- API coverage is not complete for all record types
- Some records require SuiteTalk SOAP instead

## Relationships
Uses state registry for `lastModifiedDate`. 
Schema registry stores record schemas.

## Exclusions
No GDP mappings or onboarding flows.
