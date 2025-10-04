# INSTAGRAM GRAPH CONNECTOR

## Purpose
Ingest Instagram Business and Creator account insights via Instagram Graph API. 
Standardize authentication, discovery, and incremental metrics pulls.

## Scope
- Account-level insights (followers, impressions, reach, profile views)
- Media insights (likes, comments, saves, reach, impressions)
- Hashtag search and insights when permitted

## Supported Versions
- Instagram Graph API v18.0 or later

## Authentication
- OAuth2 user access token with Instagram Business permissions
- Long-lived tokens preferred
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- Lambda for scheduled pulls
- Fargate for multiple accounts and media backfills

Network patterns
- NAT allowlist for Graph API endpoints

## Discovery
List connected Instagram Business accounts. 
Emit one or more streams per account for account insights and media insights.

## Incremental Extraction
Use date-based `since` and `until` for account insights. 
For media insights, page over media items and fetch metrics for new or updated posts within a sliding window. 
Keys: (ig_user_id, metric, end_time) and (media_id, metric, end_time).

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::social::meta::instagram_graph::rest
name: Instagram Graph Connector
taxonomy:
  origin: third_party
  source: social
  provider: meta
  product: instagram_graph
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
Respect API rate limits. 
Retry 429 and 5xx with exponential backoff and jitter.

## Error Handling
Report account id or media id and metric on failure. 
Handle permission revocation and invalid media gracefully.

## Schema Handling
Infer schemas from insights responses and media fields. 
Register in schema registry and track drift.

## Observability
Metrics: requests, rows, accounts, media items, retries. 
Logs: ig_user_id, media id, metric group, run id.

## Testing
Unit tests for windowing and pagination. 
Integration tests with sandbox Business accounts.

## Limits and Considerations
- Some insights are aggregated and not event level
- Historical ranges may be restricted per metric
- Media endpoints paginate differently from account insights

## Relationships
Uses state registry for date cursors and schema registry for payload schemas.

## Exclusions
No onboarding or UI configuration flows.
