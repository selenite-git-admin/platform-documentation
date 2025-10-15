# SOAP API CONNECTOR (GLOBAL)

## Purpose
Provide a generic SOAP connector for WSDL-based services. 
It standardizes authentication, discovery, batching, and incremental searches.

## Scope
Works with any SOAP service with accessible WSDL. 
Supports token-based, basic, or mutual TLS authentication.

## Authentication
- Basic auth or token headers
- Mutual TLS where required
- Secrets from platform secrets store

## Network and Deployment
Runners
- AWS Fargate for stable long running jobs
- EC2 for special libraries

Network patterns
- NAT allowlist for public endpoints
- VPN or PrivateLink for private services

## Discovery
Parse the WSDL to list services, ports, operations, and types. 
Emit streams mapped to operations with list or search semantics.

## Incremental Extraction
Use search operations with lastModifiedDate or equivalent filter. 
Batch through paged responses.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::api::soap::extract
name: Global SOAP Connector
taxonomy:
  origin: third_party
  source: api
  provider: generic
  product: soap
  method: extract
runtime:
  supported_runners: [fargate, ec2]
  network_patterns: [nat_allowlist, vpn, private_link]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Throttle requests and retry transient faults. 
Backoff with jitter.

## Error Handling
Surface SOAP fault codes and operation names. 
Differentiate retryable transport errors from terminal faults.

## Schema Handling
Generate schemas from XSD types. 
Register in schema registry and track versioning.

## Observability
Metrics: calls, latency, faults, retries. 
Logs: operation, soapAction, request id, run id.

## Testing
Unit tests for WSDL parsing and envelope construction. 
Integration tests against at least one real SOAP endpoint.

## Limits and Considerations
- Large XSDs require careful memory management
- Some services have strict message size limits

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding.
