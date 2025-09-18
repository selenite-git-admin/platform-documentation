# Platform Services Infrastructure

Platform Services Infrastructure defines how PHS is provisioned and operated on AWS.  
It provides the baseline environment for contracts, shared services, and enforcement before any tenant or business workload is onboarded.

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/phs-infrastructure/phs-infra.svg" alt="Platform Services Infrastructure Conceptual Diagram">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/phs-infrastructure/phs-infra.svg" alt="Platform Services Infrastructure Conceptual Diagram">
</div>

_Figure 1: Platform Services Infrastructure Conceptual Diagram_{.figure-caption}


## Deployment Model
- **Infrastructure as Code**: AWS CDK defines all stacks.  
- **Pipeline**: CICD pipelines deploy PHS; changes are PR-driven and traceable.  
- **Accounts**: PHS runs in a dedicated AWS account under the Platform Super Admin.  
- **Guardrails**:  
  - No manual console edits.  
  - All changes are logged and auditable.  
  - IAM roles with the least privilege.  

## Components
Provisioned as part of PHS infrastructure:
- VPC, subnets, routing, and security groups.  
- Core metadata databases (for contracts, lineage, audit).  
- Secrets Manager + KMS for credentials and encryption keys.  
- Observability stack (CloudWatch, X-Ray, or equivalent).  
- CICD hooks for Admin Host App deployment.  
- Logging/audit trail foundations (CloudTrail, GuardDuty).  
- Outbound egress controls for connectors.  

## Security
- Only the **Platform Super Admin** can deploy or modify infrastructure.  
- CLI/CDK/MFA enforced; no UI access.  
- Secrets are stored centrally; keys rotated automatically.  
- Audit logs linked to Git commit IDs and pipeline runs.  

## Readiness for Admin Host App
The end state of platform infrastructure is readiness to deploy the **Admin Host App**.  
The Admin Host App will then:  
- Provision, monitor, and manage **tenant lifecycles**.  
- Manage **contract lifecycles** (seeding, modifying, approval → publish to PHS).  
- Provide visibility into PHS health (via observability APIs).  
It does **not** provision or mutate PHS itself; infra remains controlled by Super Admin via CDK/CICD.  
