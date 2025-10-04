# META CONVERSIONS API CONNECTOR

## Purpose
Ingest server-side conversion events delivered to Meta via the Conversions API, either by polling event delivery logs or receiving mirrored webhooks for analytics parity.

## Scope
- Pull mode: fetch event delivery statuses where available
- Push mode: receive mirrored events via webhook before forwarding to Meta
- Use case: build full-funnel KPI models that reconcile ad spend with downstream conversions

## Supported Versions
- Conversions API current endpoints

## Authentication
- OAuth2 app credentials for pull mode
- Webhook signing secrets for push mode
- Secrets stored in platform secrets manager

## Network and Deployment
Runners
- Lambda behind API Gateway for webhooks
- Fargate for polling and reconciliation jobs

Network patterns
- Public endpoint with WAF and IP allowlists for webhooks
- NAT allowlist for Graph API

## Discovery
Configuration-driven. 
Define event types and endpoints per ad account or pixel id. 
Emit streams for delivered events and delivery statuses.

## Incremental Processing
Pull mode: date range pagination with last timestamp cursor. 
Push mode: event id and timestamp as cursor. 
Idempotency by composite key (pixel_id, event_id, event_time).

## Manifest
```yaml
manifest_version: 1.0
id: conn::third_party::ads::meta::conversions_api::rest
name: Meta Conversions API Connector
taxonomy:
  origin: third_party
  source: ads
  provider: meta
  product: conversions_api
  method: rest_or_webhook
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery_by_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: date_range_or_event_id
```

## Throttling and Retries
Honor provider retry guidance. 
Use DLQ for poison messages in webhook mode. 
Retry transient 5xx in pull mode with backoff.

## Error Handling
Validate webhook signatures. 
Surface pixel id and event id for failures. 
Separate transport failures from validation errors.

## Schema Handling
Register event schemas and status schemas. 
Ring alarm on drift that drops required fields for attribution.

## Observability
Metrics: events received, events pulled, retries, DLQ count. 
Logs: pixel id, event id, signature status, run id.

## Testing
Unit tests for signature validation and idempotency. 
Integration tests with sandbox pixels.

## Limits and Considerations
- Privacy requirements for user data hashing and salting apply
- Deduplication requires consistent event_id across client and server
- Delivery status visibility varies by account access

## Relationships
Works with state registry for cursors and schema registry for event schemas. 
Relates to Meta Ads connector for KPI reconciliation.

## Exclusions
No tenant onboarding or UI configuration flows.
