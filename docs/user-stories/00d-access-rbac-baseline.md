# Access and RBAC Baseline

> Goal: Establish role-based access control baseline for the platform.  
> Scope: Covers creating roles, assigning permissions, and validating segregation of duties.

## Context
Access control is foundational for platform security and governance.  
This story ensures that baseline roles and RBAC policies are established so that platform and tenant actions are restricted to least-privilege access.

## Actors (Personas and Roles)
- Security Admin: defines roles and policies  
- Platform Admin: applies baseline RBAC configuration  
- Compliance Officer: reviews policies for audit readiness  
- Auditor: verifies role assignments and evidence

## Preconditions
- Platform infrastructure deployed  
- User directory integrated  
- Policy definitions documented

## Scenario Flow
1. Security Admin defines baseline roles and policies for platform and tenant users  
2. Platform Admin applies RBAC configuration to control and data planes  
3. Compliance Officer reviews policy application for regulatory adherence  
4. Auditor validates evidence of role assignments and logs  
5. Baseline RBAC policies published and enforced

## Acceptance Criteria
- Roles defined and approved  
- RBAC applied successfully to platform components  
- Compliance review passed  
- Audit evidence available

## Failure Paths
- Role conflict: policy application fails  
- Missing permissions: user cannot perform required action  
- Excessive permissions: flagged during compliance review

## Observability and Governance
- Audit Events: rbac.defined, rbac.applied, rbac.reviewed  
- Metrics: policy_application_success_rate, permission_violation_count  
- RBAC: least privilege enforced  
- Evidence: role assignment logs, compliance approvals

## Interfaces and Cross Links
- Previous: [Schema Templates Seeding](00c-schema-templates-seeding.md)

## Configuration Examples

**RBAC Baseline Receipt (JSON)**
```json
{
  "role": "TenantAdmin",
  "permissions": ["connector.deploy", "workflow.initiate"],
  "applied_by": "platform_admin@platform.com",
  "compliance_check": "PASS"
}
```

## BDD Scenarios

### Scenario: RBAC baseline applied successfully
```gherkin
Given Security Admin defines baseline roles
When Platform Admin applies the configuration
Then policies are enforced
And compliance review passes
```

### Scenario: RBAC baseline rejected due to excessive permissions
```gherkin
Given Security Admin defines baseline roles
When Compliance Officer detects excessive permissions
Then RBAC configuration is rejected
And error is logged
```

## Review Checklist
- [x] Roles defined and approved  
- [x] RBAC applied successfully  
- [x] Compliance review completed  
- [x] Evidence available  
