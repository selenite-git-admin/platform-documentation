# DYNAMICS 365 FIELD SERVICE WEB API CONNECTOR

## Purpose
Connector for Dynamics 365 Field Service via Dataverse Web API.

## Scope
- Entities: workorder, booking, resource, incidenttype, account, asset
- Read-only extraction

## Supported Versions
- Dynamics 365 Field Service on Dataverse

## Authentication
- Azure AD OAuth2 client credentials
- Secrets in platform secrets manager

## Network and Deployment
Runners: Lambda, Fargate

## Discovery
Enumerate Field Service solution tables via metadata.

## Incremental Extraction
Use modifiedon or status change timestamps depending on entity.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::service::microsoft::dynamics_field_service::webapi
name: Dynamics 365 Field Service Web API Connector
taxonomy:
  origin: enterprise
  source: service
  provider: microsoft
  product: dynamics_field_service
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

## Throttling and Retries
Backoff on 429/5xx.

## Error Handling
Surface table name and correlation id.

## Schema Handling
Schemas from metadata; register and drift-check.

## Observability
Metrics: requests, rows, retries.

## Testing
Unit: cursor logic. Integration: trial env.

## Limits and Considerations
Route planning and IoT data may be in external systems; document scope explicitly.

## Relationships
Feeds service KPIs like completion time and first time fix.
