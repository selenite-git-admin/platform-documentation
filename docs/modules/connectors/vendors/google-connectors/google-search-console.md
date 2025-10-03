# GOOGLE SEARCH CONSOLE CONNECTOR

## Purpose
Provide a connector for ingesting site performance data from Google Search Console. 
Supports search analytics queries and site metadata.

## Scope
- Search Analytics API
- Sites API

## Authentication
- OAuth2 client credentials
- Secrets in platform secrets manager

## Network and Deployment
Runners
- Lambda for lightweight queries
- Fargate for scheduled backfills

Network patterns
- NAT allowlist for Google APIs

## Discovery
List verified sites for the authenticated account. 
Emit streams such as google.search_console.search_analytics.

## Incremental Extraction
Use date-based parameters `startDate` and `endDate`. 
Support sliding windows for recent days due to data latency.

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::seo::google::searchconsole::rest
name: Google Search Console Connector
taxonomy:
  origin: third_party
  source: seo
  provider: google
  product: searchconsole
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
Respect per-user quotas. 
Retry on 429 with backoff.

## Error Handling
Surface site id and query parameters. 
Skip unavailable sites gracefully.

## Schema Handling
Infer schema from search analytics dimensions. 
Register schemas and detect drift.

## Observability
Metrics: requests, rows, queries, retries. 
Logs: site id, query hash, run id.

## Testing
Unit tests for date logic and dimensions. 
Integration tests with sample sites.

## Limits and Considerations
- Data available only for last 16 months
- Latency of up to 3 days for fresh data

## Relationships
Uses state registry and schema registry.

## Exclusions
No onboarding flows.
