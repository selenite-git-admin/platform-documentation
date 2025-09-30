# Connector Handshake and Preflight

> Goal: Validate a connector and establish initial handshake with the data source.  
> Scope: Covers preflight validation, schema checks, and readiness confirmation.

## Context
Before data starts flowing from a source, the connector must perform a handshake and validation.  
This prevents schema mismatches and connectivity errors from impacting GDP and KPI layers.

## Actors (Personas and Roles)
- Tenant Data Engineer: provides source configuration details  
- Platform Admin: runs connector handshake and preflight validation  
- Security Admin: validates secrets and access scope  
- Observability Engineer: monitors preflight results

## Preconditions
- Data source registered and active  
- Connector deployed  
- Credentials stored in secrets system

## Scenario Flow
1. Platform Admin initiates connector handshake with the data source  
2. Preflight validation runs, checking schema and connection integrity  
3. Security Admin validates credential usage and access scope  
4. Observability Engineer ensures preflight metrics are logged  
5. Connector marked ready if all checks succeed

## Acceptance Criteria
- Handshake completed successfully  
- Schema validated and consistent  
- Credentials validated securely  
- Connector marked ready

## Failure Paths
- Schema mismatch: validation fails, incident ticket generated  
- Invalid credential usage: preflight fails, error logged  
- Connectivity error: handshake attempt fails, alert raised

## Observability and Governance
- Audit Events: connector.handshake, connector.validated  
- Metrics: handshake_success_rate, schema_validation_pass_rate  
- Evidence: preflight logs and connector receipt

## Interfaces and Cross Links
- Previous: [Data Source Onboarding](02-source-onboarding.md)

## Configuration Examples

**Connector Preflight Receipt (YAML)**
```yaml
connector: ERP
handshake: complete
schema_check: PASS
validated_by: security_admin@platform.com
status: READY
```

## BDD Scenarios

### Scenario: Successful connector handshake and validation
```gherkin
Given data source is registered
And connector is deployed
When Platform Admin initiates handshake
Then schema validation passes
And connector status is READY
```

### Scenario: Connector handshake fails due to schema mismatch
```gherkin
Given data source is registered
When connector preflight detects schema mismatch
Then connector status is FAILED
And incident ticket is created
```

## Review Checklist
- [x] Handshake completed  
- [x] Schema validated  
- [x] Connector ready  
- [x] Evidence available  
