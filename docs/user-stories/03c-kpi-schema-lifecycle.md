# KPI Schema Lifecycle

> Goal: Manage lifecycle of KPI schemas based on GDP.  
> Scope: Covers KPI definition, validation, versioning, publishing, and governance.

## Context
KPI schemas drive dashboards and actions. They must be precise and versioned to maintain executive trust.

## Actors (Personas and Roles)
- Schema Steward: defines KPI schema fields and logic  
- Platform Admin: registers KPI schemas  
- Compliance Officer: validates regulatory requirements  
- Observability Engineer: monitors lineage and usage

## Preconditions
- GDP schema lifecycle active  
- KPI definition approved by business stakeholders  
- Registry supports KPI versioning

## Scenario Flow
1. Schema Steward defines KPI schema linked to GDP fields  
2. Platform Admin registers the KPI schema in the registry  
3. Compliance Officer validates compliance fields  
4. KPI schema versioned and published for consumption  
5. Observability Engineer monitors KPI lineage usage

## Acceptance Criteria
- KPI schema registered and versioned  
- Compliance validation passed  
- Lineage mapping updated  
- Evidence available

## Failure Paths
- Invalid definition: reject with error  
- Compliance failure: block publishing  
- Version conflict: prevent duplicate

## Observability and Governance
- Audit Events: schema.kpi.created, schema.kpi.validated, schema.kpi.versioned  
- Metrics: kpi_schema_validation_rate, kpi_usage_count  
- Evidence: validation logs and lineage mappings

## Interfaces and Cross Links
- Previous: [GDP Schema Lifecycle](03b-gdp-schema-lifecycle.md)  
- Next: [Tenant Schema Change Request](03d-tenant-schema-change-request.md)

## Configuration Examples

**KPI Schema Receipt (YAML)**
```yaml
schema_id: KPI-DSO
based_on: GDP-AR
status: published
validated_by: compliance_officer@platform.com
version: v1.0
```

## BDD Scenarios

### Scenario: KPI schema validated and published
```gherkin
Given the GDP schema lifecycle is active
When a KPI schema is defined and validated
Then the KPI schema is registered and versioned
And publishing is allowed
```

### Scenario: KPI schema rejected due to invalid definition
```gherkin
Given a KPI schema is defined
When the definition is invalid
Then the KPI schema is rejected
And an error is logged
```

## Review Checklist
- [x] KPI schema created and validated  
- [x] Compliance passed  
- [x] Versioned in registry  
- [x] Evidence available  
