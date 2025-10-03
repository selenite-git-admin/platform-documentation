# SAP CPI

## Purpose
Describe the development requirements for the SAP CPI connector that consumes integrations exposed through SAP Cloud Platform Integration.

## Scope
Consumes messages or API outputs delivered by SAP CPI endpoints. 
Supports polling or webhook styles depending on CPI configuration. 
Handles incremental state through message identifiers or timestamps.

## Supported Versions
- SAP CPI endpoints that expose REST or webhook delivery

## Authentication
OAuth 2.0 where available. Basic is allowed only for lab systems when policy allows. 
Secrets are retrieved from the platform secrets store.

## Network and Deployment
Supported runners
- AWS Lambda for webhook handlers and light polling
- AWS Fargate for polling with heavier dependencies or scheduled batches

Supported network patterns
- NAT allowlist for CPI public endpoints where IP allowlisting is configured
- PrivateLink when CPI is reachable through partner connectivity
- VPN when CPI is exposed internally

## Discovery
Discovery is configuration driven. 
List available CPI flows or endpoints from configuration and emit streams for each flow.

## Incremental Processing
Use message id, timestamp, or CPI provided checkpoint tokens as cursors. 
Apply safety windows for late messages. 
Ensure idempotency by de duplicating on message id and cursor.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::erp::sap::sap_cpi::rest
name: SAP CPI Connector
taxonomy:
  origin: enterprise
  source: erp
  provider: sap
  product: cpi
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist, privatelink, vpn]
streams:
  strategy: discovery_by_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Respect CPI rate limits. 
For webhooks handle retries idempotently using message ids. 
For polling use backoff with jitter.

## Error Handling
Differentiate delivery failures from auth or connectivity. 
Return clear messages with flow name and request parameters.

## Schema Handling
Schemas come from CPI flow definitions or sample payloads. 
Register discovered schemas in the schema registry and raise drift alerts on changes.

## Observability
Log flow names, message counts, and latencies. 
Publish metrics for delivered messages, failed messages, and retries.

## Testing
Unit tests for id generation and de duplication. 
Integration tests with a sample CPI flow. 
Certification in Lambda and Fargate patterns.

## Limits and Considerations
- Webhook security requires signature validation
- Large payloads may need chunking
- CPI error responses vary by flow

## Relationships
Uses state registry for message checkpoints and schema registry for payload schemas.

## Exclusions
No business mappings or onboarding steps.
