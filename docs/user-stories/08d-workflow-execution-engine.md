# Workflow Execution Engine

> Goal: Execute workflows reliably with guardrails and idempotency.  
> Scope: Covers execution, retries, rollback hooks, and receipts.

## Context
Workflow execution must be reliable. The engine handles steps, retries, idempotency, and rollback so that business actions are safe and auditable.

## Actors (Personas and Roles)
- Workflow Engine: executes steps and manages retries  
- Platform Admin: observes execution and handles escalations  
- Tenant Admin: views execution receipts  
- Observability Engineer: monitors performance

## Preconditions
- Triggers and approvals configured  
- Target systems reachable  
- Idempotency keys available

## Scenario Flow
1. Execution starts and idempotency keys are set  
2. Steps are executed with retries on transient errors  
3. Rollback hooks available for reversible actions  
4. Receipt generated with step outcomes and timestamps

## Acceptance Criteria
- Steps execute successfully or fail safely  
- Retries and rollback behave as designed  
- Receipt available to stakeholders

## Failure Paths
- Irrecoverable error: execution halts and incident logged  
- Partial side effects: rollback invoked  
- Idempotency failure: duplicate prevented and logged

## Observability and Governance
- Audit Events: workflow.started, workflow.step.completed, workflow.receipt.generated  
- Metrics: workflow_success_rate, mean_time_to_complete  
- Evidence: execution receipts and logs

## Interfaces and Cross Links
- Previous: [Triggers and Approvals](08c-triggers-approvals.md)  
- Next: [Simulation and Rollback](08e-simulation-rollback.md)

## Configuration Examples

**Execution Receipt (JSON)**
```json
{
  "workflow_id": "WF-DELAY-VENDOR-PAYMENTS-ACME",
  "status": "EXECUTED",
  "steps": [
    {"name": "apply_vendor_hold", "status": "SUCCESS"},
    {"name": "notify_ap_team", "status": "SUCCESS"}
  ],
  "timestamp": "2025-09-29T13:00:00Z"
}
```

## BDD Scenarios

### Scenario: Successful execution with retries
```gherkin
Given a workflow execution begins
When a transient error occurs
Then the engine retries
And the workflow completes
And a receipt is generated
```

## Review Checklist
- [x] Idempotency keys used  
- [x] Retries configured  
- [x] Receipts generated  
