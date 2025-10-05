# Subscription Enforcement – User Interface

## Scope
Documents tenant and admin screens for plan visibility, quota usage, simulation, and overrides. 【123†source】

## Placement 【123†source】
- **Tenant App**: Plan & Usage, Feature Entitlements, Plan Simulator.  
- **Admin App**: Overrides and Diagnostics.

## Screens at a glance 【123†source】
| Screen | Purpose |
|--------|---------|
| [Usage Overview](#usage-overview) | Show current usage vs limits |
| [Feature Entitlements](#feature-entitlements) | List enabled features and constraints |
| [Plan Simulator](#plan-simulator) | Preview outcomes under another plan |
| [Overrides (Admin)](#overrides-admin) | Apply time‑boxed grace or overage |

## Screen details 【123†source】

### Usage Overview
- **Purpose**: Display quota progress per feature.  
- **Primary actions**: None.  
- **Roles and permissions**: Tenant role.  
- **State model**: Derived from `GET /plan` + metrics feed.  
- **API dependencies**: `/plan`.  
- **Navigation**: Dashboard → Plan & Usage.  
- **Notes**: Show per‑window bars and textual reason phrases.

### Feature Entitlements
- **Purpose**: List effective entitlements (plan + overrides).  
- **Primary actions**: None.  
- **Roles and permissions**: Tenant role.  
- **State model**: Merge plan features with active overrides.  
- **API dependencies**: `/plan`.  
- **Navigation**: Dashboard → Plan & Usage.

### Plan Simulator
- **Purpose**: Evaluate outcomes under a different edition.  
- **Primary actions**: Submit simulation form.  
- **Roles and permissions**: Tenant and Admin.  
- **State model**: Request → `POST /simulate` → render decision and `plan_diff`.  
- **API dependencies**: `/simulate`.  
- **Navigation**: Dashboard → Plan & Usage → Simulator.  
- **Notes**: Surface cost implications when available.

### Overrides (Admin)
- **Purpose**: Create and manage time‑boxed overrides.  
- **Primary actions**: Create override, activate, revoke.  
- **Roles and permissions**: Admin only.  
- **State model**: Draft → Active → Expired/Revoked.  
- **API dependencies**: Plan Registry admin APIs.  
- **Navigation**: Admin → Entitlements → Overrides.

## Accessibility and localization 【123†source】
- Full keyboard navigation with visible focus.  
- Labels and aria attributes for all inputs.  
- Dates and numbers localized to tenant locale/timezone.  
- Color contrast meets WCAG AA.

## Error, loading, and empty states 【123†source】
- Errors: show cause and recovery action (e.g., “over limit; try later or upgrade”).  
- Loading: skeletons for tables and charts.  
- Empty: “No features enabled for this edition.”

## Dependencies 【123†source】
- [Enforcement API](api.md)  
- Feature flag `plan-simulator-enabled`  
- Metering metrics subscription
