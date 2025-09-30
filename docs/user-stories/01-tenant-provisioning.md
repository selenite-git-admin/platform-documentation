# Tenant Provisioning

> Goal: Provision a new tenant environment with baseline configuration.  
> Scope: Covers creation of tenant identity, assignment of resources, and validation of provisioning.

## Context
Tenant provisioning is the first step to onboard a customer onto the platform.  
This process must ensure isolation, security, and readiness for subsequent configuration such as connectors and schemas.  
The goal is to provide a governed and auditable way of provisioning tenant environments.

## Actors (Personas and Roles)
- Platform Admin: initiates and executes provisioning  
- Tenant Admin: receives access to manage tenant-specific settings  
- Security Admin: validates isolation and access policies  
- Compliance Officer: reviews evidence of provisioning

## Preconditions
- Platform infrastructure active  
- RBAC baseline established  
- Tenant onboarding request approved

## Scenario Flow
1. Platform Admin creates tenant identity in the control plane  
2. Dedicated data plane resources are assigned to the tenant  
3. Secrets, keys, and network isolation configured  
4. Security Admin validates configuration and access policies  
5. Tenant Admin receives credentials and login access  
6. Compliance Officer reviews evidence of provisioning

## Acceptance Criteria
- Tenant identity created and active  
- Resources isolated and secured  
- Tenant Admin access provisioned  
- Evidence available for audit

## Failure Paths
- Resource allocation failure: provisioning incomplete, alert raised  
- IAM misconfiguration: tenant access not established, rollback executed  
- Compliance review fails: tenant provisioning blocked

## Observability and Governance
- Audit Events: tenant.created, tenant.validated  
- Metrics: provisioning_success_rate, provisioning_time  
- Evidence: provisioning receipts stored for compliance

## Interfaces and Cross Links
- Next: [Tenant Infrastructure Provisioning](01b-tenant-infrastructure-provisioning.md)

## Configuration Examples

**Tenant Provisioning Receipt (JSON)**
```json
{
  "tenant_id": "TEN-001",
  "status": "ACTIVE",
  "created_by": "platform_admin@platform.com",
  "validated_by": "security_admin@platform.com",
  "timestamp": "2025-09-29T10:30:00Z"
}
```

## BDD Scenarios

### Scenario: Successful tenant provisioning
```gherkin
Given platform infrastructure is active
When Platform Admin provisions a tenant
Then tenant identity and resources are created
And Tenant Admin receives access
```

### Scenario: Tenant provisioning fails due to IAM misconfiguration
```gherkin
Given Platform Admin provisions a tenant
When IAM configuration fails
Then tenant access is not established
And provisioning is rolled back
```

## Review Checklist
- [x] Tenant identity created  
- [x] Resources isolated  
- [x] Tenant Admin access active  
- [x] Evidence available  
