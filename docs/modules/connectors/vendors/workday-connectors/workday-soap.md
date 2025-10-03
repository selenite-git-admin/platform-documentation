# WORKDAY SOAP CONNECTOR

## Purpose
Describe development requirements for the Workday SOAP connector based on Workday Web Services. 
It standardizes WSDL parsing, authentication, search filters, batching, and idempotent landing.

## Scope
Reads data from Workday WWS across domains such as Human Resources, Payroll, and Finance. 
Supports discovery from WSDL, incremental extraction using date filters, and paging over large datasets. 
Includes retries, error handling, observability, and certification.

## Supported Versions
- Workday WWS services with accessible WSDLs for the tenant

## Authentication
- Username and password with integration system user
- OAuth 2.0 or SAML assertions where configured through gateways
- Secrets retrieved from the platform secrets store

## Network and Deployment
Runners
- AWS Fargate for stable long running requests
- EC2 for special requirements

Network patterns
- NAT allowlist for Workday SOAP endpoints
- VPN for private routing where available

## Discovery
Parse WSDL to enumerate services, ports, operations, and types. 
Emit streams mapped to list and get operations with search capabilities.

## Incremental Extraction
Use search filters such as Transaction_Log_Effective_Date or Last_Updated_Timestamp where available. 
Batch through paginated responses using Workday response tokens.

Example request pattern
```xml
<wd:Get_Workers_Request>
  <wd:Request_Criteria>
    <wd:Transaction_Log_Effective_Date>2025-01-01T00:00:00Z</wd:Transaction_Log_Effective_Date>
  </wd:Request_Criteria>
  <wd:Response_Filter>
    <wd:Page>1</wd:Page>
    <wd:Count>500</wd:Count>
  </wd:Response_Filter>
</wd:Get_Workers_Request>
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::hcm::workday::cloud::soap
name: Workday SOAP Connector
taxonomy:
  origin: enterprise
  source: hcm
  provider: workday
  product: cloud
  method: soap
runtime:
  supported_runners: [fargate, ec2]
  network_patterns: [nat_allowlist, vpn]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Workday enforces throughput limits. 
Retry transient SOAP faults and 5xx with backoff. 
Throttle long running list operations proactively.

## Error Handling
Surface SOAP fault codes and operation names. 
Differentiate terminal validation faults from retryable transport errors.

## Schema Handling
Generate schemas from XSD and example payloads. 
Register schemas in schema registry and track compatibility.

## Observability
Metrics: calls, items, latency, faults, retries. 
Logs: service, operation, request id, run id.

## Testing
Unit tests for WSDL parsing and request construction. 
Integration tests with a sandbox tenant. 
Certification in Fargate and EC2.

## Limits and Considerations
- Some services require specific security roles that limit fields
- Search filters vary by service and version
- Response sizes can be large for historical data

## Relationships
Uses state registry for cursors and schema registry for payload schemas.

## Exclusions
No GDP mappings or onboarding flows.
