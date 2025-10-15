# Action Domain

## Role in the Platform
The Action domain converts KPI and state changes into outcomes. It catalogs reusable action templates, evaluates rules against events, and delivers actions reliably to external systems (email, chat, ITSM, webhooks).

## Submodules
- [Action Catalog](action-catalog/index.md) — versioned library of templates and parameters.  
- [Action Engine](action-engine/index.md) — rule evaluation and job creation.  
- [Action Delivery](action-delivery/index.md) — reliable dispatch with retries, backoff, and DLQ.

## Position in the Platform
Consumes KPI and event streams from Runtime and Storage modules. Emits deliveries, evidence, and telemetry. Integrates with Access for auth and with Trust for signatures and evidence.

## Interfaces
- Tenant‑facing APIs to browse templates, configure rules, and inspect outcomes.  
- Admin APIs to publish templates and manage throttling.  
- Delivery adapters for email, Slack, ITSM, and generic webhooks.

## Constraints
- Does not compute KPIs.  
- Does not own identity; enforces tenant scopes and quotas.
