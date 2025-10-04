# GOOGLE ADSENSE CONNECTOR

## Purpose
Ingest revenue and performance data from Google AdSense. 
Supports reports and account metadata. 
Handles authentication, date-based incremental pulls, and schema validation.

## Scope
- AdSense Management API
- Reports: Earnings, Ad Units, Sites, Custom Channels

## Authentication
- OAuth2 client credentials
- Secrets in platform secrets manager

## Network and Deployment
Runners
- Lambda for scheduled pulls
- Fargate for large reports

Network patterns
- NAT allowlist for Google APIs

## Discovery
List AdSense accounts and available reports. 
Emit streams such as google.adsense.earnings.

## Incremental Extraction
Use `startDate` and `endDate` parameters. 
Sliding windows for latency correction.

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::ads::google::adsense::rest
name: Google AdSense Connector
taxonomy:
  origin: third_party
  source: ads
  provider: google
  product: adsense
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
Respect daily quota. 
Retry on 429 and 5xx.

## Error Handling
Surface report id and date range in logs. 
Skip empty responses gracefully.

## Schema Handling
Infer schema from report headers. 
Register schemas in registry.

## Observability
Metrics: requests, rows, bytes, retries. 
Logs: account id, report id, query hash.

## Testing
Unit tests for date logic. 
Integration tests with sample AdSense accounts.

## Limits and Considerations
- Daily quota limits large tenants
- Historical data may have sampling

## Relationships
State registry for cursors, schema registry for schemas.

## Exclusions
No onboarding or UI flows.
