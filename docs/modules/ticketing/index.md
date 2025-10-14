# Ticketing

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Ticketing is a **platform‑scoped** service for capturing, triaging, routing, and resolving incidents and requests across all tenants. It centralizes machine‑generated events (health degradation, pipeline failures, data freshness violations, cost anomalies) and human requests (schema changes, new connectors, access and quota changes) into one auditable workflow that integrates with Evidence Ledger, Notifications, RBAC, DRR, Runtime, and Delivery.

## Scope
Included
- Ticket creation from API, UI, and event streams
- Classification, deduplication, policy‑based routing
- State model and SLA tracking
- Assignment, escalation, and bulk operations
- Comments, attachments, links to platform resources
- Inbound email/webhook bridges and outbound webhooks
- Full audit with exportability

Excluded
- General project/portfolio management
- Arbitrary user‑defined workflows outside the supported state machine

## Design principles
- **Single system of record** for platform and tenant work
- **Automation first** with human assist
- **RBAC‑enforced visibility** rather than per‑tenant infrastructure
- **Idempotent writes** with stable keys
- **Typed payloads** with compact, safe fields

## Platform vs tenant visibility
- Tickets are stored in a shared platform database.  
- Tenant users can create and read **only** tickets with `tenant_id` matching their scope.  
- Platform operators can access **all** tickets, including platform‑only incidents where `tenant_id` is null.  
- Optional `visibility` flag on tickets and comments: `platform_only`, `tenant`, `mixed`.

## Ticket categories
System
- Health, pipeline/job failure, data freshness violation (from DRR), security findings, cost anomalies

Service requests
- Schema changes, new connectors, quotas, access, configuration, deletion/export

## Lifecycle
States
- new, ack, in_progress, wait_requester, wait_dependency, resolved, closed, canceled

Transitions are policy‑gated. Reopen allowed from closed to in_progress with audit.

## Integration map
- Health opens incidents on readiness failures and late data
- DRR opens tickets for late datasets and schema drift
- Runtime opens for stuck jobs and queue backlogs
- Notifications informs owners and requesters
- Evidence Ledger stores immutable state change anchors
- RBAC limits tenant visibility to their own scope
- Subscription Management opens for credit exhaustion or cost anomalies

## Summary
A platform‑scoped Ticketing service keeps operations sane, enables cross‑tenant correlation, and preserves strong tenant privacy through RBAC and query scoping rather than per‑tenant silos.