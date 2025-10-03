# Tenant Management

## Role in the platform
Tenant Management is the control point for onboarding, lifecycle, and configuration of tenants. It records tenant identity and infrastructure choices that other modules read to apply policy and route workloads.

## Responsibilities
- Create and manage tenant records and lifecycle states
- Record region and residency selections
- Bind product plan code for Subscription Enforcement to apply features and limits
- Maintain contact roles for operations and incidents
- Maintain external identifiers that map to billing or CRM
- Expose read APIs for profile lookup and search
- Emit change events for downstream caches

## Non goals
- Calendars and working time semantics are owned by Calendar Service
- Identities and access tokens are owned by Access Modules
- Business data is out of scope

## Inputs
- Admin actions from Platform Admin App
- Infra masters from Platform Catalog

## Outputs
- Tenant profile for lookups by other modules
- Change events for caches and routing layers

## Module documentation

[Data Model](data-model.md)
Entities, relationships, ERD placeholder, DBML, and DDL skeletons.

[UI](ui.md)
Screens for onboarding, lifecycle, and metadata edits.

[API](api.md)
Operations for tenant profile reads and lifecycle updates.

[Observability](observability.md)
Metrics, logs, and SLOs for control operations.

[Runbook](runbook.md)
Procedures for routine operations and incidents.

[Security](security.md)
Classification, access control, and audit.
