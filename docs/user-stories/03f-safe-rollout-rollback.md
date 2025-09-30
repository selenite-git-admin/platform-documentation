# Safe Rollout and Rollback

> Goal: Roll out schema changes safely and revert quickly if needed.  
> Scope: Covers staged rollout, dry runs, canaries, rollback, and evidence.

## Context
Schema changes can break pipelines and KPIs. A safe rollout strategy reduces risk through staged deployment and quick rollback.

## Actors (Personas and Roles)
- Platform Admin: schedules and executes rollout  
- Schema Steward: signs off on readiness  
- Observability Engineer: watches canaries and metrics  
- Tenant Admin: informed of tenant-facing changes

## Preconditions
- Change request approved  
- Dry-run simulation passed  
- Rollback plan prepared

## Scenario Flow
1. Platform Admin schedules a staged rollout with canaries  
2. Observability Engineer monitors key metrics and errors  
3. If healthy, expand rollout to full scope  
4. If issues detected, execute rollback plan  
5. Capture evidence and update status

## Acceptance Criteria
- Rollout completed or safely rolled back  
- No data loss or KPI corruption  
- Evidence available for audit

## Failure Paths
- Canary failure: stop rollout and rollback  
- Monitoring gap: incident logged and fixed  
- Rollback fails: escalate to incident response

## Observability and Governance
- Audit Events: rollout.started, rollout.expanded, rollout.rolled_back  
- Metrics: error_rate_during_rollout, rollback_time_seconds  
- Evidence: rollout receipts and logs

## Interfaces and Cross Links
- Previous: [Tenant-Specific Schema Extension](03e-tenant-specific-schema-extension.md)  
- Next: [Impact Analysis and Notifications](03g-impact-analysis-notifications.md)

## Configuration Examples

**Rollout Plan (JSON)**
```json
{
  "change_id": "SC-2025-09-29-01",
  "stages": ["canary", "25pct", "100pct"],
  "rollback_on": ["error_rate>2pct", "latency>p95+30pct"]
}
```

## BDD Scenarios

### Scenario: Staged rollout succeeds
```gherkin
Given a schema change is approved
When a staged rollout is executed
Then canaries pass and rollout completes
And evidence is recorded
```

### Scenario: Rollout rolled back due to errors
```gherkin
Given a schema change is approved
When canary metrics exceed thresholds
Then the system rolls back
And logs the reason
```

## Review Checklist
- [x] Staged rollout executed  
- [x] Rollback plan validated  
- [x] Evidence captured  
