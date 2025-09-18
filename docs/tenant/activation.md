# Tenant App – Activation Panels

## Purpose
Activation panels provide tenant users with the ability to initiate, approve, and monitor business workflows.  
They ensure that curated numbers translate into concrete actions in downstream systems.

## Capabilities
- **Activation Library**
  - Catalog of available flows: manual, scheduled, or event‑driven.
  - Each flow includes description, scope, and required approvals.

- **Pre‑Flight Checks**
  - Validate connectivity and scope before execution.
  - Estimate blast radius and provide dry‑run results where possible.

- **Execution**
  - Triggered by authorized users through the Tenant App.
  - Status updates streamed in real time to the UI.
  - Final outcome logged with correlation IDs.

- **Approvals**
  - Configurable approval gates for high‑impact actions.
  - Approval can be delegated with audit trail.
  - Evidence bundle attached to each run (logs, payloads, signatures).

- **Rollback and Recovery**
  - Runbook links provided for reversal steps.
  - Retention of execution logs for forensic review.

## Roles Involved
- **Executives**
  - Authorize and approve high‑impact activation runs.
  - Trigger workflows aligned to business decisions.
- **Business Team Members**
  - Prepare and initiate activation requests subject to approval.
- **Operators**
  - Monitor activation execution and manage retries.

## Notes
- All activation runs are immutable records in the audit log.  
- Dry‑run and approval steps are mandatory for high‑risk flows.  
- Evidence bundles are exportable for compliance review.  
