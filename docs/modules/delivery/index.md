# Data Consumption Domain

## Role in the Platform
The Data Consumption domain is the final stage of the platform: it exposes validated & published data to tenants via APIs, dashboards, catalog, exports, and webhooks. Materialization stays in Storage; Consumption governs access & delivery.

## Submodules
- Activation APIs — query layer for KPIs and published datasets.  
- Catalog — consumer-facing discovery of resources.  
- Exports — delivery jobs to external destinations.  
- Webhooks — push notifications and event delivery.  
- Dashboards — curated, read-only visualization.

## Interfaces
- REST/GraphQL for queries, catalog browsing, export & webhook management, server-rendered dashboards.

## Constraints
- No materialization or schema authoring; read-only over Storage outputs.  
- Contract-stable responses; additive versioning only.
