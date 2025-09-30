# Data Source Onboarding

> Goal: Onboard a new data source into the platform.  
> Scope: Covers registering the source, configuring credentials, and validating connectivity.

## Context
Data source onboarding is required before information can flow into the platform.  
This story ensures that a new data source is registered, authenticated, and validated so that subsequent GDP and KPI processing can take place.

## Actors (Personas and Roles)
- Tenant Data Engineer: requests source onboarding and provides configuration details  
- Platform Admin: registers and configures the data source  
- Security Admin: validates credentials and policies  
- Observability Engineer: ensures monitoring for source activity

## Preconditions
- Tenant identity active  
- Connector for the data source available  
- Credentials approved and stored securely

## Scenario Flow
1. Tenant Data Engineer submits onboarding request with source details  
2. Platform Admin registers the data source in the platform  
3. Credentials stored in the secrets management system  
4. Security Admin validates authentication and access scope  
5. Connectivity tested with preflight validation  
6. Observability Engineer enables monitoring of the new source

## Acceptance Criteria
- Data source registered successfully  
- Credentials secured and validated  
- Connectivity confirmed with test records  
- Monitoring active for source activity

## Failure Paths
- Invalid credentials: onboarding fails, error logged  
- Network unreachable: connection test fails, alert raised  
- Compliance validation fails: source blocked

## Observability and Governance
- Audit Events: source.onboarded, source.validated  
- Metrics: onboarding_success_rate, connection_test_latency  
- Evidence: onboarding receipt and validation logs

## Interfaces and Cross Links
- Next: [Connector Handshake and Preflight](02b-connector-handshake-preflight.md)

## Configuration Examples

**Source Onboarding Receipt (JSON)**
```json
{
  "source": "ERP",
  "status": "ACTIVE",
  "onboarded_by": "platform_admin@platform.com",
  "validated_by": "security_admin@platform.com",
  "timestamp": "2025-09-29T11:30:00Z"
}
```

## BDD Scenarios

### Scenario: Successful data source onboarding
```gherkin
Given tenant identity is active
And connector is available
When Platform Admin registers the data source
And Security Admin validates credentials
Then the data source status is ACTIVE
```

### Scenario: Data source onboarding fails due to invalid credentials
```gherkin
Given tenant identity is active
When Tenant Data Engineer provides invalid credentials
Then onboarding fails
And an error is logged
```

## Review Checklist
- [x] Source registered  
- [x] Credentials secured  
- [x] Connectivity tested  
- [x] Monitoring enabled  
