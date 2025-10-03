# NETSUITE SOAP

## Purpose
Describe development requirements for the NetSuite SOAP API connector (SuiteTalk).

## Scope
Reads records using NetSuite SOAP API. 
Supports discovery of record types, incremental extraction with `lastModifiedDate`, and batching.

## Supported Versions
- NetSuite accounts with SuiteTalk SOAP enabled

## Authentication
- Token-based authentication for SuiteTalk SOAP
- Secrets retrieved from platform secrets store

## Network and Deployment
Supported runners
- AWS Fargate (preferred for SOAP)
- AWS EC2 when special libraries required

Network patterns
- NAT allowlist for SOAP endpoints

## Discovery
Use `getAll` or `getSelectValue` operations to enumerate record types. 
Emit streams for supported objects.

## Incremental Extraction
Use `search` with `lastModifiedDate` filter. 
Batch through paged search results.

Example
```xml
<search>
  <basic>
    <lastModifiedDate operator="after" value="2025-01-01T00:00:00Z"/>
  </basic>
</search>
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::erp::netsuite::cloud::soap
name: NetSuite SOAP Connector
taxonomy:
  origin: enterprise
  source: erp
  provider: netsuite
  product: cloud
  method: soap
runtime:
  supported_runners: [fargate, ec2]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
SOAP API has governance limits. 
Throttle and backoff on errors. 
Retry transient errors.

## Error Handling
- Retryable: timeout, 5xx, rate limit
- Terminal: invalid record, permission denied

## Schema Handling
Emit schemas from WSDL or describe calls. 
Register in schema registry.

## Observability
Log record type, SOAP action, request id. 
Metrics: rows read, errors, retries.

## Testing
Unit tests for WSDL parsing, SOAP message construction. 
Integration tests with sandbox.

## Limits and Considerations
- SOAP API is legacy and heavier
- Coverage may be broader than REST for some objects

## Relationships
Uses state registry for `lastModifiedDate`. 
Schema registry stores schemas.

## Exclusions
No GDP mappings or onboarding flows.
