# FACEBOOK PAGES INSIGHTS CONNECTOR

## Purpose
Ingest Facebook Page analytics and insights for owned Pages. 
Standardize authentication, discovery of pages, metric selection, and incremental date pulls.

## Scope
- Insights metrics: page_impressions, page_fans, page_engaged_users, etc.
- Page metadata: name, category, verification, fan_count

## Supported Versions
- Graph API v18.0 or later

## Authentication
- OAuth2 user access token with required Page permissions
- Long-lived tokens preferred
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- Lambda for light scheduled pulls
- Fargate for larger page fleets

Network patterns
- NAT allowlist for Graph API endpoints

## Discovery
List Pages accessible to the token. 
Emit one stream per Page for insights and a metadata stream.

## Incremental Extraction
Date-based parameters `since` and `until`. 
Use daily granularity and a sliding window for the last N days to correct late postings. 
Keyed by (page_id, metric, end_time).

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::social::meta::facebook_pages::rest
name: Facebook Pages Insights Connector
taxonomy:
  origin: third_party
  source: social
  provider: meta
  product: facebook_pages
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared
    cursor_strategy: date_range
```

## Throttling and Retries
Respect rate limits. 
Retry 429 and 5xx with backoff and jitter.

## Error Handling
Report Page id, metric, and date range on failure. 
Handle permission changes gracefully by skipping revoked Pages.

## Schema Handling
Infer schemas from metric definitions and metadata fields. 
Register in schema registry and track drift.

## Observability
Metrics: requests, rows, pages, retries. 
Logs: page id, metric group, run id.

## Testing
Unit tests for date windowing and metric selection. 
Integration tests against test Pages.

## Limits and Considerations
- Metrics availability depends on Page permissions
- Historical range may be limited for some metrics

## Relationships
Uses state registry for cursors and schema registry for insight schemas.

## Exclusions
No onboarding or UI flows.
