# GOOGLE ADS CONNECTOR

## Purpose
Provide a connector for ingesting campaign and performance data from Google Ads API. 
Supports authentication, discovery, incremental pulls, schema handling, and observability.

## Scope
- Google Ads API v15 and later
- Entities: Campaigns, Ad Groups, Keywords, Performance Reports

## Authentication
- OAuth2 client credentials with refresh tokens
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- AWS Fargate for continuous reporting
- Lambda for small scheduled pulls

Network patterns
- NAT allowlist for Google APIs

## Discovery
Enumerate accessible accounts and campaigns. 
Emit streams such as google.ads.campaign_performance.

## Incremental Extraction
Use date-based parameters `segments.date`. 
Apply sliding windows for partial-day updates. 
Support custom report queries.

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::ads::google::ads::rest
name: Google Ads Connector
taxonomy:
  origin: third_party
  source: ads
  provider: google
  product: ads
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: config_defined
  defaults:
    key_strategy: source_declared
    cursor_strategy: date_range
```

## Throttling and Retries
Respect Google Ads quotas and rate limits. 
Retry 429s and quota exceeded errors.

## Error Handling
Surface descriptive messages per account and query. 
Classify transient vs terminal errors.

## Schema Handling
Infer schema from Ads API query fields. 
Register schemas in registry.

## Observability
Metrics: requests, rows, retries, quota usage. 
Logs: account id, campaign id, query hash.

## Testing
Unit tests for query construction and cursor logic. 
Integration tests with sandbox accounts.

## Limits and Considerations
- Quotas vary by account
- Sampling may apply to some report types

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No onboarding or UI configuration flows.
