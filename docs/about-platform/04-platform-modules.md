# Platform Modules

## Purpose of this catalog
This page orients readers to the module families in the platform and points to the detailed module documentation. Each family groups modules with a shared responsibility. Keep Host lean and focused. Move shared utilities and governance out of Host.

## Host Modules
[Tenant Management](../modules/host/tenant-management/index.md)
Owns tenant identity, lifecycle, residency, and routing tags. Other modules read it; it does not call dependents.

[Platform Catalog](../modules/master/index.md)
Authoritative infra and service knobs such as regions, residency policies, environment codes, namespace prefixes, tag taxonomy, notification channels, and escalation policies.

## Governance Modules
[Policy Registry](../modules/policy-registry/index.md)
Central registry for guardrail policies that other modules reference at decision time.

Lineage Obligations (planned)
Location for lineage based governance rules.

## Data Utilities Modules
[Calendar Service](../modules/calendar-service/index.md)
Time semantics for the platform including calendars, tenant overlays, fiscal periods, working time utilities, and the Date Table used by BI.

[Data Contract Registry](../modules/utilities/data-contract-registry/index.md)
Catalog of dataset contracts and versions across layers: extraction, raw, gold, and consumption. Producers and consumers align on these contracts.

Schema Registry (planned)
Engine agnostic registry for schema evolution and compatibility checks.

Catalog and Discovery (planned)
Metadata and search to help teams find datasets and services.

Migration Service (planned)
Utilities to plan and execute controlled data or schema migrations.

## Access Modules (planned)
Authentication, Authorization, Subscription Enforcement. Subscription Enforcement applies product plan features and limits at runtime.

## Security Modules (planned)
Gateway, Network Security. Network boundaries and request filtering for inbound and outbound traffic.

## Compute Modules (planned)
Ingestion, Normalization, KPI Build, Publish, Orchestration. Transform and move data through the platform.

## Data Storage Modules (planned)
Raw Store, GDP Store, KPI Store, Published Store. Authoritative storage layers with clear contracts.

## Consumption Modules (planned)
Activation APIs, Exports, Webhooks, Catalog. Deliver data and events to downstream applications and tools.

## Action Modules (planned)
Action Engine, Action Catalog, Action Delivery. Define actions and deliver them to destinations.

## Runtime Modules (planned)
Scheduler, Messaging and Events, Observability, Error Handling, Metering. Operate the platform reliably.
