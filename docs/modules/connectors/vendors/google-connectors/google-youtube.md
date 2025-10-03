# GOOGLE YOUTUBE CONNECTOR

## Purpose
Provide a connector for ingesting YouTube Analytics and Reporting API data. 
Supports channel and video level metrics. 
Handles authentication, incremental extraction, and schema registration.

## Scope
- YouTube Analytics API
- YouTube Reporting API (bulk exports)

## Authentication
- OAuth2 client credentials
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- Lambda for light queries
- Fargate for large report downloads

Network patterns
- NAT allowlist for Google APIs

## Discovery
List accessible channels and reports. 
Emit streams such as google.youtube.analytics_videos.

## Incremental Extraction
Use date-based parameters for Analytics API. 
For Reporting API consume file-based exports with checkpointing.

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::media::google::youtube::rest
name: Google YouTube Connector
taxonomy:
  origin: third_party
  source: media
  provider: google
  product: youtube
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery_or_config
  defaults:
    key_strategy: source_declared
    cursor_strategy: date_range_or_file_checkpoint
```

## Throttling and Retries
Respect API quotas. 
Retry on 429 and transient 5xx.

## Error Handling
Log channel id, report id, and query parameters. 
Skip unavailable reports gracefully.

## Schema Handling
Infer schema from API metadata and report headers. 
Register schemas and track drift.

## Observability
Metrics: requests, rows, videos, retries. 
Logs: channel id, query hash, run id.

## Testing
Unit tests for cursor logic and file checkpointing. 
Integration tests with sandbox channels.

## Limits and Considerations
- Quota limits per channel
- Reporting API delivers files with latency of 1–2 days

## Relationships
Uses state registry and schema registry.

## Exclusions
No onboarding or UI configuration.
