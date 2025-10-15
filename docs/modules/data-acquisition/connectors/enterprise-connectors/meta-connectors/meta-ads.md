# META ADS CONNECTOR

## Purpose
Provide a connector for ingesting paid media performance data from Meta (Facebook) Marketing API. 
Supports campaign, ad set, ad, creative, and insights resources. 
Standardizes authentication, discovery, incremental extraction, throttling, and schema registration.

## Scope
- Marketing API Insights for metrics (impressions, clicks, spend, conversions)
- Entities: Accounts, Campaigns, AdSets, Ads, Creatives, Audiences
- Breakdowns: date, device, placement, country (configurable)

## Supported Versions
- Meta Marketing API v18.0 or later (update per Meta release cadence)

## Authentication
- OAuth2 user access with system user or app + long-lived access tokens
- Optional app secret proof
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- AWS Fargate for continuous scheduled reporting
- AWS Lambda for small scheduled pulls

Network patterns
- NAT allowlist for Meta Graph API endpoints

## Discovery
Enumerate ad accounts accessible by the token. 
Emit streams for core entities and for configured insights reports per account.

## Incremental Extraction
Use date-based parameters `time_range` and `time_increment`. 
Apply sliding windows for the last N days to correct late-attribution changes. 
Idempotency is enforced by composite key (account_id, entity_id, date, breakdowns).

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::ads::meta::marketing::rest
name: Meta Ads Connector
taxonomy:
  origin: third_party
  source: ads
  provider: meta
  product: marketing
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery_or_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: date_range
```

## Throttling and Retries
Respect per-app and per-user rate limits. 
Retry 429 and transient 5xx with exponential backoff and jitter. 
Use batch size and field selection to manage payload size.

## Error Handling
Classify errors with Graph API error codes. 
Surface clear messages with account id and endpoint summary, without exposing tokens.

## Schema Handling
Infer schemas from field selections and insights definitions. 
Register schemas and detect drift when fields change or when API versions advance.

## Observability
Metrics: requests, rows, spend, retries, errors, quota indications. 
Logs: account id, query hash, run id.

## Testing
Unit tests for date windowing, pagination, and breakdown combinations. 
Integration tests against a sandbox/test ad account.

## Limits and Considerations
- Attribution windows cause late data changes; use sliding windows
- Marketing API versions deprecate regularly; keep manifest compatibility matrix
- Some breakdowns are incompatible with certain metrics

## Relationships
Uses state registry for date cursors and schema registry for report schemas.

## Exclusions
No tenant onboarding or UI configuration flows.
