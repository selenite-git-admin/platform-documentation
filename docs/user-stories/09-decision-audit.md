# Decision Making

> Goal: Capture business decisions with rationale, evidence, and traceability.  
> Scope: Covers decision initiation, data review, approval, action, and audit log creation.

## Context
Executives and managers make decisions based on KPIs, forecasts, and risk signals. These decisions need a consistent record that links rationale to data, approvals, and resulting actions so that outcomes can be reviewed and audited later.

## Actors (Personas and Roles)
- Business Owner: initiates or confirms decisions and triggers actions
- Analyst or Viewer: prepares data packs and scenario analysis
- Compliance Officer: reviews evidence sufficiency for regulated areas
- Platform Admin: ensures decision records are stored and accessible

## Preconditions
- Relevant KPIs and evidence available
- User has permissions to initiate decisions
- Action workflows exist for the decision outcomes

## Scenario Flow
1. Business Owner opens Decision Console and selects a KPI or case
2. Analyst attaches data pack: KPI snapshots, trends, scenario models
3. Business Owner records rationale and selects intended outcome
4. Optional approvals applied based on policy
5. Linked workflow is triggered if applicable
6. Decision record is saved with timestamps, identities, and evidence links

## Acceptance Criteria
- Decision record contains rationale, inputs, and selected outcome
- Evidence links resolve to immutable artifacts
- Optional approvals applied per policy
- Decision is traceable to actions taken

## Failure Paths
- Missing evidence: decision cannot be finalized
- Policy rule requires approval but is misconfigured: block and alert
- Storage failure: decision record write error and retry

## Observability and Governance
- Audit Events: decision.created, decision.finalized, decision.linked_action
- Metrics: decisions_per_period, decision_to_action_rate
- Evidence: decision pack with snapshots and links to lineage

## Interfaces and Cross Links
- Previous: [KPI Consumption](07-kpi-consumption.md)
- Next: [Evidence Export for Regulators](09b-evidence-export-regulators.md)

## Configuration Examples

**Decision Record (JSON)**
```json
{
  "decision_id": "DEC-2025-09-29-001",
  "initiated_by": "cfo@tenant.com",
  "rationale": "DSO trend exceeds threshold for 2 weeks",
  "inputs": ["kpi_dso_2025w39.png", "trend.csv"],
  "outcome": "delay_vendor_payments",
  "linked_workflow": "WF-DELAY-VENDOR-PAYMENTS-ACME",
  "status": "FINALIZED"
}
```

## BDD Scenarios

### Scenario: Decision finalized with linked action
```gherkin
Given KPIs and evidence are available
When a Business Owner records a decision with rationale
And selects an outcome with a linked workflow
Then the decision is finalized
And a decision.linked_action event is recorded
```

### Scenario: Decision blocked due to missing evidence
```gherkin
Given a decision is being recorded
When required evidence is missing
Then the decision cannot be finalized
And the user is prompted to attach the evidence
```

## Review Checklist
- [x] Rationale captured
- [x] Evidence linked
- [x] Policy checks applied
- [x] Action linkage recorded
