# Workflow Authoring and Configuration

> Goal: Author new workflows and configure tenant-specific parameters.  
> Scope: Covers template derivation, parameter defaults, and tenant enablement.

## Context
Tenants often need tailored variations of baseline workflows. Authoring and configuration ensure each tenant can adopt workflows with correct parameters and controls.

## Actors (Personas and Roles)
- Workflow Author: creates or derives workflows from templates  
- Tenant Admin: provides tenant parameters and scopes  
- Platform Admin: applies configuration and enables workflow  
- Compliance Officer: validates parameter risk

## Preconditions
- Templates seeded and available  
- Tenant scope defined  
- Parameter catalog documented

## Scenario Flow
1. Workflow Author derives a tenant-specific workflow from a template  
2. Tenant Admin supplies parameter values and scopes  
3. Platform Admin applies configuration and enables workflow  
4. Compliance Officer validates risk-sensitive parameters

## Acceptance Criteria
- Tenant workflow configured and enabled  
- Parameters validated and stored securely  
- Evidence recorded

## Failure Paths
- Missing parameter: configuration blocked  
- Invalid scope: workflow not enabled  
- Compliance rejection: revision requested

## Observability and Governance
- Audit Events: workflow.authored, workflow.configured, workflow.enabled  
- Metrics: workflow_enable_rate, parameter_validation_pass_rate  
- Evidence: configuration logs and approvals

## Interfaces and Cross Links
- Previous: [Workflow Templates Seeding](08a-workflow-templates-seeding.md)  
- Next: [Triggers and Approvals](08c-triggers-approvals.md)

## Configuration Examples

**Tenant Workflow Config (JSON)**
```json
{
  "workflow_id": "WF-DELAY-VENDOR-PAYMENTS-ACME",
  "params": {"vendor_segment": "non_critical", "hold_days": 14},
  "scope": "tenant:ACME",
  "status": "ENABLED"
}
```

## BDD Scenarios

### Scenario: Workflow configured for tenant
```gherkin
Given a template is available
When a tenant provides parameters
Then the workflow is configured and enabled
And evidence is recorded
```

## Review Checklist
- [x] Derived workflow created  
- [x] Parameters validated  
- [x] Enabled for tenant  
- [x] Evidence captured  
