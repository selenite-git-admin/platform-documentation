# WORKDAY RAAS CONNECTOR

## Purpose
Describe development requirements for the Workday Reports as a Service connector. 
It standardizes ingestion of Workday custom reports exposed as REST endpoints that return CSV or XML.

## Scope
Consumes RaaS endpoints defined by customers. 
Supports configuration driven discovery where each RaaS URL is a stream. 
Incremental extraction depends on report parameters or design.

## Supported Versions
- Workday tenants exposing RaaS reports

## Authentication
- Workday web services authentication using integration user credentials or OAuth through gateway
- Secrets from platform secrets store

## Network and Deployment
Runners
- AWS Lambda for small to medium reports
- AWS Fargate for large reports

Network patterns
- NAT allowlist for Workday endpoints
- VPN where private routing is configured

## Discovery
Configuration defines the list of RaaS URLs and expected formats. 
Emit streams such as workday.raas.workers_csv mapped to each URL.

## Incremental Extraction
If the report supports date parameters pass the last cursor value as a parameter. 
Otherwise treat as full refresh and de duplicate at landing using stable keys.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::hcm::workday::cloud::raas
name: Workday RaaS Connector
taxonomy:
  origin: enterprise-connectors
  source: hcm
  provider: workday
  product: cloud
  method: raas
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist, vpn]
streams:
  strategy: discovery_by_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: config_declared_or_full_refresh
```

## Throttling and Retries
Throttle downloads and retry transient failures. 
For very large reports use chunked downloads and streaming parsers.

## Error Handling
Return clear messages with report name and URL. 
Classify permission errors versus data errors.

## Schema Handling
Infer schemas from CSV or XML. 
Register in schema registry and detect drift when report changes.

## Observability
Metrics: files downloaded, rows emitted, bytes, errors. 
Logs: report name, URL hash, run id.

## Testing
Unit tests for parameter injection and parsing. 
Integration tests with sample RaaS reports.

## Limits and Considerations
- RaaS is tenant specific and may change without notice
- Reports may not include modified dates for incremental loads
- CSV headers can vary across edits

## Relationships
Uses state registry for cursors and schema registry for inferred schemas.

## Exclusions
No GDP mappings or onboarding flows.
