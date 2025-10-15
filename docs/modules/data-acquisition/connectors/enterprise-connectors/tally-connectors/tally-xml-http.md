# TALLY XML HTTP

## Purpose
Describe development requirements for the Tally XML over HTTP connector.

## Scope
Reads data from Tally ERP systems via the XML over HTTP interface. 
Supports incremental extraction when modification date fields are exposed. 
Covers authentication, network, retries, error handling, and observability.

## Supported Versions
- Tally.ERP 9 and TallyPrime with ODBC/XML interface enabled

## Authentication
- Basic authentication with username and password configured in Tally server
- Secrets retrieved from platform secrets store

## Network and Deployment
Supported runners
- AWS Lambda for small extracts
- AWS Fargate for larger extracts

Network patterns
- VPN or site-to-site to reach on-prem Tally servers
- NAT allowlist only if Tally is exposed securely

## Discovery
Discovery is configuration driven. 
Connector manifest must specify XML request templates for master and transaction objects.

## Incremental Extraction
Use `ALTERID` or `LASTMODIFIEDDATE` fields if available. 
Pass cursor from orchestrator and filter results.

Example XML request
```xml
<ENVELOPE>
  <HEADER>
    <TALLYREQUEST>Export Data</TALLYREQUEST>
  </HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVFROMDATE>20250101</SVFROMDATE>
          <SVTODATE>20250131</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::tally::onprem::xml_http
name: Tally XML over HTTP Connector
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: tally
  product: erp9
  method: xml_http
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [vpn, nat_allowlist]
streams:
  strategy: config_defined
  defaults:
    key_strategy: config_declared
    cursor_strategy: config_declared_or_full_refresh
```

## Throttling and Retries
Tally servers can handle only limited concurrent sessions. 
Throttle requests to avoid timeouts. 
Retry transient failures with backoff.

## Error Handling
- Retryable: transient network failures
- Terminal: invalid request XML, authentication failure

## Schema Handling
Schemas defined in configuration based on expected XML structure. 
Emit schemas to schema registry. 
Raise drift alerts when XML fields change.

## Observability
Log report name, request parameters, and response size. 
Metrics for rows read, rows emitted, errors, retries.

## Testing
Unit tests for XML template construction and cursor logic. 
Integration tests with sample Tally instances.

## Limits and Considerations
- Performance depends on Tally server configuration
- XML responses can be large, chunking may be required
- Tally customization may change available fields

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding flows.
