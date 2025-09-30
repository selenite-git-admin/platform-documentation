# Impact Analysis and Notifications

> Goal: Analyze the impact of schema changes and notify affected stakeholders.  
> Scope: Covers dependency graphing, blast radius estimation, notifications, and sign-off tracking.

## Context
Schema changes affect pipelines, KPIs, and dashboards. Impact analysis helps avoid surprises and ensures stakeholders are informed before rollout.

## Actors (Personas and Roles)
- Schema Steward: runs impact analysis  
- Platform Admin: coordinates notifications and windows  
- Observability Engineer: validates health after change  
- Tenant Admin: receives notifications for tenant scope

## Preconditions
- Dependency graph and lineage available  
- Notification channels configured  
- Calendar for change windows defined

## Scenario Flow
1. Schema Steward runs impact analysis to determine blast radius  
2. Platform Admin schedules change window and notifies affected users  
3. Observability Engineer monitors post-change health  
4. Sign-offs recorded from required stakeholders

## Acceptance Criteria
- Impact analysis attached to change  
- Notifications sent to all affected stakeholders  
- Post-change health confirmed  
- Sign-offs recorded

## Failure Paths
- Incomplete dependency graph: analysis flagged and review required  
- Notification failure: resend with alternate channel  
- Post-change incident: open ticket and remediate

## Observability and Governance
- Audit Events: impact.analysis.completed, notifications.sent, signoffs.recorded  
- Metrics: coverage_of_notified_assets, post_change_incident_rate  
- Evidence: analysis report and notification receipts

## Interfaces and Cross Links
- Previous: [Safe Rollout and Rollback](03f-safe-rollout-rollback.md)

## Configuration Examples

**Notification Packet (YAML)**
```yaml
change_id: SC-2025-09-29-01
impact_scope:
  datasets: ["gdp_ar", "kpi_dso"]
  dashboards: ["finance_overview"]
recipients: ["tenant_admin@acme.com", "platform_admin@platform.com"]
status: sent
```

## BDD Scenarios

### Scenario: Impact analysis completed and notifications sent
```gherkin
Given a schema change is approved
When impact analysis runs
Then notifications are sent to affected stakeholders
And sign-offs are recorded
```

### Scenario: Post-change incident triggers follow-up
```gherkin
Given a schema change was deployed
When an incident occurs post-change
Then a remediation ticket is created
And stakeholders are informed
```

## Review Checklist
- [x] Analysis complete  
- [x] Notifications sent  
- [x] Post-change health confirmed  
- [x] Sign-offs recorded  
