# GRAPHQL CONNECTOR (GLOBAL)

## Purpose
Provide a generic connector for GraphQL APIs. 
It standardizes schema introspection, pagination, incremental queries, and error handling.

## Scope
Works with GraphQL endpoints that support introspection. 
Handles cursor-based pagination with `pageInfo` and `endCursor` patterns. 
Supports OAuth2 or API key authentication.

## Authentication
- OAuth2 bearer token
- API key header
- Secrets from platform secrets store

## Network and Deployment
Runners
- AWS Lambda for lightweight polling
- AWS Fargate for higher throughput

Network patterns
- NAT allowlist for public endpoints
- VPN for private endpoints

## Discovery
Run GraphQL introspection to build a type map. 
Emit streams for queryable types configured in the connection profile.

## Incremental Extraction
Use `updatedAt` or equivalent fields when present. 
Use cursor-based pagination with `after: <endCursor>` and apply safety windows.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::api::graphql::extract
name: Global GraphQL Connector
taxonomy:
  origin: third_party
  source: api
  provider: generic
  product: graphql
  method: extract
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
Respect per field cost limits if enforced. 
Retry transient errors and rate limits with backoff.

## Error Handling
Handle GraphQL `errors` array and partial data. 
Surface path and message for actionable debugging.

## Schema Handling
Use introspection schema as a reference and infer stream schemas from query selections. 
Register in schema registry.

## Observability
Metrics: requests, items, latency, errors. 
Logs: query hash, variables hash, run id.

## Testing
Unit tests for pagination and query generation. 
Integration tests against a sample endpoint.

## Limits and Considerations
- Introspection may be disabled in production
- Relay style connections required for cursor pagination

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding.
