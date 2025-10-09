# Parked Scope

**Audience:** Engineering leadership, product owners, and platform architects  
**Status:** Working draft  
**Purpose:** Track items that are intentionally out of scope for the current Tenancy deliverable. This file documents regulatory mappings and deferred features that require future planning. It also clarifies items that are in scope to avoid ambiguity.

## Scope Classification

Items are classified as one of the following:
- Parked for future delivery
- Explicitly not covered
- In scope and tracked elsewhere

## In Scope Now

The following capabilities are active scope and documented in the main Tenancy set.
- Tenant App user roles and tenant level RBAC. Implemented in the Customer Portal. Enforcement is tied to Action and Identity policies. UI behavior is defined in tenancy-ui.md. API surfaces are defined in tenancy-apis.md.
- Tenancy policy enforcement for residency, encryption, retention, and actions. Defined in tenancy-policies.md.
- Observability, audit, and lifecycle orchestration. Defined in tenancy-observability.md and tenancy-tenant-life-cycle.md.

## Regulatory Mappings

Regulatory and certification mappings are parked to a future iteration. The platform already implements the underlying controls in the security and operations layers. The mappings below require evidence automation and narrative alignment but do not block current delivery.

**ISO 27001**
- Control family alignment for access control, cryptography, operations security, communications security, and supplier relationships.
- Evidence hooks from audit events and configuration snapshots.
- Policy documents and SoA updates needed in a separate compliance track.

**SOC 2**
- Trust Services Criteria coverage for security, availability, and confidentiality.
- Evidence collection pipeline for metrics, alerts, and incident postmortems.
- Change management and access review reports generated from existing logs.

**GDPR**
- Data subject request support and deletion attestations.
- Residency enforcement already provided by policy. Documentation and DSR workflow automation are required.
- Data processing addendum references will be handled by Legal.

**HIPAA**
- Encryption in transit and at rest already enforced. Formal BAAs and evidence controls are out of scope for this iteration.
- Additional logging and alerting rules will be addressed in the compliance track.

## Deferred Features

These features are parked for future releases. They are not required for current delivery.

- Fine grained audit query builder in the UI for complex filters and saved searches.
- Plan auto downgrade logic based on usage thresholds with customer notifications.
- Advanced webhook signing with dual key rotation and overlapping validity windows.
- Event payload schema registry with version negotiation and producer side validation.
- Quota visualization with predictive alerts in Customer Portal.
- Automated sandbox cloning blueprints with data masking profiles.
- Policy authoring UI for platform admins with dry run and shadow evaluation.
- Region migration scheduling UI with guardrails and conflict detection.
- On call drill automation for tenancy workflows with synthetic tenants.

## Explicitly Not Covered

The following item is intentionally not covered by the current Tenancy documents and implementation scope.

- Hybrid on premises deployment option. The current release targets cloud native multi tenant and single tenant profiles. A hybrid on premises model requires a separate architecture for control plane distribution, secret custody, offline policy evaluation, AirGap compatible webhooks, and tenant local observability stores. This will be addressed in a dedicated design.

## Dependencies For Parked Items

- Evidence automation service for compliance mappings.
- Schema registry or typed event contracts for webhook payloads.
- Secure key management process for advanced signing and rotation.
- Job scheduler primitives for migration and drill automation.

## Review And Change Management

- Parked scope is reviewed at the end of each release cycle.
- Items are promoted to active scope only with engineering capacity and product approval.
- Each promotion requires an RFC with architecture, test plan, and rollout strategy.

## Summary

The parked scope isolates work that is not required for the current Tenancy release. Regulatory mappings are deferred without blocking delivery because the technical controls already exist in the platform. The Hybrid on premises deployment option is out of scope and will be designed separately. Tenant level RBAC in the Tenant App is in scope and documented in the core Tenancy files.