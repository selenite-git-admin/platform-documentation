# Tenant Decommissioning

> Goal: Decommission a tenant environment safely.  
> Scope: Covers secure deletion of tenant resources, archiving evidence, and updating platform records.

## Context
When a tenant offboards, the platform must ensure secure decommissioning of all resources.  
This story defines the process of disabling access, decommissioning infrastructure, and archiving evidence for compliance.

## Actors (Personas and Roles)
- Platform Admin: initiates decommissioning  
- Security Admin: validates deletion and ensures data is wiped securely  
- Compliance Officer: reviews archived evidence  
- Auditor: confirms process followed policies

## Preconditions
- Tenant offboarding request approved  
- Active tenant resources identified  
- Compliance policy defined for data retention and archival

## Scenario Flow
1. Platform Admin initiates tenant decommissioning  
2. Tenant access disabled and login revoked  
3. Infrastructure resources decommissioned securely  
4. Security Admin validates that data is wiped  
5. Compliance Officer archives receipts and logs  
6. Auditor verifies completion against policies

## Acceptance Criteria
- Tenant access revoked  
- Resources deleted securely  
- Evidence archived  
- Audit confirms compliance

## Failure Paths
- Incomplete deletion: resources remain active, alert raised  
- Evidence missing: compliance review fails  
- Data retention policy violated: incident logged

## Observability and Governance
- Audit Events: tenant.decommissioned, data.wiped, evidence.archived  
- Metrics: decommissioning_success_rate, incident_count  
- Evidence: archival logs, deletion receipts

## Interfaces and Cross Links
- Previous: [Tenant Infrastructure Provisioning](01b-tenant-infrastructure-provisioning.md)

## Configuration Examples

**Tenant Decommissioning Receipt (JSON)**
```json
{
  "tenant_id": "TEN-001",
  "status": "DECOMMISSIONED",
  "deleted_by": "platform_admin@platform.com",
  "validated_by": "security_admin@platform.com",
  "archived_by": "compliance_officer@platform.com",
  "timestamp": "2025-09-29T11:00:00Z"
}
```

## BDD Scenarios

### Scenario: Successful tenant decommissioning
```gherkin
Given tenant offboarding is approved
When Platform Admin decommissions the tenant
Then resources are deleted
And evidence is archived
```

### Scenario: Tenant decommissioning fails due to missing evidence
```gherkin
Given Platform Admin decommissions the tenant
When compliance evidence is missing
Then decommissioning is blocked
And incident is logged
```

## Review Checklist
- [x] Tenant access revoked  
- [x] Resources deleted securely  
- [x] Evidence archived  
- [x] Audit confirmed  
