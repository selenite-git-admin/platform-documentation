# Versioning and Lifecycle

## Purpose
Connectors are long-lived components that evolve as source systems change.  
Without a defined lifecycle, connectors risk becoming brittle, unpredictable, and difficult to upgrade.  
This section defines how connectors are versioned, supported, upgraded, and retired. It ensures that every connector follows the same standards for release and deprecation.

## Scope
This document applies to all connectors across vendors and methods.  
It defines semantic versioning, release channels, support windows, upgrade and rollback processes, and deprecation procedures.  
It also explains how lifecycle events are recorded in the registry and surfaced to tenants.

## Semantic Versioning
Every connector must follow semantic versioning (semver) with three parts: **major.minor.patch**.

- **Major**: breaking changes such as dropping a stream, changing authentication, or removing a field. Example: `2.0.0`  
- **Minor**: backward compatible features such as adding a new stream, supporting a new cursor, or improving performance. Example: `1.2.0`  
- **Patch**: bug fixes or small corrections that do not affect functionality. Example: `1.2.3`  

Examples:
- A SAP OData connector that adds support for a new entity uses a minor version bump.  
- A Salesforce REST connector that fixes retry logic for rate limits uses a patch bump.  
- A JDBC connector that changes how keys are handled requires a major version bump.

## Release Channels
Connectors are distributed through release channels to balance stability and agility.

- **Stable**: certified, production-ready versions. Default for all tenants.  
- **Preview**: early access for testing new features. Tenants may opt in.  
- **Deprecated**: versions that remain available for backward compatibility but are scheduled for removal.  

The manifest must declare the release channel, and the catalog must surface it clearly to administrators.

## Support Windows
Every connector version has a defined support window.

- Major versions are supported for at least 18 months after release.  
- Minor versions are supported until the next minor release on the same major line.  
- Patch versions are supported until replaced by a newer patch.  

After the support window expires, the connector moves to deprecated status.

## Upgrade and Rollback
The orchestrator manages upgrades and rollbacks of connector artifacts.

- **Upgrade**: Tenants are notified when a new version is available. They may choose to upgrade immediately or within a grace window.  
- **Rollback**: If a new version fails, tenants can revert to the previous stable version within the same major line.  

Examples:
- A Salesforce connector upgraded from `1.5.2` to `1.6.0` can be rolled back to `1.5.2` if required.  
- A SAP connector moving from `1.9.3` to `2.0.0` cannot roll back automatically, because it involves a breaking change. The upgrade must be planned and tested.

## Deprecation and Retirement
Deprecation is a controlled process to phase out old connectors.

- When a connector or method is scheduled for retirement, it must be marked as **deprecated** in the catalog.  
- Tenants receive at least 6 months’ notice before final retirement.  
- The catalog must display alternatives or migration paths.  

Examples:
- RFC connectors may be deprecated as SAP phases out legacy access in favor of OData.  
- A Salesforce Bulk API v1 connector may be deprecated when Bulk API v2 is stable.

## Registry Tracking
Lifecycle events must be recorded in the registry.  

- **connector_definitions** table tracks version, release channel, and status.  
- **compat_alerts** record when a tenant is running a deprecated or unsupported connector.  
- **upgrade_events** record who upgraded, rolled back, or deferred an upgrade.  

This ensures complete auditability.

## Principles
- Semantic versioning is mandatory for all connectors.  
- All changes must be categorized as major, minor, or patch.  
- Release channels must be explicit.  
- Deprecation must always include advance notice and a migration path.  
- Registry tracking is required for all lifecycle events.  

## Relationships
- The catalog surfaces lifecycle status to tenants.  
- Governance modules enforce retirement policies.  
- Runtime modules ensure rollbacks can be applied safely.  
- Security modules validate that old, insecure versions are removed on schedule.

## Exclusions
This document does not define tenant onboarding or credential migration during connector upgrades.  
It does not cover GDP or KPI model versioning. Its scope is strictly the lifecycle of connector artifacts.
