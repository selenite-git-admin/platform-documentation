# WEBHOOK CONNECTOR (GLOBAL)

## Purpose
Provide a push based ingestion endpoint for services that deliver events via webhooks. 
It validates signatures, enforces idempotency, and writes to Bronze.

## Scope
Works with common webhook providers. 
Supports HMAC signatures, retry semantics, and dead letter queues.

## Authentication
- Shared secret for signature validation
- Optional basic auth on endpoint

## Network and Deployment
Runners
- AWS Lambda behind API Gateway for serverless handlers
- AWS Fargate for higher throughput

Network patterns
- Public endpoint with IP allowlists or WAF
- PrivateLink if the source is inside AWS

## Discovery
Configuration driven. 
Define event types to accept and their schema references.

## Incremental Processing
Use event id and delivery timestamp as the cursor. 
Ensure idempotency by de duplicating on event id.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::api::webhook::ingest
name: Global Webhook Connector
taxonomy:
  origin: third_party
  source: api
  provider: generic
  product: webhook
  method: ingest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist, private_link]
streams:
  strategy: config_defined
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: event_id
```

## Throttling and Retries
Honor provider retry semantics. 
Use DLQ for poison messages.

## Error Handling
Reject invalid signatures. 
Surface validation errors with event type and reason.

## Schema Handling
Register event schemas in the schema registry. 
Raise drift when providers change payloads.

## Observability
Metrics: events received, accepted, rejected, retries. 
Logs: event id, type, signature status.

## Testing
Unit tests for signature validation and idempotency. 
Integration tests with a mock sender.

## Limits and Considerations
- Replay attacks must be prevented with nonce and timestamp checks
- Burst protection via WAF or rate limits

## Relationships
Uses state registry for event cursors and schema registry for payloads.

## Exclusions
No GDP mappings or onboarding.
