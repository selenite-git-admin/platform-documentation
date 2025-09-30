# Triggers and Approvals

> Goal: Define when workflows should start and what approvals are required.  
> Scope: Covers trigger conditions, routing, and approval logic.

## Context
Workflows must start for the right reasons and involve the right decision makers. Trigger and approval configuration ensures controlled execution without bottlenecks.

## Actors (Personas and Roles)
- Workflow Author: defines triggers and approval logic  
- Tenant Admin: selects activation channels and thresholds  
- Business Owner: reviews and confirms trigger design  
- Compliance Officer: validates approval rules

## Preconditions
- Workflow configured for tenant  
- KPI and event sources available  
- Approval rules catalog present

## Scenario Flow
1. Workflow Author defines trigger conditions such as KPI breaches or anomaly flags  
2. Tenant Admin selects channels such as manual, scheduled, or event driven  
3. Approval routing configured including parallel or step-up approvals  
4. Compliance Officer validates rules

## Acceptance Criteria
- Triggers saved and testable  
- Approval logic consistent with policy  
- Evidence of configuration recorded

## Failure Paths
- Unreachable approver: routing fallback used  
- Trigger noise: thresholds tuned or suppression applied  
- Policy conflict: configuration blocked

## Observability and Governance
- Audit Events: workflow.trigger.configured, workflow.approval.configured  
- Metrics: trigger_fire_rate, approval_latency  
- Evidence: config receipts and test runs

## Interfaces and Cross Links
- Previous: [Workflow Authoring and Configuration](08b-workflow-authoring-configuration.md)  
- Next: [Workflow Execution Engine](08d-workflow-execution-engine.md)

## Configuration Examples

**Trigger Config (YAML)**
```yaml
workflow_id: WF-DELAY-VENDOR-PAYMENTS-ACME
triggers:
  - type: kpi_breach
    kpi: DSO
    threshold: 45
approvals:
  - type: policy
    rule: within_budget_limits
status: active
```

## BDD Scenarios

### Scenario: Trigger fires and approval passes
```gherkin
Given a trigger is configured on DSO breach
When the threshold is crossed
Then the workflow request is created
And policy checks pass
And the workflow proceeds
```

## Review Checklist
- [x] Triggers configured  
- [x] Approvals validated  
- [x] Evidence recorded  
