# Activation Plane — Flows

## Purpose
Flows describe **how actions are triggered** inside the Activation Plane.  
They ensure that decisions made from KPIs can be executed consistently, whether automatically or manually, with governance enforced at each step.

---

## Types of Flows

### 1. Event-Driven Flows
Triggered by conditions or thresholds defined on KPI outputs.
- **Examples**
  - AR overdue > 90 days → Create collections task in ERP.
  - OEE < 70% → Notify plant manager in Slack.
- **Governance**
  - Thresholds and conditions must be tenant-approved.
  - Notifications and downstream actions pass through policy checks.
- **Characteristics**
  - Near-real-time.
  - Auto-generated audit log with KPI reference.

---

### 2. Scheduled Flows
Triggered on fixed intervals or calendar events.
- **Examples**
  - Weekly compliance bundle exported to regulator portal.
  - Monthly board report PDF posted to SharePoint.
- **Governance**
  - Tenant Admin defines frequency, recipients, and destinations.
  - Data quality and freshness checks enforced before execution.
- **Characteristics**
  - Predictable timing.
  - Alignment with fiscal periods, regulatory deadlines, or business cycles.

---

### 3. Manual Flows
Triggered by tenant users directly from the Tenant App.
- **Examples**
  - User clicks “Escalate to Collections” on overdue KPI panel.
  - CFO requests one-time liquidity forecast run.
- **Governance**
  - RBAC and scope limits enforced on who can trigger manual actions.
  - Optional approval workflows (Maker–Checker) for sensitive actions.
- **Characteristics**
  - Immediate and on-demand.
  - Contextual — initiated from the KPI view.

---

## Flow Lifecycle
All flows, regardless of type, follow the same lifecycle:

1. **Trigger**  
   - Event condition met, schedule reached, or manual click.
2. **Policy Check**  
   - Validation of role, quotas, allow-lists, and data masking rules.
3. **Execution**  
   - Action performed via connector (notify, task, export, write-back).
4. **Audit & Observability**  
   - Logs captured with correlation ID, KPI reference, and timestamp.
5. **Retry & Recovery**  
   - If action fails, retry with exponential backoff.  
   - Failed attempts routed to DLQ; Tenant Admin can replay.

---

## Boundaries
- **Flows do not** design business processes end-to-end (those remain in ERP/CRM).  
- **Flows do** orchestrate the final step between a KPI insight and its governed activation.  

---

## Value
By supporting event-driven, scheduled, and manual activations under one framework, the Activation Plane:
- Guarantees consistent execution.
- Ensures all actions are governed and auditable.
- Bridges the last-mile gap from “knowing” to “doing.”
