# GDP Schema Lifecycle

> Goal: Manage lifecycle of Golden Data Point (GDP) schemas.  
> Scope: Covers GDP schema creation, validation, versioning, communication, and deprecation.

## Context
GDP schemas are the standardized layer that powers KPIs and actions. They must be versioned and governed for cross-tenant consistency and trust.

## Actors (Personas and Roles)
- Schema Steward: defines GDP schemas and mappings  
- Platform Admin: publishes schemas to the registry  
- Compliance Officer: verifies regulatory fields  
- Observability Engineer: monitors usage

## Preconditions
- Raw schema lifecycle active  
- Transformation mappings available  
- Registry supports GDP versioning

## Scenario Flow
1. Schema Steward defines GDP schema with mappings from raw sources  
2. Platform Admin registers GDP schema in the registry  
3. Compliance Officer validates regulatory coverage  
4. Schema versioned and lineage mapping updated  
5. Broadcast change notice to impacted tenants

## Acceptance Criteria
- GDP schema registered and versioned  
- Compliance validation passed  
- Lineage mapping updated  
- Change notice delivered

## Failure Paths
- Invalid mapping: reject with error  
- Compliance failure: block publishing  
- Version conflict: prevent duplicate

## Observability and Governance
- Audit Events: schema.gdp.created, schema.gdp.validated, schema.gdp.versioned  
- Metrics: gdp_validation_rate, gdp_usage_count  
- Evidence: validation logs and lineage receipts

## Interfaces and Cross Links
- Previous: [Source (Raw) Schema Lifecycle](03a-raw-schema-lifecycle.md)  
- Next: [KPI Schema Lifecycle](03c-kpi-schema-lifecycle.md)

## Configuration Examples

**GDP Schema Definition (JSON)**
```json
{
  "schema_id": "GDP-AR",
  "fields": ["customer_id", "invoice_amount_net", "currency"],
  "status": "versioned",
  "version": "v1.0"
}
```

## BDD Scenarios

### Scenario: GDP schema created and validated
```gherkin
Given raw schema lifecycle is active
When Schema Steward defines a GDP schema
And Compliance Officer validates required fields
Then the GDP schema is registered and versioned
```

### Scenario: GDP schema rejected due to compliance failure
```gherkin
Given Schema Steward defines a GDP schema
When Compliance Officer finds a missing regulatory field
Then publishing is blocked
And an error is logged
```

## Review Checklist
- [x] GDP schema published  
- [x] Compliance validated  
- [x] Version recorded and lineage mapped  
- [x] Change notice issued  
