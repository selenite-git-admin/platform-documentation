# Workflow Observability and Receipts

> Goal: Provide clear visibility into workflow activity and outcomes.  
> Scope: Covers dashboards, alerts, receipts, and export for evidence.

## Context
Stakeholders need visibility into workflow health and outcomes. Observability and receipts provide real time transparency and support audits.

## Actors (Personas and Roles)
- Observability Engineer: builds dashboards and alerts  
- Platform Admin: reviews execution health  
- Tenant Admin: downloads receipts  
- Auditor: reviews evidence

## Preconditions
- Execution engine emitting metrics and events  
- Evidence store available  
- Dashboards configured

## Scenario Flow
1. Observability Engineer publishes workflow dashboards and alerts  
2. Platform Admin reviews execution health regularly  
3. Tenant Admin downloads execution receipts for internal use  
4. Auditor reviews evidence on request

## Acceptance Criteria
- Dashboards and alerts available  
- Receipts accessible and exportable  
- Evidence repository up to date

## Failure Paths
- Metrics gap: missing signals, detection disabled  
- Receipt generation failure: export blocked  
- Dashboard outage: alert raised

## Observability and Governance
- Audit Events: workflow.metrics.enabled, workflow.receipt.available, workflow.receipt.exported  
- Metrics: workflow_success_rate, alert_volume, receipt_download_count  
- Evidence: dashboards snapshots and receipts

## Interfaces and Cross Links
- Previous: [Simulation and Rollback](08e-simulation-rollback.md)

## Configuration Examples

**Receipt Index (JSON)**
```json
{
  "workflow_id": "WF-DELAY-VENDOR-PAYMENTS-ACME",
  "receipts": ["WF-2025-09-29-001", "WF-2025-09-29-002"],
  "exportable": true
}
```

## BDD Scenarios

### Scenario: Receipt available after execution
```gherkin
Given a workflow has executed
When a user requests the receipt
Then the receipt is available for download
And an audit event is recorded
```

## Review Checklist
- [x] Dashboards configured  
- [x] Alerts active  
- [x] Receipts exportable  
- [x] Evidence current  
