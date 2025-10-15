# NETSUITE RESTLET

## Purpose
Describe development requirements for the NetSuite RESTlet connector.

## Scope
Reads and writes data via custom RESTlets deployed in NetSuite. 
Supports incremental extraction when RESTlet scripts expose change fields. 
Covers authentication, network, error handling, and observability.

## Supported Versions
- NetSuite accounts with RESTlets enabled

## Authentication
- OAuth 1.0a token-based authentication (preferred)
- OAuth 2.0 if RESTlet is proxied through an integration gateway
Secrets retrieved from the platform secrets store.

## Network and Deployment
Supported runners
- AWS Lambda for lightweight extracts
- AWS Fargate for longer running calls

Network patterns
- NAT allowlist for NetSuite public endpoints
- VPN when exposed internally through reverse proxy

## Discovery
Discovery is driven by configuration, as RESTlets are custom. 
Connector manifest must specify available endpoints and their payloads.

## Incremental Extraction
Use a timestamp or internalId if exposed by the RESTlet. 
Pass state from orchestrator and update based on results.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::netsuite::cloud::restlet
name: NetSuite RESTlet Connector
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: netsuite
  product: cloud
  method: restlet
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist, vpn]
streams:
  strategy: config_defined
  defaults:
    key_strategy: config_declared
    cursor_strategy: config_declared_or_full_refresh
```

## Throttling and Retries
NetSuite limits concurrent RESTlet calls. 
Throttle requests to avoid exceeding governance units. 
Retry on 429 and 5xx with exponential backoff.

## Error Handling
Classify errors clearly.
- Retryable: transient 5xx, rate limits
- Terminal: invalid script id, authentication failure

## Schema Handling
Schemas defined by RESTlet payloads. 
Register in schema registry from configuration.

## Observability
Log script id, endpoint, request id. 
Metrics for rows read, rows emitted, latency, errors.

## Testing
Unit tests for payload construction and state handling. 
Integration tests with sandbox account.

## Limits and Considerations
- Custom scripts vary widely, connector behavior is only as reliable as RESTlet design
- RESTlet limits apply per account

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding flows.
