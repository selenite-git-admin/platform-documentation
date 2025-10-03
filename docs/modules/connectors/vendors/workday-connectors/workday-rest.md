# WORKDAY REST CONNECTOR

## Purpose
Describe development requirements for the Workday REST connector. 
It standardizes authentication, discovery, pagination, incremental extraction, and idempotent landing for Workday JSON resources.

## Scope
Reads data from Workday REST APIs across HCM, Finance, Recruiting, and other domains. 
Supports discovery from metadata or OpenAPI, incremental extraction using timestamp cursors, and reliable pagination. 
Includes rate limiting, retries, error handling, observability, and CI certification.

## Supported Versions
- Workday REST APIs that expose JSON and pagination
- Tenant specific endpoints under the Workday domain

## Authentication
- OAuth 2.0 client credentials or authorization code per tenant configuration
- Secrets retrieved from the platform secrets store
- Do not store credentials in code or config files

## Network and Deployment
Runners
- AWS Lambda for light polling
- AWS Fargate for higher throughput and longer jobs

Network patterns
- NAT allowlist for Workday public endpoints
- VPN or PrivateLink style partner connectivity if available through customer networks

## Discovery
Use available metadata endpoints or OpenAPI documents to enumerate resources and fields. 
When metadata is not available use configuration to define resource paths and query parameters. 
Emit streams with stable ids such as workday.rest.workers or workday.rest.positions.

## Incremental Extraction
Prefer timestamp fields such as lastModifiedDateTime or updated. 
Use server side filtering when supported and apply ordering by the cursor field. 
If the API is inclusive around equality use a safety window.

Example request template
```
GET /workers?modifiedFrom=2025-09-30T23:59:59Z&page=1&pageSize=1000
```

## Pagination
Support both token based and page number pagination. 
Stop when token is null or when the result count drops below the page size.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::hcm::workday::cloud::rest
name: Workday REST Connector
taxonomy:
  origin: enterprise
  source: hcm
  provider: workday
  product: cloud
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist, vpn]
streams:
  strategy: discovery_or_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Respect Workday rate limits. 
Retry 429 and 5xx with exponential backoff and jitter. 
Track remaining quota in metrics when headers expose it.

## Error Handling
Classify errors into retryable and terminal. 
Return clear messages with resource path and parameters without exposing secrets.

## Schema Handling
Infer schemas from JSON payloads or reference OpenAPI. 
Register schemas in schema registry and detect drift on field additions or type changes.

## Observability
Metrics: requests, items, latency, errors, retries. 
Logs: resource path, parameters hash, run id. 
Tracing: propagate trace id per request.

## Testing
Unit tests for pagination, cursor handling, and error classification. 
Integration tests against a sandbox tenant. 
Certification in Lambda and Fargate.

## Limits and Considerations
- Some resources do not expose modified timestamps
- Field visibility depends on security groups assigned to the integration user
- Large result sets require conservative page sizes

## Relationships
Uses state registry for cursors and schema registry for payload schemas.

## Exclusions
No GDP mappings or tenant onboarding flows.
