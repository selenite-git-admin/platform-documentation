# Schema Templates Seeding

> Goal: Seed schema templates that define raw, GDP, and KPI structures.  
> Scope: Covers loading baseline schemas, validating structures, and making them available for tenants.

## Context
Schema templates provide the foundation for consistent data modeling across tenants.  
By seeding standardized templates, the platform ensures that GDP and KPI layers are aligned and reusable.  
This story focuses on making schema templates available and validated.

## Actors (Personas and Roles)
- Schema Steward: defines and validates schema templates  
- Platform Admin: seeds templates into the platform  
- Compliance Officer: reviews templates for regulatory alignment  
- Observability Engineer: monitors schema versioning

## Preconditions
- Platform infrastructure and connectors active  
- Schema definitions available and approved  
- Version control system ready for tracking schemas

## Scenario Flow
1. Platform Admin loads schema templates into the control plane  
2. Schema Steward validates structure, field definitions, and lineage rules  
3. Compliance Officer confirms regulatory requirements are captured  
4. Templates versioned and marked as available for tenants  
5. Observability Engineer ensures schema usage is tracked

## Acceptance Criteria
- Templates loaded successfully  
- Validation completed by Schema Steward  
- Compliance review passed  
- Templates versioned and published

## Failure Paths
- Invalid schema definition: validation fails, error logged  
- Missing compliance field: template rejected  
- Version conflict: schema versioning process blocks duplicate

## Observability and Governance
- Audit Events: schema.seeded, schema.validated, schema.published  
- Metrics: template_validation_success_rate, schema_usage_count  
- RBAC: seeding restricted to Platform Admin, validation by Schema Steward  
- Evidence: validation logs and version receipts

## Interfaces and Cross Links
- Previous: [Connector Deployment and Maintenance](00b-connector-deployment.md)  
- Next: [Access and RBAC Baseline](00d-access-rbac-baseline.md)

## Configuration Examples

**Schema Template Receipt (YAML)**
```yaml
schema_id: GDP-001
status: published
validated_by: schema_steward@platform.com
compliance_check: PASS
version: v1.0
```

## BDD Scenarios

### Scenario: Schema template seeded successfully
```gherkin
Given Platform Admin loads schema templates
When Schema Steward validates definitions
And Compliance Officer approves
Then schema template is published
And version receipt is generated
```

### Scenario: Schema template rejected due to missing compliance field
```gherkin
Given Platform Admin loads schema templates
When Compliance Officer detects missing regulatory field
Then template is rejected
And error is logged
```

## Review Checklist
- [x] Schema templates loaded  
- [x] Validation completed  
- [x] Compliance confirmed  
- [x] Version receipts available  
