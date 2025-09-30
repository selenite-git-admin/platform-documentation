# Source (Raw) Schema Lifecycle

> Goal: Manage lifecycle of raw source schemas ingested from tenant systems.  
> Scope: Covers registration, validation, versioning, drift detection, and retirement of raw schemas.

## Context
Raw schemas represent the original format of ingested data. The aim is to register and version them so downstream transformations remain stable. Changes must be validated and communicated to avoid breakage.

## Actors (Personas and Roles)
- Tenant Data Engineer: submits source schema details  
- Platform Admin: registers schemas in the registry  
- Schema Steward: validates definitions and metadata  
- Observability Engineer: monitors drift and alerts

## Preconditions
- Data source onboarding complete  
- Schema registry active  
- Validation tooling available

## Scenario Flow
1. Tenant Data Engineer submits the raw schema definition  
2. Platform Admin registers schema in the registry  
3. Schema Steward validates structure and metadata completeness  
4. Version recorded with lineage mapping to GDP fields  
5. Observability Engineer monitors ingestion for drift

## Acceptance Criteria
- Raw schema registered and versioned  
- Validation passed with evidence  
- Lineage mapping available  
- Drift monitoring enabled

## Failure Paths
- Invalid schema definition: reject and log error  
- Drift detected: raise alert and open review ticket  
- Version conflict: registry blocks duplicate

## Observability and Governance
- Audit Events: schema.raw.registered, schema.raw.validated, schema.raw.versioned  
- Metrics: schema_validation_pass_rate, drift_detection_count  
- Evidence: schema receipts and drift logs

## Interfaces and Cross Links
- Next: [GDP Schema Lifecycle](03b-gdp-schema-lifecycle.md)

## Configuration Examples

**Raw Schema Registration (YAML)**
```yaml
schema_id: RAW-CUST-001
status: registered
version: v1.0
validated_by: schema_steward@platform.com
```

## BDD Scenarios

### Scenario: Successful raw schema registration
```gherkin
Given source onboarding is complete
When Platform Admin registers a raw schema
Then validation passes
And the schema is versioned
```

### Scenario: Raw schema rejected due to invalid definition
```gherkin
Given Tenant Data Engineer submits an invalid schema
When validation runs
Then the schema is rejected
And an error is logged
```

## Review Checklist
- [x] Schema registered and versioned  
- [x] Validation evidence captured  
- [x] Lineage mapping established  
- [x] Drift monitoring configured  
