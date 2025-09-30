# Host App — Identity & RBAC

## Purpose
Explains how identity and role-based access control (RBAC) are enforced in the Host App.  
Identity and RBAC ensure that all actions are authenticated, authorized, and fully auditable.

## Identity
- Enterprise SSO via OIDC or SAML.  
- Scoped API tokens for automation.  
- Session management: renewals, expirations, and revocation.  

This model guarantees consistent identity management across UI and API.

## Roles
Governance-oriented roles:  
- **Org Admin** — manages roles, policies, residency.  
- **Data Steward** — authors contracts and reference data.  
- **Approver** — validates and approves publishes.  
- **Viewer** — read-only dashboards and contracts.  
- **Auditor** — queries and exports compliance evidence.  

Roles map directly to governance responsibilities.

## Permissions
- Draft, approve, and publish contracts.  
- Manage tenants and residency.  
- Configure calendars, FX, org hierarchies.  
- View health dashboards.  
- Export audit evidence.  

Permissions are enforced at the API layer, surfaced in UI.

## Design Tenets
- **Separation of Duties:** no role both drafts and approves.  
- **Least Privilege:** access rights are minimized.  
- **Immutable Evidence:** every action logged with identity and timestamp.  

## Why This Matters
Without strong identity and RBAC, governance collapses into trust-based processes.  
The Host App provides guardrails that are transparent, enforceable, and defensible during audits.
