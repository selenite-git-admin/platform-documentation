# REST API CONNECTOR (GLOBAL)

## Purpose
Provide a generic REST connector for APIs that support HTTP based access. 
It standardizes authentication, pagination, incremental cursors, and error handling.

## Scope
Works with OpenAPI documented services or custom REST endpoints. 
Supports OAuth2, API keys, HMAC signatures, and custom headers. 
Covers request shaping, rate limiting, retries, and observability.

## Authentication
- OAuth2 client credentials or authorization code
- API keys in headers
- HMAC signatures when required
- Secrets from platform secrets store

## Network and Deployment
Runners
- AWS Lambda for light polling
- AWS Fargate for heavier workloads

Network patterns
- NAT allowlist for public APIs
- PrivateLink or VPN for private endpoints

## Discovery
Use OpenAPI where available to enumerate resources and fields. 
When not available, discovery is config-driven with endpoint templates.

## Incremental Extraction
Use timestamp or id cursors when the API supports filtering. 
Otherwise use updated_since parameters or ETag based pagination. 
Ensure idempotency by including a stable resource id in the envelope.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::api::rest::extract
name: Global REST API Connector
taxonomy:
  origin: third_party
  source: api
  provider: generic
  product: rest
  method: extract
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist, private_link, vpn]
streams:
  strategy: discovery_or_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Rate limit per API guidance. 
Retry 429 and 5xx with exponential backoff and jitter.

## Error Handling
Classify 4xx vs 5xx. 
Surface terminal errors with endpoint and parameters, without secrets.

## Schema Handling
Infer schema from JSON samples or reference OpenAPI schemas. 
Register in schema registry. 
Raise drift alerts on shape changes.

## Observability
Metrics: requests, latency, errors, retries, bytes. 
Logs: endpoint, method, parameters hash, run id.

## Testing
Unit tests for pagination and cursor handling. 
Integration tests against a mock server and one real API.

## Limits and Considerations
- Heterogeneous pagination styles must be abstracted
- Date filters can be inclusive; use safety windows
- API versioning changes require manifest updates

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding.
