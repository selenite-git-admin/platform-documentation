# MICROSOFT DATAVERSE WEB API CONNECTOR

## Purpose
Generic connector for Dataverse tables irrespective of the specific Dynamics app. Serves as a shared method layer for Sales, Customer Service, Marketing, and Field Service.

## Scope
- Enumerate and extract any table permitted to the application user
- Reusable pagination, filtering, and modifiedon cursor logic

## Supported Versions
- Dataverse Web API

## Authentication
- Azure AD OAuth2 client credentials

## Network and Deployment
Runners: Lambda, Fargate

## Discovery
Web API $metadata to list tables and attributes. Allow include/exclude lists per solution prefix.

## Incremental Extraction
Default to modifiedon with safety window. Allow override per table.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::platform::microsoft::dataverse::webapi
name: Dataverse Web API Connector
taxonomy:
  origin: enterprise
  source: platform
  provider: microsoft
  product: dataverse
  method: webapi
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [vpn, azure_privatelink, nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared
    cursor_strategy: modified_timestamp
```

## Throttling, Error Handling, Schema, Observability, Testing
Reuse the same patterns as specific app connectors.
