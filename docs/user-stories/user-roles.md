# User Roles & Responsibility Model

## Trust Boundaries & Planes

- **Control Plane (PHS + Host App):** Global governance, contracts, policy, identity, config, quotas, telemetry, evidence. High‑privilege actions are tightly scoped and audited.
- **Data Plane (Tenant Apps + Connectors + Workflow Engine):** Per‑tenant execution — ingestion, processing (Bronze → Silver → Gold → KPI), activation workflows. Blast radius confined to tenant.
- **Shared Services:** Secrets/KMS, IAM/RBAC directory, audit/evidence store, lineage/metadata, orchestration/scheduling.

**Principles:** least privilege, separation of duties, tenant isolation, explicit approvals for risk‑altering changes, immutable audit trails, break‑glass only with time‑boxed elevation.

## Personas

### Platform (Provider) Personas
- **PLATFORM OWNER** ultimate authority for platform posture and spend; approves risky global changes.
- **PLATFORM ADMIN** operates control plane; manages environments, quotas, global configs; no tenant data read.
- **SECURITY ADMIN** owns identity, RBAC, secrets/KMS, guardrails, vulnerability & compliance posture.
- **SCHEMA STEWARD** owns contracts (Raw/GDP/KPI); versioning, validations, rollout/rollback, impact notices.
- **KPI AUTHOR** defines KPI specs, thresholds, validation rules; no infra privileges.
- **WORKFLOW AUTHOR** authors activation templates, approvals, triggers, rollback behavior.
- **OBSERVABILITY/SRE** monitors reliability, costs, autoscaling; incident response; no business data edits.
- **COMPLIANCE OFFICER** configures evidence policies, retention, residency; read audit, no execution rights.
- **AUDITOR (Read‑only)** read‑only to logs, evidence, lineage; cannot change policy or data.

### Tenant (Customer) Personas
- **TENANT ADMIN** manages tenant users, source bindings, environment toggles; submits schema/KPI requests.
- **TENANT APPROVER** business approver for workflows, risky changes, and quota escalations.
- **BUSINESS OWNER (CFO/CGO/COO)** consumes packs, sets thresholds/targets, initiates governed actions.
- **DATA ENGINEER (Tenant)** manages connectors and mappings within tenant scope; no global configs.
- **ANALYST / VIEWER** reads KPIs, reports, evidence limited by RBAC; cannot change policy.
- **INTEGRATION OPERATOR** runs/backfills jobs, retries failed loads, manages replays under guardrails.

## Scope by Service (Allowed Actions)

| Service Area                    | Platform Owner | Platform Admin | Security Admin | Schema Steward | KPI Author | Workflow Author | SRE | Compliance | Auditor | Tenant Admin | Tenant Approver | Business Owner | Data Eng. (Tenant) | Analyst |
|---------------------------------|----------------|----------------|----------------|----------------|------------|-----------------|-----|------------|---------|--------------|-----------------|----------------|--------------------|---------|
| **PHS Control APIs**            | A              | M              | C              | C              | C          | C               | C   | R          | R       | R            | C               | R              | R                  | R       |
| **IAM/RBAC & KMS**              | A              | C              | M              | R              | R          | R               | R   | R          | R       | R            | C               | R              | R                  | R       |
| **Schema Services (Contracts)** | C              | C              | C              | M              | C          | R               | R   | R          | R       | R            | C               | R              | C                  | R       |
| **KPI Services**                | R              | C              | C              | C              | M          | R               | R   | R          | R       | R            | C               | C              | C                  | R       |
| **Activation/Workflows**        | C              | C              | C              | R              | C          | M               | R   | R          | R       | C            | A               | A              | C                  | R       |
| **Connectors & Ingestion**      | C              | A              | C              | C              | R          | R               | R   | R          | R       | M            | C               | R              | M                  | R       |
| **Observability/Cost**          | R              | M              | R              | R              | R          | R               | M   | R          | R       | R            | C               | R              | R                  | R       |
| **Evidence/Lineage**            | R              | R              | R              | R              | R          | R               | R   | M          | R       | R            | R               | R              | R                  | R       |

Legend: **M**=Manage, **A**=Approve, **C**=Configure, **R**=Read.

## Separation of Duties (SoD) Guardrails

- No single persona can draft **and** approve **and** deploy risk‑altering changes (schema, KPI, workflow, RBAC).
- **Security Admin** manages identities/secrets but cannot change business contracts or run workflows.
- **Schema Steward** and **KPI Author** cannot change infra; **SRE** cannot alter KPIs/contracts.
- **Tenant Admin** manages membership and sources; **Tenant Approver** signs off on triggers above risk thresholds.

## Common Permission Bundles (RBAC Profiles)

- **Platform‑Core:** Platform Admin + read to Security; no tenant data read.
- **Governance‑Author:** Schema Steward + KPI Author + Workflow Author; publish requires Approver.
- **Ops‑Run:** SRE + Integration Operator; can replay jobs, roll forward/back; cannot alter policy.
- **Tenant‑Business:** Tenant Admin + Tenant Approver + Business Owner; no control‑plane changes.

## Example Policy Snippets (Illustrative)

### Deny Cross‑Tenant Data Read (applies to all platform roles)
```json
{
  "Effect": "Deny",
  "Action": ["data:Read", "kpi:GetResults"],
  "Resource": ["tenant/*"],
  "Condition": {"StringNotEquals": {"tenant:context": "${aws:PrincipalTag/tenant_id}"}}
}
```

### Break‑Glass Elevation (time‑boxed, approval required)
```json
{
  "Effect": "Allow",
  "Action": ["workflow:Execute", "schema:Rollback"],
  "Resource": ["tenant/${tenant_id}/*"],
  "Condition": {
    "Bool": {"approval:ticket_open": true},
    "DateLessThan": {"aws:CurrentTime": "${now+2h}"}
  }
}
```

### Publish Requires Dual Control
```json
{
  "Effect": "Allow",
  "Action": ["schema:Publish", "kpi:Publish", "workflow:Publish"],
  "Resource": ["tenant/${tenant_id}/*"],
  "Condition": {"Bool": {"approval:dual_signed": true}}
}
```

## RACI for Core Activities

| Activity                      | Platform Admin | Security Admin | Schema Steward | KPI Author | Workflow Author | SRE   | Compliance | Tenant Admin | Tenant Approver | Business Owner |
|-------------------------------|----------------|----------------|----------------|------------|-----------------|-------|------------|--------------|-----------------|----------------|
| Provision Tenant              | **R**          | C              | I              | I          | I               | C     | I          | **A/R**      | I               | I              |
| Onboard Connector             | C              | C              | I              | I          | I               | **R** | I          | **A/R**      | I               | I              |
| Contract Change (Raw/GDP/KPI) | I              | C              | **R**          | C          | I               | I     | I          | C            | **A**           | I              |
| KPI Thresholds                | I              | I              | C              | **R**      | I               | I     | I          | C            | **A**           | **A**          |
| Workflow Template             | I              | I              | I              | C          | **R**           | I     | I          | C            | **A**           | **A**          |
| Incident Response             | I              | I              | I              | I          | I               | **R** | C          | I            | I               | I              |
| Evidence Export               | I              | I              | I              | I          | I               | I     | **R**      | C            | **A**           | A              |

Legend: **R**=Responsible, **A**=Accountable, **C**=Consulted, **I**=Informed.

## Usage in User Stories

Place this section at the start of **Platform User Stories**. Reference personas explicitly in each story step (e.g., *Tenant Admin submits schema change → Schema Steward publishes draft → Tenant Approver approves → SRE rolls out → Auditor verifies evidence*).
