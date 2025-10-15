# SALESFORCE REST

## Purpose
Describe development requirements for the Salesforce REST connector.

## Scope
Reads Salesforce objects using the REST API. 
Supports discovery of SObjects and fields, incremental extraction using SystemModstamp, and bulk pagination. 
Covers authentication, networking, retries, error handling, and observability.

## Supported Versions
- Salesforce Lightning and Classic orgs with REST API enabled
- API versions 54.0 and above recommended

## Authentication
Use OAuth 2.0 with refresh token flow. 
Secrets retrieved from the platform secrets store. 
Do not store credentials in code or config.

## Network and Deployment
Supported runners
- AWS Lambda for most workloads
- AWS Fargate for high volume extracts

Network patterns
- NAT allowlist for Salesforce public endpoints
- PrivateLink if Salesforce exposes a private endpoint (when available)

## Discovery
Call `describeGlobal()` to list all objects. 
For each object call `describeSObject()` to obtain fields, keys, and whether SystemModstamp is supported.

## Incremental Extraction
Use SystemModstamp as cursor for most standard and custom objects. 
Fallback to full refresh when not supported.

SOQL pattern
```sql
SELECT Id, Name, SystemModstamp 
FROM Account 
WHERE SystemModstamp > :cursor 
ORDER BY SystemModstamp ASC 
LIMIT 2000
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::crm::salesforce::cloud::rest
name: Salesforce REST Connector
taxonomy:
  origin: enterprise-connectors
  source: crm
  provider: salesforce
  product: cloud
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Respect Salesforce API limits (15k requests per 24h per licensed user, etc). 
Use retry with exponential backoff on 429 and 5xx. 
Track API usage in metrics.

## Error Handling
Classify errors clearly.
- Retryable: 429, 500, 503
- Terminal: invalid session, permission denied
Return error with object name and SOQL.

## Schema Handling
Emit object schemas and register in schema registry. 
Raise drift alerts when fields are added, removed, or type changed.

## Observability
Log object, SOQL, run id, and tenant id. 
Report metrics for rows read, rows emitted, API calls, errors, and retries. 
Trace each request with trace id.

## Testing
Unit tests for SOQL generation, discovery parsing, and cursor logic. 
Integration tests against a sandbox org. 
Certification in Lambda and Fargate.

## Limits and Considerations
- Some objects are read only via REST
- API limits are strict, design around them
- Fields may be hidden by profile

## Relationships
Uses state registry for SystemModstamp cursors and schema registry for object schemas.

## Exclusions
No GDP mappings or onboarding flows.
