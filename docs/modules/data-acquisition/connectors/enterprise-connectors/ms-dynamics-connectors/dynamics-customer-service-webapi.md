# DYNAMICS 365 CUSTOMER SERVICE WEB API CONNECTOR

## Purpose
Connector for Dynamics 365 Customer Service via Dataverse Web API.

## Scope
- Entities: incident (case), queue, queueitem, knowledgearticle, account, contact, activitypointer
- Read-only extraction

## Supported Versions
- Dynamics 365 Customer Service on Dataverse

## Authentication
- Azure AD OAuth2 client credentials
- Secrets in platform secrets manager

## Network and Deployment
Runners: Lambda, Fargate
Network: VPN or Azure Private Link for private endpoints

## Discovery
Web API metadata enumeration with filtering by solution prefix when configured.

## Incremental Extraction
Use modifiedon; for knowledge articles use modifiedon or publishdate depending on use case.

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::crm::microsoft::dynamics_customer_service::webapi
name: Dynamics 365 Customer Service Web API Connector
taxonomy:
  origin: enterprise-connectors
  source: crm
  provider: microsoft
  product: dynamics_customer_service
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
Backoff on 429/5xx. Respect concurrency caps.

## Error Handling
Classify permission errors vs missing tables. Provide table logical name and request id.

## Schema Handling
Schemas from metadata; register and drift-check.

## Observability
Metrics: requests, tables, rows, retries.

## Testing
Unit: paging, cursor. Integration: demo environment.

## Limits and Considerations
Some KPIs require joining activity and case tables with lookups.

## Relationships
Feeds case SLA and CSAT analytics.
