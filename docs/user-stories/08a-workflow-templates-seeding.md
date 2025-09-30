# Workflow Templates Seeding

> Goal: Seed baseline workflow templates for governed actions.  
> Scope: Covers loading templates, validating inputs, enabling for tenant use.

## Context
Workflow templates provide consistent, governed actions such as spend freeze, credit hold, or price override. Seeding templates makes these actions available to tenants with auditable defaults.

## Actors (Personas and Roles)
- Workflow Author: defines templates and input contracts  
- Platform Admin: seeds templates into the platform  
- Compliance Officer: reviews templates for policy alignment  
- Observability Engineer: monitors template usage

## Preconditions
- Evidence and policy framework available  
- Template definitions authored and reviewed  
- Registry for templates active

## Scenario Flow
1. Platform Admin loads workflow templates into the registry  
2. Compliance Officer reviews approvals and risk treatments  
3. Templates are versioned and enabled for tenant scoping  
4. Observability Engineer verifies usage dashboards

## Acceptance Criteria
- Templates loaded and versioned  
- Compliance review recorded  
- Templates enabled for tenant use  
- Evidence captured

## Failure Paths
- Invalid template schema: reject and log error  
- Missing approvals: template not enabled  
- Version conflict: block duplicate

## Observability and Governance
- Audit Events: workflow.template.seeded, workflow.template.versioned, workflow.template.enabled  
- Metrics: template_enable_rate, template_usage_count  
- Evidence: template receipts and review logs

## Interfaces and Cross Links
- Previous: [KPI Consumption](07-kpi-consumption.md)  
- Next: [Workflow Authoring and Configuration](08b-workflow-authoring-configuration.md)

## Configuration Examples

**Template Receipt (YAML)**
```yaml
template_id: WF-DELAY-VENDOR-PAYMENTS
inputs:
  - vendor_segment
  - hold_days
approvals:
  - finance_policy
status: enabled
version: v1.0
```

## BDD Scenarios

### Scenario: Template seeded and enabled
```gherkin
Given a workflow template is authored
When Platform Admin seeds the template
And Compliance Officer reviews it
Then the template is versioned and enabled
And evidence is recorded
```

## Review Checklist
- [x] Templates loaded  
- [x] Compliance reviewed  
- [x] Enabled for tenants  
- [x] Evidence available  
