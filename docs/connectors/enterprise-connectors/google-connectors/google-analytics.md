# GOOGLE ANALYTICS CONNECTOR

## Purpose
Provide a connector for ingesting data from Google Analytics APIs. 
Supports Universal Analytics (legacy) and Google Analytics 4 (GA4) Data API. 
Handles authentication, discovery, incremental extraction, and schema registration.

## Scope
- GA4 Data API for event-level and aggregated metrics
- Universal Analytics Reporting API (deprecated but may be required for historical backfills)
- Incremental extraction using date ranges and cursors

## Authentication
- OAuth2 client credentials for user delegated access
- Service account authentication for server-to-server integrations
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- AWS Lambda for scheduled lightweight queries
- AWS Fargate for larger query sets or backfills

Network patterns
- NAT allowlist for Google APIs

## Discovery
Supports dynamic discovery of available GA properties and views. 
Streams generated per property and report configuration.

## Incremental Extraction
Use date-based parameters `startDate` and `endDate`. 
Support cursor fields such as eventDate for GA4. 
Apply safety windows to avoid data latency issues.

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::analytics::google::ga4::rest
name: Google Analytics Connector
taxonomy:
  origin: third_party
  source: analytics
  provider: google
  product: ga4
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
Respect Google Analytics quotas and rate limits. 
Retry 429s with exponential backoff and jitter.

## Error Handling
Classify errors by property or report. 
Surface descriptive errors without exposing tokens.

## Schema Handling
Infer schema from report metadata. 
Register schemas and track drift when fields change.

## Observability
Metrics: requests, rows, bytes, retries, errors. 
Logs: property id, view id, query hash, run id.

## Testing
Unit tests for date windowing and cursor logic. 
Integration tests with GA demo account.

## Limits and Considerations
- Universal Analytics sunset reduces coverage
- GA4 sampling can affect query accuracy
- Event schema may evolve frequently

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No tenant onboarding flows or UI references.
