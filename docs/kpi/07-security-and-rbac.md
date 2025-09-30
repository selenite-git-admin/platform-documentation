# Security and RBAC

## Purpose
Protect metric data and APIs.
Apply least privilege and audit access.

## Data classes
Classify data by sensitivity.
Apply controls per class.

## Scopes and tokens
Issue scoped tokens for APIs.
Rotate and revoke tokens with policy.

## Row level security
Apply RLS for multi tenant views.
Document scope resolution.

## Audit logs
Record who read what and when.
Link to evidence records for runs and releases.

## Legacy content
The following section is imported from legacy security.

# Kpi Security
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Define security and compliance controls for the KPI System.  
- Scope: Includes authN/Z, secrets, data protection, auditing. Excludes corporate SOC processes.  
- Target Readers: Security engineers, platform owners, auditors.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Security Framework (Policy-Level)

## Purpose
Define how platform-wide infrastructure security and tenant-specific data access are governed for KPIs.  
Platform owns physical & infra security; each tenant owns data security policy (sensitivity, access control, masking, exports).

## Shared Responsibility Model

- Platform (Cxofacts)
  - Network/VPC, KMS keys custody, backups, infra logs (CloudWatch), secrets (AWS Secrets Manager).
  - Multi-tenant isolation (per-tenant schema/DB or RLS), service identities (IAM roles), TLS, API Gateway auth.
- Tenant
  - Sensitivity classification per KPI (`public|internal|restricted|confidential`).
  - Access control (who can read/run/export; entity/time-grain scope; allowed extensions).
  - Data handling (masking, aggregation thresholds, SCD view restrictions).
  - Admin controls (who can publish/pause/rollback within tenant).

## Policy-as-Data (AWS-IAM style)

Tenant security is expressed as declarative policies (JSON/Cedar/Rego), versioned per tenant and enforced at runtime.

### Resources
- `kpi:{kpi_id}` (optionally `{kpi_id}:{contract_version}`)
- Packs/folders, KPI result slices (entity/time-grain), admin ops

### Actions
- `kpi:Run`, `kpi:Read`, `kpi:Export`, `kpi:Admin`, `kpi:Inspect`

### Attributes (ABAC)
- User: roles, groups, dept, region, tenant
- KPI: sensitivity, layer, owners
- Slice: entity scope, geography, time-grain, extensions, scd_view
- Env/Op: env(`dev|stg|prod`), export_format

## Example Policy (IAM-flavored JSON)

```json
{
  "Version": "2025-08-01",
  "Tenant": "acme-corp",
  "Statements": [
    {
      "Sid": "AllowFinanceToReadInternalKPIs",
      "Effect": "Allow",
      "Action": ["kpi:Read"],
      "Resource": ["kpi:*"],
      "Condition": {
        "kpi:sensitivity": ["public","internal"],
        "user:roles": ["Finance","Ops"],
        "env:environment": ["prod"]
      }
    },
    {
      "Sid": "RestrictConfidentialToCFO",
      "Effect": "Allow",
      "Action": ["kpi:Read","kpi:Run","kpi:Export"],
      "Resource": ["kpi:*"],
      "Condition": {
        "kpi:sensitivity": ["confidential"],
        "user:roles": ["CFOOffice"]
      }
    },
    {
      "Sid": "EntityScopeByRegion",
      "Effect": "Allow",
      "Action": ["kpi:Read","kpi:Run"],
      "Resource": ["kpi:LiquidityRatio","kpi:DSO"],
      "Condition": {
        "data:entity_region": ["APAC","EMEA"],
        "user:region": ["APAC"]
      }
    },
    {
      "Sid": "MaskingOnExports",
      "Effect": "Allow",
      "Action": ["kpi:Export"],
      "Resource": ["kpi:*"],
      "Condition": {
        "data:export_format": ["csv","xlsx"],
        "kpi:masking_policy": ["hash_account_numbers","suppress_small_segments"]
      }
    },
    {
      "Sid": "PlatformGuardrailNoCrossTenant",
      "Effect": "Deny",
      "Action": ["kpi:*"],
      "Resource": ["kpi:*"],
      "Condition": { "user:tenant": [{ "neq": "resource:tenant" }] }
    }
  ]
}
```

## Cedar (AWS Verified Permissions) Example

```cedar
// Actions
permit(principal, action, resource)
when { action in [kpi::Read, kpi::Run] };

// Confidential KPI only to CFOOffice
permit(principal, action, resource)
when {
  resource.sensitivity == "confidential" &&
  "CFOOffice" in principal.roles &&
  action in [kpi::Read, kpi::Run, kpi::Export]
};
```

## Rego (OPA) Snippet

```rego
package kpi.authz

default allow = false

allow {
  input.action == "kpi:Read"
  some role
  role := input.user.roles[_]
  role == "Finance"
  input.kpi.sensitivity == "internal"
  input.env == "prod"
}
```

## Enforcement Points (Runtime)

1) AuthN (OIDC/Cognito) → resolve user → tenant, roles, attrs.  
2) Policy eval (Lambda authorizer / Verified Permissions / OPA) → Allow/Deny + obligations (masking, filters, grain caps).  
3) Query shaping (KPI Call engine) → apply RLS filters, masking, extension & grain limits.  
4) Response meta → echo policy version, KPI contract version, applied masking.  
5) Audit → log allow/deny decision, policy SID, user, KPI, slice to tenant-scoped logs.

## Masking & Aggregation (Obligations)

- Field masking (hash/redact), value bucketing, k-anonymity (suppress groups < N).  
- Grain control (deny `day` for external viewers, allow `month+`).  
- Extension control (allow `benchmark`, deny `entity=legal_entity`, etc.).  
- Export control (on-screen view allowed, export denied).

## Admin Dashboard Integration

- Policy templates (Finance Standard, External Auditor, CFO Confidential).  
- Policy editor with linting + unit tests; simulate decisions before saving.  
- Change Requests & approvals; policy version catalog; break-glass temporary grants.

## Storage & Versioning

- Policy store per tenant (DynamoDB or AWS Verified Permissions).  
- Versioned documents; every KPI run logs which policy version was enforced.

## Diagrams (Placeholders)

- Security Flow → `../assets/diagrams/kpi-security-flow.svg`  
- Policy Evaluation Context → `../assets/diagrams/kpi-policy-context.svg`

## Why It Matters

- Separation of concerns: platform secures infra; tenants control data access.  
- Least privilege by default; explicit obligations applied.  
- Auditable: allow/deny + masking logged against policy version.  
- Portable: start with OPA; graduate to AWS Verified Permissions.  
- Composable: integrates with Lifecycle, Versioning, Admin Dashboard, SLA, Monitoring.

## Diagrams

None

## Tables

None



## Glossary

None
