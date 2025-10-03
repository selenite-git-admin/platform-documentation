# SALESFORCE STREAMING

## Purpose
Describe development requirements for the Salesforce Streaming connector.

## Scope
Consumes Salesforce change events and platform events via the Streaming API (CometD). 
Supports incremental state via replayId and ensures at least once delivery.

## Supported Versions
- Salesforce orgs with Streaming API enabled

## Authentication
OAuth 2.0 refresh token flow. 
Secrets retrieved from platform secrets store.

## Network and Deployment
Supported runners
- AWS Fargate for persistent connections
- AWS Lambda for lightweight consumers with short sessions

Network patterns
- NAT allowlist for Salesforce streaming endpoints

## Discovery
List available topics or channels from configuration or metadata API. 
Emit streams with stable ids such as sf.event.account_changes.

## Incremental Processing
Use replayId from last event as checkpoint. 
Store replayId in state registry per stream. 
Ensure idempotency by de duplicating on replayId.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::crm::salesforce::cloud::streaming
name: Salesforce Streaming Connector
taxonomy:
  origin: enterprise
  source: crm
  provider: salesforce
  product: cloud
  method: streaming
runtime:
  supported_runners: [fargate, lambda]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery_by_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: replay_id
```

## Throttling and Retries
CometD protocol includes replay logic. 
Reconnect with last known replayId after disconnects. 
Apply exponential backoff on network failures.

## Error Handling
Classify errors clearly. 
- Retryable: transient disconnects
- Terminal: invalid subscription, permission denied

## Schema Handling
Schema derived from event definitions. 
Emit to schema registry and track changes.

## Observability
Log channel name, replayId, and event counts. 
Metrics: events received, errors, reconnects. 
Tracing links streaming sessions to orchestrator run id.

## Testing
Unit tests for replayId handling and subscription management. 
Integration tests with sandbox orgs. 
Certification in Fargate and Lambda.

## Limits and Considerations
- Persistent connections required for Fargate
- ReplayId has retention limits
- Not all objects generate change events

## Relationships
Uses state registry for replayId checkpoints and schema registry for event payloads.

## Exclusions
No GDP mappings or onboarding flows.
