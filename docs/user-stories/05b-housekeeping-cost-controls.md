# Automated Housekeeping and Cost Controls

> Goal: Reduce storage and compute costs while preserving compliance.  
> Scope: Covers retention schedules, tiering, compaction, and cost guardrails.

## Context
Costs can grow quickly if storage and compute are not managed.  
This story defines automated tasks to clean up, tier, or compact data and to enforce cost limits without impacting compliance or availability.

## Actors (Personas and Roles)
- Platform Admin: configures housekeeping jobs and cost controls  
- Security Admin: validates that cleanups meet policy and do not remove protected data  
- Observability Engineer: monitors cost and housekeeping metrics  
- Compliance Officer: approves retention schedules

## Preconditions
- Evidence and retention policies defined  
- Storage and compute metrics available  
- Job scheduler active

## Scenario Flow
1. Platform Admin defines retention schedules and tiering rules  
2. Compaction and vacuum jobs scheduled for large datasets  
3. Cost guardrails set such as daily spend caps or action budgets  
4. Security Admin validates that protected data is excluded from deletion  
5. Observability Engineer reviews dashboards for storage footprint and spend

## Acceptance Criteria
- Retention and tiering in effect and verifiable  
- Compaction jobs complete successfully  
- Cost guardrails active and alerting works  
- Evidence of housekeeping stored

## Failure Paths
- Over deletion risk: job blocked by security rules  
- Compaction failure: job error logged and retried  
- Spend overrun: guardrail triggers block on non essential actions

## Observability and Governance
- Audit Events: housekeeping.scheduled, housekeeping.executed, cost.guardrail.enforced  
- Metrics: storage_footprint_gb, compute_hours, spend_to_budget_ratio  
- Evidence: housekeeping logs and cost reports

## Interfaces and Cross Links
- Previous: [Evidence](05-evidence-lineage.md)

## Configuration Examples

**Retention Policy (YAML)**
```yaml
policy_id: RET-12M
scope: gdp
retention_months: 12
action_on_expiry: tier_to_cold
```

**Cost Guardrail (JSON)**
```json
{
  "guardrail_id": "COST-CAP-DAILY",
  "tenant_scope": "global",
  "daily_spend_cap_usd": 500,
  "on_breach": "block_non_essential_actions"
}
```

## BDD Scenarios

### Scenario: Retention policy moves data to cold storage
```gherkin
Given retention policy RET-12M is active
When a dataset exceeds 12 months
Then the system tiers data to cold storage
And records a housekeeping event
```

### Scenario: Cost cap blocks non essential actions
```gherkin
Given cost guardrail COST-CAP-DAILY is active
When daily spend exceeds the cap
Then non essential actions are blocked
And an alert is raised
```

## Review Checklist
- [x] Retention and tiering configured  
- [x] Compaction jobs scheduled and passing  
- [x] Cost guardrails active  
- [x] Evidence and reports available  
