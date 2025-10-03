# Flow: Tenant Onboarding

## Purpose
Describe how a tenant selects a connector and prepares it for execution.

## Actors
- Tenant administrator
- Orchestrator
- Secrets service

## Steps
1. Administrator selects connector and version from the catalog. 
2. Administrator selects runner profile and network route. 
3. Administrator supplies credential references and stream selection rules. 
4. Orchestrator validates choices against the manifest. 
5. Orchestrator stores a connection profile and initial state baseline.

## Inputs
- Catalog entry
- Runner profiles
- Credential references
- Stream selection rules

## Outputs
- Connection profile
- Initial state
- Validation results

## Observability
- Audit logs for selection and validation
- Errors for invalid combinations
