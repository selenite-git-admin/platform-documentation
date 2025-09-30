# Setting Up Guardrails and Data Quality Controls (DQC)

> Goal: Establish platform guardrails and data quality controls that prevent bad data and risky actions.  
> Scope: Covers policy definition, validation rules, threshold settings, and enforcement.

## Context
Guardrails and data quality controls reduce operational risk and ensure reliable KPI outcomes.  
This story introduces policies and validation rules that run across ingestion, transformation, KPI computation, and activation.  
The result is a predictable platform where errors are caught early and risky actions are blocked by policy.

## Actors (Personas and Roles)
- Security Admin: defines global guardrails and policy boundaries  
- Schema Steward: defines validation rules for raw, GDP, and KPI data  
- Platform Admin: enables guardrails across services  
- Compliance Officer: verifies policy coverage and retention rules  
- Observability Engineer: monitors control effectiveness

## Preconditions
- Platform infrastructure active  
- RBAC baseline in place  
- Policy framework and rule registry available

## Scenario Flow
1. Security Admin defines guardrails such as action quotas, data residency, and export limits  
2. Schema Steward registers validation rules for raw, GDP, and KPI layers  
3. Platform Admin enables guardrails and rules across ingestion, transformation, and activation services  
4. Thresholds and error handling behaviors configured such as block, quarantine, or alert  
5. Observability Engineer verifies dashboards and alerts for policy events

## Acceptance Criteria
- Guardrails enabled across all relevant services  
- Validation rules active and versioned  
- Thresholds documented and tested  
- Evidence available for audits

## Failure Paths
- Conflicting rules: policy application fails and error logged  
- Excessive blocking: business workflows stalled and review required  
- Missing rule coverage: gap identified and remediation ticket created

## Observability and Governance
- Audit Events: policy.defined, policy.enabled, rule.versioned, rule.applied  
- Metrics: rule_pass_rate, rule_block_rate, false_positive_rate  
- Evidence: policy registry export and validation logs

## Interfaces and Cross Links
- Previous: [Connector Handshake and Preflight](02b-connector-handshake-preflight.md)  
- Next: [Evidence](05-evidence-lineage.md)

## Configuration Examples

**Guardrail Policy (YAML)**
```yaml
policy_id: ACT-QUOTA-01
description: "Limit high-risk actions per tenant per day"
scope: tenant
quota_per_day: 5
enforcement: block
```

**Validation Rule (JSON)**
```json
{
  "rule_id": "GDP-INVOICE-AMT-NOT-NULL",
  "layer": "GDP",
  "field": "invoice_amount_net",
  "check": "not_null",
  "on_fail": "quarantine"
}
```

## BDD Scenarios

### Scenario: Guardrail blocks excessive actions
```gherkin
Given guardrail ACT-QUOTA-01 is enabled
When a tenant exceeds the daily action quota
Then the system blocks the action
And an audit event is recorded as policy.enforced
```

### Scenario: Validation rule quarantines bad data
```gherkin
Given rule GDP-INVOICE-AMT-NOT-NULL is active
When ingestion produces a record with null invoice_amount_net
Then the record is quarantined
And an alert is raised to the data team
```

## Review Checklist
- [x] Guardrails defined and enabled  
- [x] Validation rules registered and versioned  
- [x] Thresholds configured and tested  
- [x] Evidence available for audit  
