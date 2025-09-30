# Tenant Infrastructure Provisioning

> Goal: Provision tenant-specific infrastructure resources.  
> Scope: Covers creation of dedicated compute, storage, and networking for tenant workloads.

## Context
Each tenant requires dedicated infrastructure resources to ensure isolation and performance.  
This story provisions tenant-specific compute, storage, and network resources and validates them before data onboarding.

## Actors (Personas and Roles)
- Platform Admin: provisions tenant infrastructure  
- Security Admin: validates isolation policies  
- Observability Engineer: ensures monitoring is enabled  
- Tenant Admin: receives visibility into resources

## Preconditions
- Tenant identity created  
- Resource quotas available  
- Infrastructure templates approved

## Scenario Flow
1. Platform Admin provisions tenant compute, storage, and networking resources  
2. Security Admin validates VPC, IAM roles, and firewall rules  
3. Observability Engineer enables monitoring and logging for tenant resources  
4. Tenant Admin receives confirmation of infrastructure readiness

## Acceptance Criteria
- Tenant resources provisioned successfully  
- Security validation passed  
- Monitoring and logging enabled  
- Evidence available for audit

## Failure Paths
- Resource quota exceeded: provisioning blocked  
- Security validation fails: resources decommissioned  
- Monitoring setup error: observability incomplete

## Observability and Governance
- Audit Events: infra.tenant.provisioned, infra.tenant.validated  
- Metrics: tenant_infra_success_rate, validation_failure_count  
- Evidence: resource allocation logs

## Interfaces and Cross Links
- Previous: [Tenant Provisioning](01-tenant-provisioning.md)  
- Next: [Tenant Decommissioning](01c-tenant-decommissioning.md)

## Configuration Examples

**Tenant Infrastructure Receipt (YAML)**
```yaml
tenant_id: TEN-001
compute: provisioned
storage: provisioned
network: provisioned
validated_by: security_admin@platform.com
status: SUCCESS
```

## BDD Scenarios

### Scenario: Successful tenant infrastructure provisioning
```gherkin
Given tenant identity exists
When Platform Admin provisions tenant infrastructure
Then compute, storage, and network are provisioned
And validated by Security Admin
```

### Scenario: Provisioning fails due to quota issue
```gherkin
Given tenant identity exists
When Platform Admin provisions infrastructure
And resource quota is exceeded
Then provisioning is blocked
And error logged
```

## Review Checklist
- [x] Resources provisioned  
- [x] Security validation passed  
- [x] Monitoring enabled  
- [x] Evidence available  
