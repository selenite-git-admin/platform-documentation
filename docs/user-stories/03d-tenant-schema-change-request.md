# Tenant Schema Change Request

> Goal: Manage tenant-initiated schema change requests.  
> Scope: Covers request submission, impact analysis, approval, rollout, and audit.

## Context
Tenants may request schema changes to support new fields or corrections. This process controls risk by assessing impact and coordinating rollout with evidence.

## Actors (Personas and Roles)
- Tenant Admin: submits change request  
- Schema Steward: reviews and validates change  
- Platform Admin: schedules rollout  
- Observability Engineer: monitors impact

## Preconditions
- Active schemas in registry  
- Change request form available  
- Impact analysis tooling ready

## Scenario Flow
1. Tenant Admin submits change request with justification  
2. Schema Steward validates and estimates impact  
3. Platform Admin schedules rollout in a safe window  
4. Notifications sent to affected consumers  
5. Rollout executed with monitoring

## Acceptance Criteria
- Request documented and approved  
- Impact analysis attached  
- Rollout executed with no breakage  
- Evidence captured

## Failure Paths
- Incomplete request: send back for clarification  
- High-risk impact: rollback plan required or request denied  
- Rollout failure: automatic rollback and incident

## Observability and Governance
- Audit Events: schema.change.requested, schema.change.approved, schema.change.deployed  
- Metrics: change_success_rate, rollback_count  
- Evidence: request docs and deployment receipts

## Interfaces and Cross Links
- Previous: [KPI Schema Lifecycle](03c-kpi-schema-lifecycle.md)  
- Next: [Tenant-Specific Schema Extension](03e-tenant-specific-schema-extension.md)

## Configuration Examples

**Change Request (JSON)**
```json
{
  "tenant_id": "TEN-001",
  "schema": "GDP-AR",
  "change": "add field payment_terms",
  "risk": "medium",
  "status": "APPROVED"
}
```

## BDD Scenarios

### Scenario: Tenant schema change approved and deployed
```gherkin
Given a tenant submits a schema change request
When the change is validated and approved
Then the rollout is scheduled and executed
And evidence is captured
```

### Scenario: Tenant schema change rejected due to high risk
```gherkin
Given a tenant submits a schema change request
When impact analysis indicates high risk without rollback
Then the request is rejected
And a recommendation is provided
```

## Review Checklist
- [x] Request documented and validated  
- [x] Impact analyzed  
- [x] Rollout executed or rejected with rationale  
- [x] Evidence captured  
