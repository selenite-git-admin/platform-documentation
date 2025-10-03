# Runbook

## Scope
Operational procedures for Tenant Management in incidents and routine tasks.

## Quick reference
| Symptom | First checks | Safe mitigations | Validation |
| --- | --- | --- | --- |
| Cannot activate tenant | missing plan or regions | Set plan and regions then retry activate | status is active |
| Wrong residency policy | policy id mismatch | Put corrected policy with effective_from today | policy reflected in GET |
| Stale cache downstream | change events not delivered | Re-publish last change or flush cache | downstream reflects change |

## Procedures

### 1. Onboard a new tenant
1. Create tenant with slug and legal name
2. Put regions and residency policy
3. Put plan with effective_from
4. Add contacts and external ids
5. Activate lifecycle

### 2. Suspend a tenant
1. Post lifecycle suspend with correlation id
2. Confirm status is suspended
3. Verify downstream services apply suspension

### 3. Correct regions
1. Read current regions
2. Put corrected region list
3. Confirm list and publish change

### 4. Update contacts
1. Get contacts
2. Replace with corrected list
3. Validate emails and roles

## Routine tasks
- Review tenants in draft older than threshold
- Audit contacts for completeness
- Reconcile external ids with billing

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Security](security.md)
