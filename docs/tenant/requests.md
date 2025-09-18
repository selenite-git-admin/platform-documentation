# Tenant App – Requests and Approvals

## Purpose
Requests and approvals provide a structured workflow for tenant users to submit, track, and authorize actions.  
They ensure governance, compliance, and accountability for sensitive operations.

## Capabilities
- **Request Types**
  - New data source onboarding.
  - Schema or contract changes.
  - Role or scope escalations.
  - Data exports and egress approvals.
  - Activation flow execution where gated.

- **Workflow**
  1. Submit request with description and required details.
  2. System assigns SLA clock and priority.
  3. Request is routed to approvers or delegated roles.
  4. Approvers review, comment, and approve or reject.
  5. Actions are logged with correlation IDs.

- **Tracking**
  - Status: open, pending approval, approved, rejected, closed.
  - Priority levels and due dates tracked against SLA targets.
  - Watchers can subscribe to updates.

- **Audit Trail**
  - All requests and approvals are logged.
  - Comments and decisions are immutable records.
  - Exportable evidence for compliance.

## Roles Involved
- **Executives**
  - Approve or reject high‑impact requests (exports, activations).
- **Business Team Members**
  - Submit requests for operational needs.
- **Admins**
  - Submit and review administrative requests.
- **Stewards**
  - Approve schema and contract related requests.

## Notes
- Notifications sent on status change to requestor and watchers.  
- Approvals can be delegated to backup approvers with documented justification.  
- All SLA breaches are flagged in health dashboards.  
