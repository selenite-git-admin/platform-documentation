# SAP CDS

## Purpose
Describe the development requirements for the SAP CDS connector that reads Core Data Services views exposed by SAP.

## Scope
Reads data from CDS views in SAP S4HANA. 
Supports discovery of available views through metadata endpoints or configured lists. 
Supports incremental extraction where change timestamps are available. 
Covers authentication, networking, retries, error handling, and observability.

## Supported Versions
- SAP S4HANA CDS views accessible through OData or SQL style exposure depending on deployment

## Authentication
Use the same modes as the gateway that exposes CDS. 
OAuth 2.0 is preferred. Basic is allowed only for test systems when policy allows. 
Secrets are retrieved from the platform secrets store.

## Network and Deployment
Supported runners
- AWS Fargate for most workloads
- AWS Lambda for light reads when service supports it

Supported network patterns
- VPN for internal gateways
- PrivateLink when CDS exposure is behind an internal NLB
- NAT allowlist only when strictly necessary

## Discovery
Enumerate CDS views by introspecting metadata or by reading a configured allowlist. 
Emit streams with stable identifiers and propose keys and cursors when available.

## Incremental Extraction
Use available change timestamps or version fields as cursors. 
Fallback to full refresh if not present. 
Apply safety windows to account for late arriving changes.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::erp::sap::sap_s4hana::cds
name: SAP S4HANA CDS Connector
taxonomy:
  origin: enterprise
  source: erp
  provider: sap
  product: s4hana
  method: cds
runtime:
  supported_runners: [fargate, lambda]
  network_patterns: [vpn, private_link, nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Respect service limits. Use backoff with jitter. 
Prefer smaller page sizes when views are complex.

## Error Handling
Differentiate query errors from auth or connectivity issues. 
Return actionable messages with view name and query parameters.

## Schema Handling
Emit discovered schemas and register them in the schema registry. 
Do not embed schemas inline in manifests.

## Observability
Log view names, query parameters, and response sizes. 
Report metrics for rows read, rows emitted, and latency.

## Testing
Unit tests for discovery and paging. 
Integration tests against a sandbox with representative views. 
Certification requires runs in at least one supported runner and network pattern.

## Limits and Considerations
- Some CDS views are virtual and heavy to compute
- Filters may be restricted by the gateway
- Sorting by cursor fields may require indexing on the source

## Relationships
Uses state registry for cursors and schema registry for schema versions.

## Exclusions
No business mappings or tenant onboarding steps.
