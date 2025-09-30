# Tenant-Specific Schema Extension

> Goal: Allow controlled extensions to schemas for tenant needs.  
> Scope: Covers extension proposal, validation, namespacing, rollout, and audit.

## Context
Some tenants need extra fields that do not belong in global contracts. Controlled extensions allow flexibility without breaking shared models.

## Actors (Personas and Roles)
- Tenant Admin: proposes extension  
- Schema Steward: validates design and namespace  
- Platform Admin: implements extension hooks  
- Compliance Officer: reviews regulatory impact

## Preconditions
- Base schema version published  
- Extension namespace strategy documented  
- Validation tooling supports custom fields

## Scenario Flow
1. Tenant Admin proposes an extension with business case  
2. Schema Steward validates fields, namespacing, and constraints  
3. Platform Admin applies extension configuration  
4. Extension rolled out to tenant scope only  
5. Documentation and lineage updated

## Acceptance Criteria
- Extension approved and applied in tenant scope  
- No impact to global consumers  
- Evidence captured with lineage updates

## Failure Paths
- Namespace conflict: extension rejected  
- Constraint violation: extension blocked  
- Unexpected side effects: rollback executed

## Observability and Governance
- Audit Events: schema.extension.approved, schema.extension.deployed  
- Metrics: extension_count, extension_rollback_count  
- Evidence: extension receipts and lineage links

## Interfaces and Cross Links
- Previous: [Tenant Schema Change Request](03d-tenant-schema-change-request.md)  
- Next: [Safe Rollout and Rollback](03f-safe-rollout-rollback.md)

## Configuration Examples

**Tenant Extension (YAML)**
```yaml
tenant_id: TEN-001
base_schema: GDP-AR
extension:
  payment_terms_detail: string
scope: tenant
status: deployed
```

## BDD Scenarios

### Scenario: Tenant extension deployed safely
```gherkin
Given a tenant proposes a schema extension
When validation passes with namespacing
Then the extension is deployed to tenant scope
And lineage is updated
```

### Scenario: Tenant extension rejected due to namespace conflict
```gherkin
Given a tenant proposes a schema extension
When a namespace conflict is detected
Then the extension is rejected
And an error is logged
```

## Review Checklist
- [x] Extension validated and namespaced  
- [x] Tenant-only scope enforced  
- [x] Evidence and lineage updated  
