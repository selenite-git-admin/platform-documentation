# Platform Catalog

## Role in the Platform
Platform Catalog centralizes platform reference data that other modules read during tenant creation, policy binding, activation, scheduling, and operations. It provides authoritative lists, policies, and calendars so that selections are consistent and validated at write time elsewhere.

## Responsibilities
- Store and version reference sets such as regions, residency policies, plans, limits, tag taxonomy, namespace rules, notification channels, and calendars
- Serve read APIs with cache friendly semantics and ETags
- Expose admin APIs for controlled updates with auditing
- Publish change events so dependents refresh caches
- Resolve effective calendars for a tenant by combining platform sets with tenant overlays

## Inputs
- Platform administrator updates to reference tables
- Calendar definitions and events maintained by platform operations

## Outputs
- Read APIs for reference data
- Change events for cache busting and downstream automation
- Effective calendars by tenant

## Interfaces
- Read APIs for all reference sets
- Admin write APIs guarded by roles
- Event publisher for reference updates

## Operational Behavior
- Read heavy service. Writes are rare and audited
- ETag based caching on read endpoints
- Event driven cache invalidation for consumers
- Calendar resolution performed on demand with simple set logic

## Constraints
- Does not manage identities or entitlements
- Does not own billing or subscription logic
- Does not call back into dependents
- Keeps history through effective dates and audit records

## Examples in Action

Tenant create
Tenant Management reads regions, residency policies, plans, limits, tag taxonomy, and namespace rules from Platform Catalog to validate selections before activation.

Calendar overlay
A tenant selects the APAC holiday set. Tenant specific overlays add a local holiday and suppress a platform maintenance freeze window. The Activation API resolves effective calendars through Platform Catalog.

## Module Documentation

[Data Model](data-model.md)
Entities, relationships, ERD placeholder, and DDL skeletons.

[UI](ui.md)
Screens, placement, API dependencies, and wireframe placeholders.

[API](api.md)
Operations, request and response schemas, idempotency, and errors.

[Observability](observability.md)
Metrics, logs, traces, dashboards, alerts, and SLOs.

[Runbook](runbook.md)
Operational procedures for incidents and routine tasks.

[Security](security.md)
Classification, access control, auditability, and safeguards.


Calendars
Moved to Calendar Service. See [Calendar Service](../../utilities/calendar-service/index.md)
