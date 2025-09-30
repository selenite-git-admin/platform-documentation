# Platform User Stories

## Key Personas in Stories

**Platform (Provider):**  

- Platform Owner: Approves global/risky changes.
- Platform Admin: Manages control plane infra/config; no tenant data read.
- Security Admin: IAM, secrets/KMS, guardrails, compliance.
- Schema Steward: Owns Raw/GDP/KPI contracts.
- KPI Author: Defines KPI specs/thresholds.
- Workflow Author: Designs activation templates.
- Observability/SRE: Monitors costs/reliability, incident response.
- Compliance Officer: Evidence/retention config; no execution rights.
- Auditor (Read-only): Lineage, evidence, logs.

**Tenant (Customer):**  

- Tenant Admin: Manages users, sources, environment toggles.
- Tenant Approver: Approves workflows and risky changes.
- Business Owner (CFO/CGO/COO): Consumes packs, triggers governed actions.
- Tenant Data Engineer: Manages connectors/mappings in a tenant scope.
- Analyst/Viewer: Reads KPIs, reports under RBAC.
- Integration Operator: Retries jobs, replays data under guardrails.

[Reed more about roles...](user-roles.md) 

## Story Categories

### Platform Setup

- [Platform Infrastructure Deployment](00a-platform-infrastructure-deployment.md)  
- [Connector Deployment & Maintenance](00b-connector-deployment.md)  
- [Schema Templates Seeding](00c-schema-templates-seeding.md)  
- [Access & RBAC Baseline](00d-access-rbac-baseline.md)

### Tenant Lifecycle

- [Tenant Provisioning](01-tenant-provisioning.md)  
- [Tenant Infrastructure Provisioning](01b-tenant-infrastructure-provisioning.md)  
- [Tenant Decommissioning / Offboarding](01c-tenant-decommissioning.md)

### Data Onboarding

- [Data Source Onboarding](02-source-onboarding.md)  
- [Connector Handshake & Preflight](02b-connector-handshake-preflight.md)

### Governance & Enforcement

- [Setting Up Guardrails](04-guardrails-dqc.md)  
- [Evidence](05-evidence-lineage.md)  
- [Automated Housekeeping & Cost Controls](05b-housekeeping-cost-controls.md)

### Schema Lifecycles

- [Source (Raw) Schema Lifecycle](03a-raw-schema-lifecycle.md)  
- [GDP Schema Lifecycle](03b-gdp-schema-lifecycle.md)  
- [KPI Schema Lifecycle](03c-kpi-schema-lifecycle.md)  
- [Tenant Schema Change Request](03d-tenant-schema-change-request.md)  
- [Tenant-Specific Schema Extension](03e-tenant-specific-schema-extension.md)  
- [Safe Rollout & Rollback](03f-safe-rollout-rollback.md)  
- [Impact Analysis & Notifications](03g-impact-analysis-notifications.md)

### KPI Lifecycle

- [KPI Publishing](06-kpi-publishing.md)  
- [KPI Consumption](07-kpi-consumption.md)

### Data Action Workflows

- [Workflow Templates Seeding](08a-workflow-templates-seeding.md)  
- [Workflow Authoring & Configuration](08b-workflow-authoring-configuration.md)  
- [Triggers & Approvals](08c-triggers-approvals.md)  
- [Workflow Execution Engine](08d-workflow-execution-engine.md)  
- [Simulation / Dry-Run & Rollback](08e-simulation-rollback.md)  
- [Workflow Observability & Receipts](08f-workflow-observability-receipts.md)

### Operations & Improvement

- [Decision-Making](09-decision-audit.md)  
- [Evidence Export for Regulators](09b-evidence-export-regulators.md)  
- [Monitoring](10-observability-monitoring.md)  
- [Incident Handling](10b-incident-handling.md)  
- [Feedback](11-feedback.md)

### Extended Stories

- [CFO Consumption & Activation](12-cfo-consumption-activation.md)  
- [Ops Connector Failure & Recovery](13-ops-connector-failure-recovery.md)  
- [Hybrid Deployment for Regulated Tenant](14-hybrid-deployment.md)  
- [AI Actor-Assisted Decisioning](15-ai-actors-workflows.md)
- [Anomaly Engine Escalation](16-anomaly-engine.md)  
- [Anomaly Threshold Tuning](17-anomaly-tuning.md)  

Together, these stories provide a complete picture of the platform in operation: 
from setup and governance through KPI consumption, activation, exception handling, and compliance.
