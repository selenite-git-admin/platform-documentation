# Gateway – User Interface

## Scope
Screens for tenant and admin users.

## Screens at a Glance
| Screen | Purpose |
|---|---|
| Routes | Manage upstream mappings |
| WAF Policies | Attach rulesets |
| Certificates | Rotate TLS certs |

## Screen Details
### Routes
- Purpose: Manage upstream mappings
- Primary actions: Create, update
- Roles: Admin
- API: /routes

### WAF Policies
- Purpose: Attach rulesets
- Primary actions: Enable shadow/block
- Roles: Admin
- API: /waf/policies

### Certificates
- Purpose: Rotate TLS certs
- Primary actions: Rotate, rollback
- Roles: Admin
- API: /certs/rotate

## Accessibility and Localization
- WCAG AA; keyboard navigation; localized formats.
