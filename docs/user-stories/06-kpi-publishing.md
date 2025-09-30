# KPI Publishing

> Goal: Publish validated KPI definitions to tenant dashboards.  
> Scope: Covers making KPI definitions available, logging the event, and confirming visibility.

## Context
Once KPI logic is validated, it must be published so executives can consume it. Publishing must be controlled, auditable, and reversible if needed.

## Actors (Personas and Roles)
- Platform Admin: publishes KPI definitions  
- Business Owner: confirms visibility and correctness  
- Compliance Officer: verifies publishing evidence  
- Observability Engineer: monitors usage

## Preconditions
- KPI definition validated and approved  
- Dashboards configured for target personas

## Scenario Flow
1. Platform Admin publishes KPI definition to dashboards  
2. Business Owner confirms KPI visibility and values  
3. Compliance Officer verifies publishing logs and evidence  
4. Observability Engineer tracks consumption metrics

## Acceptance Criteria
- KPI visible on dashboards for intended roles  
- Publishing logs recorded  
- Evidence available for audit

## Failure Paths
- Publishing error: KPI not visible, alert raised  
- Evidence missing: publishing blocked  
- Dashboard misconfiguration: correction needed

## Observability and Governance
- Audit Events: kpi.published, kpi.consumed  
- Metrics: kpi_publish_success_rate, kpi_consumption_rate  
- Evidence: publishing receipts and logs

## Interfaces and Cross Links
- Previous: [KPI Schema Lifecycle](03c-kpi-schema-lifecycle.md)  
- Next: [KPI Consumption](07-kpi-consumption.md)

## Configuration Examples

**Publishing Receipt (YAML)**
```yaml
kpi_id: DSO
status: published
published_by: platform_admin@platform.com
timestamp: "2025-09-29T12:00:00Z"
```

## BDD Scenarios

### Scenario: KPI published successfully
```gherkin
Given KPI validation is complete
When Platform Admin publishes the KPI
Then KPI is visible on dashboards
And logs are recorded
```

### Scenario: KPI publishing fails due to evidence gap
```gherkin
Given KPI validation is complete
When publishing evidence is missing
Then publishing is blocked
And error is logged
```

## Review Checklist
- [x] KPI published  
- [x] Visibility confirmed  
- [x] Evidence recorded  
