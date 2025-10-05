# Calendar Service

## Role in the Platform
Calendar Service provides authoritative time semantics for the platform. It resolves platform calendars, tenant overlays, fiscal periods, and working time functions that other modules call during scheduling, SLAs, KPI windows, exports, and maintenance freezes.

## Responsibilities
- Store calendar definitions, events, and reusable calendar sets
- Apply tenant overlays to add or suppress events
- Maintain fiscal calendars and period mappings
- Resolve effective calendars for a tenant and date range
- Provide working time utilities such as next business day, add business days, and business minutes between timestamps
- Serve read APIs with ETags and range parameters. Admin writes are audited

## Inputs
- Platform administrator writes for definitions, events, sets, and fiscal calendars
- Tenant overlay updates from Platform Admin App

## Outputs
- Resolved calendar events by tenant and date range
- Working time calculations
- Change events for cache busting

## Interfaces
- Read APIs for definitions, sets, fiscal calendars, and working time
- Admin write APIs for definitions, events, sets, overlays, and fiscal calendars

## Operational Behavior
- Read heavy service. Range queries are optimized and cache friendly
- Overlay resolution is deterministic. Effective calendar = union(platform sets) minus suppressed events plus overlay events
- Working time functions operate on the effective calendar and honor time zones

## Constraints
- Does not manage identities or entitlements
- Does not own tenant lifecycle. Overlays reference tenant_id only
- Does not schedule jobs. Scheduler consumes results

## Examples in Action

Resolve tenant business days
An orchestration flow resolves business days for next week using the tenant’s selected calendar set and overlay.

Add business days
An Activation API computes a promised delivery date by adding three business days to a timestamp using the tenant’s effective calendar.

## Module Documentation

[Data Model](data-model.md)
Entities, relationships, ERD placeholder, DBML, and DDL skeletons.

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
