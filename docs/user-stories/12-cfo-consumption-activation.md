# CFO Consumption and Activation

> Goal: Enable CFOs to act on governed KPIs with evidence and system guardrails.  
> Scope: Covers KPI monitoring, action triggers, and compliance proof.

## Context
CFOs need near real time visibility into financial health and the ability to take corrective action when thresholds are breached. Actions must remain governed and provide evidence for compliance and audit.

## Actors (Personas and Roles)
- CFO: consumes KPIs and takes corrective action
- Platform Admin: ensures KPI visibility and governance
- Compliance Officer: verifies compliance proof and evidence

## Preconditions
- KPI publishing complete
- CFO dashboard configured
- Governance policies enforced

## Scenario Flow
1. CFO views KPIs and notes threshold breach (e.g., DSO > 45 days)
2. CFO triggers action such as delaying vendor payments
3. System validates action against governance policies
4. Evidence recorded with timestamp and CFO identity
5. Compliance Officer reviews evidence

## Acceptance Criteria
- CFO actions executed with policy checks
- Evidence linked to action and KPI
- Compliance verification available

## Failure Paths
- Action blocked by policy violation
- Evidence recording failure: alert raised
- KPI misconfigured: dashboard corrected

## Observability and Governance
- Audit Events: cfo.action.initiated, cfo.action.executed, cfo.action.evidence.recorded
- Metrics: cfo_action_count, evidence_record_success_rate
- Evidence: action receipts with identity and timestamp

## Interfaces and Cross Links
- Previous: [KPI Consumption](07-kpi-consumption.md)
- Next: [Ops Connector Failure and Recovery](13-ops-connector-failure-recovery.md)

## Configuration Examples

**Action Receipt (JSON)**
```json
{
  "action_id": "ACT-2025-09-29-001",
  "initiated_by": "cfo@tenant.com",
  "kpi": "DSO",
  "outcome": "delay_vendor_payments",
  "status": "EXECUTED",
  "timestamp": "2025-09-29T12:00:00Z"
}
```

## BDD Scenarios

### Scenario: CFO action executed with evidence
```gherkin
Given KPI publishing is complete
When the CFO initiates an action on threshold breach
Then the action is executed with policy checks
And evidence is recorded
```

### Scenario: CFO action blocked due to policy
```gherkin
Given KPI publishing is complete
When the CFO initiates an action violating policy
Then the action is blocked
And an alert is raised
```

## Review Checklist
- [x] CFO action enabled
- [x] Policy checks enforced
- [x] Evidence recorded
