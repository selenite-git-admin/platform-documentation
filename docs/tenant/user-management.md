# Tenant App – User Management

## Purpose
User management provides tenant administrators with controls to add, update, and remove user accounts.  
It enforces role assignments, integrates with identity providers, and supports compliance through audit logging.

## Capabilities
- **Provisioning**
  - Integrates with IdPs using OIDC, SAML, or SCIM.
  - Supports Just‑in‑Time (JIT) user creation during SSO login.
  - Local account creation available only if explicitly enabled.

- **Role Assignment**
  - Assign decision or enablement roles to users.
  - Supports default role bundles per tenant.
  - Provides page‑level access preview before assignment.

- **Authentication and Sessions**
  - All sessions tied to IdP authentication.
  - Session and device lists visible to administrators.
  - Ability to revoke sessions on demand.

- **Multi‑Factor Enforcement**
  - Delegated to the IdP where supported.
  - Enforcement policies checked at login.

- **Deprovisioning**
  - Automated through SCIM when available.
  - Manual disablement via Tenant App for break‑glass.
  - All active sessions and tokens revoked immediately.

## Roles Involved
- **Admins**
  - Manage user lifecycle and assign roles.
- **Stewards**
  - Review access for compliance if required.
- **Executives**
  - Visible as assigned decision‑makers but not provisioned directly.

## Notes
- All user lifecycle actions are logged and auditable.
- Break‑glass local accounts are excluded from automated provisioning flows and require post‑use review.
