# DYNAMICS 365 MARKETING REST CONNECTOR

## Purpose
Connector for Dynamics 365 Marketing data via REST endpoints and Dataverse entities used by Marketing.

## Scope
- Entities: contacts, marketing lists, journeys, emails, interactions
- REST-specific endpoints for insights where applicable

## Supported Versions
- Dynamics 365 Marketing on Dataverse

## Authentication
- Azure AD OAuth2
- Secrets in platform secrets manager

## Network and Deployment
Runners: Lambda, Fargate

## Discovery
Enumerate Dataverse tables and configured Marketing insight endpoints.

## Incremental Extraction
Use modifiedon for entities and date parameters for insights endpoints.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise::marketing::microsoft::dynamics_marketing::rest
name: Dynamics 365 Marketing REST Connector
taxonomy:
  origin: enterprise
  source: marketing
  provider: microsoft
  product: dynamics_marketing
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [vpn, azure_privatelink, nat_allowlist]
streams:
  strategy: discovery_or_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: modified_timestamp_or_date_range
```

## Throttling and Retries
Handle 429/5xx with backoff. Limit page size on insights.

## Error Handling
Return entity or endpoint name and parameters. Mask secrets.

## Schema Handling
Infer from metadata and endpoint docs. Register schemas and drift alerts.

## Observability
Metrics: requests, entities, insights rows, retries.

## Testing
Unit: windowing, insights pagination. Integration: sandbox.

## Limits and Considerations
Some insight endpoints are eventually consistent; use sliding windows.

## Relationships
Feeds marketing funnel KPIs with Ads and GA connectors.
