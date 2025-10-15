# DYNAMICS 365 SALES WEB API CONNECTOR

## Purpose
Connector for Dynamics 365 Sales via Dataverse Web API (OData v4).

## Scope
- Entities: account, contact, lead, opportunity, systemuser, activitypointer, task, email
- Read-only extraction

## Supported Versions
- Dynamics 365 Sales on Dataverse

## Authentication
- Azure AD OAuth2 client credentials (application user)
- Secrets in platform secrets manager

## Network and Deployment
Runners: Lambda, Fargate
Network: VPN or Azure Private Link for private endpoints

## Discovery
Use Web API $metadata to enumerate tables including custom (prefix-based).

## Incremental Extraction
Use modifiedon (UTC) as default cursor where present. For activities use activitypointer.modifiedon.
Apply safety window to handle server-side equality semantics.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::crm::microsoft::dynamics_sales::webapi
name: Dynamics 365 Sales Web API Connector
taxonomy:
  origin: enterprise-connectors
  source: crm
  provider: microsoft
  product: dynamics_sales
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
Honor API limits; retry 429/5xx with jitter. Prefer $select to reduce payloads.

## Error Handling
Report table logical name and correlation id. Mask tokens.

## Schema Handling
Build schemas from metadata; include option set text where available. Register and track drift.

## Observability
Metrics: requests, tables, rows, retries. Logs: org url, table, query hash.

## Testing
Unit: OData paging, delta windowing. Integration: trial tenant.

## Limits and Considerations
Delta query not available for all tables. Some relationships require expand limits.

## Relationships
Feeds sales pipeline KPIs. Uses state and schema registries.
