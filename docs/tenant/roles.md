# Tenant App – Roles and Permissions

## Role Model
Roles are grouped into two categories: **Decision Roles** and **Enablement Roles**.  
Decision roles consume information and take actions. Enablement roles configure and support the app to make those actions possible.

## Decision Roles
- **Executives (CXOs, BU Heads)**
  - Review KPIs and curated reports.
  - Approve requests such as exports or activations.
  - Trigger workflows and delegate actions to teams.

- **Business Team Members**
  - Prepare and analyze reports.
  - Submit requests for approvals.
  - Support executives with operational insights.

## Enablement Roles
- **Admins**
  - Configure data sources, users, and role assignments.
  - Manage infrastructure bindings.

- **Stewards**
  - Define and validate data contracts.
  - Oversee schema compliance and contract drift.

- **Operators**
  - Monitor health dashboards.
  - Handle retries and incident triage.

- **Developers**
  - Work with APIs, tokens, and webhooks.
  - Build integrations with tenant systems.

## Permissions
- Permissions are scoped with tenant-specific prefixes (e.g., `tenant.exec.*`, `tenant.admin.*`).
- Fine-grained actions map to individual pages and API scopes.
- Default role bundles can be customized per tenant.

## Principles
- Least privilege is enforced by default.
- Role assignments are auditable and logged.
- Break-glass accounts are allowed only under exceptional cases and require review.
