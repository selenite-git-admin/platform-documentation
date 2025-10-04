# Governance and Guardrails for Runners

## Purpose
Define the governance model and guardrails that apply to runner selection and use in BareCount pipelines. Governance ensures that teams choose classes, sizes, and network profiles responsibly, while guardrails enforce compliance, cost discipline, and operational safety.

## Context
Runner classes provide flexibility. Without policy, teams may oversize, overspend, or expose data improperly. Governance establishes allowed choices per tenant, cost and network policies, and exception workflows. Guardrails are technical enforcements that prevent unsafe configurations from running.

## Governance Model
- **Tenant Policy**  
  Each tenant has an approved matrix of runner classes, sizes, and network profiles. Policies reflect data sensitivity, regulatory requirements, and budget.

- **Approval Workflow**  
  Requests for XLarge sizes, custom profiles, or dedicated compute require governance review and documented approval.

- **Policy Registry**  
  Allowed combinations are recorded in the platform Policy Registry and checked at pipeline deploy time.

- **Change Management**  
  Changes to policies follow the enterprise change process with testing in staging environments before production rollout.

## Guardrails

### Class and Size Limits
- Block use of XLarge profiles without approval
- Default to Medium for new workloads if size not declared
- Enforce maximum concurrency caps per tenant

### Network Profiles
- Validate declared network_profile against tenant policy
- Block public egress when private connectivity exists
- Require DNS validation for PrivateLink and VPN endpoints
- Deny on premise agent without explicit residency requirement

### Cost Controls
- Tag runs by class, size, tenant, and pipeline for chargeback
- Quotas on monthly runtime hours per class and tenant
- Alerts on sustained over provisioning or idle hosts
- Deny runs that exceed quota without governance override

### Security
- All secrets must come from platform secrets service
- Images and drivers must be from approved registries
- Vulnerability scans required before deploy
- Access logs and Evidence entries are mandatory for all runs

### Operational Safety
- Health checks before job start on dedicated compute
- Automatic retries with capped budgets
- Dead letter queue for failed events or partitions
- Enforced run timeouts per class to avoid runaway costs

## Exception Handling
- Exception requests must include business justification, risk analysis, and cost plan
- Temporary approvals expire and must be renewed
- Evidence entries record approver, reason, and expiration

## Evidence Requirements
Every run must write Evidence including
- Runner class, size, and network profile
- Image or driver versions
- Secrets used by reference, not value
- Policy checks applied and passed
- Approvals attached for exceptions

## Observability
- Dashboards show usage by class, size, and tenant
- Alerts fire when usage exceeds policy or when denied runs occur
- Governance teams review trends monthly for optimization
- Evidence ledger is the source of truth for audit

## Notes
Governance ensures runner flexibility does not compromise compliance or cost. Guardrails prevent unsafe or expensive runs from starting. Together they make runner selection predictable, auditable, and aligned with enterprise risk posture.
