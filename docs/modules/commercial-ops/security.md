# Security

## Overview

This document defines the security controls for the Commercial-Ops module. It covers identity and access management, tenant isolation, data protection, network boundaries, audit, and incident response. The design assumes AWS native services with Aurora as the main database for operator data and Aurora or equivalent for tenant business data. Currency defaults to USD. Canonical terms are tenant and plan.

## Security Objectives

- Protect tenant data with strong isolation at network and data layers
- Enforce least privilege across services and environments
- Provide continuous audit trails for financial and administrative actions
- Meet enterprise requirements for retention, backup, recovery, and compliance
- Support secure multi-tenancy without exposing AWS internals to tenants

## Data Classification

| Class | Description | Examples | Protection |
|------|-------------|----------|-----------|
| Public | Safe for publication | Product docs | Standard controls |
| Internal | Operational metadata | Plan caps, allocation rules | IAM scoped, audit events |
| Sensitive | Tenant usage and invoices | usage_snapshot_daily, invoice_detail | KMS encryption, strict IAM |
| Regulated | PII or bank refs | Billing contact names, IBAN reference | KMS CMK, tokenization or redaction, access approvals |

PII storage is minimized. No secrets or full payment instrument data are stored. Payment provider references are used instead.

## Identity and Access Management

### Roles and Personas

| Persona | Access Scope | Typical Actions |
|--------|---------------|-----------------|
| Tenant admin | Own tenant resources | View dashboards, download invoices, manage seats |
| Operator billing | All tenants but limited write | Adjust invoices, process payments, run reconciliation |
| Operator platform | Infrastructure and pipelines | CUR ingestion, allocation jobs, tagging validators |
| Auditor | Read-only evidence | Export recon reports, audit trails |

### IAM Principles

- Each Lambda, ECS task, and job has a dedicated IAM role
- Deny by default and grant least privilege with resource-level constraints
- Access to Aurora uses IAM auth or short-lived credentials via Secrets Manager
- Cross-account CUR read uses an external ID and a dedicated role in payer account

### Example IAM Policy: CUR Reader

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AthenaRead",
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryResults",
        "glue:GetTable",
        "glue:GetDatabase"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3CURRead",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::payer-cur-bucket",
        "arn:aws:s3:::payer-cur-bucket/*"
      ]
    }
  ]
}
```

### Service Control Policy guardrails (examples)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyPublicS3",
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "*",
      "Condition": {
        "Bool": { "aws:SecureTransport": "false" }
      }
    },
    {
      "Sid": "DenyIAMUser",
      "Effect": "Deny",
      "Action": "iam:*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": { "aws:PrincipalArn": "arn:aws:iam::<account>:role/*" }
      }
    }
  ]
}
```

## Authentication and Authorization

- Tenant and operator SSO via OIDC or SAML2 (IdP integration recommended)
- Access tokens are JWT with short TTL and audience checks
- Role based access control layered with attribute checks: tenant_id, plan_code, environment
- Fine grained grants inside Aurora using database roles for read vs write

### API Authorization Checks

```pseudo
if request.tenant_id != token.tenant_id and not token.has_scope("operator"):
    deny("forbidden")
if path.includes("invoice") and not scope.contains("invoice:read"):
    deny("insufficient_scope")
```

## Tenant Isolation

| Layer | Control | Notes |
|------|---------|------|
| Network | VPC segmentation, separate subnets for data plane and control plane | Security groups follow least privilege |
| Data | Row level permissions by tenant_id | Enforced in API layer; optional PostgreSQL RLS |
| Compute | Dedicated runner instances per tenant when required | Always on runners tagged with tenant_id |
| Cost | Tags `user:tenant_id` and `user:plan_id` | Validated daily |

Cross tenant queries are blocked by API policy and database role mapping. Batch exports are prefiltered by tenant_id.

## Network Security

- Private subnets for databases
- NAT Gateway or PrivateLink for outbound access to AWS services
- VPC endpoints for S3, Secrets Manager, KMS, CloudWatch Logs
- TLS required end to end, with modern ciphers only
- Security groups restrict inbound to load balancers and endpoints only

### Example Security Group policy fragment

```bash
aws ec2 authorize-security-group-ingress   --group-id sg-abc123   --protocol tcp --port 5432   --source-group sg-app-lambda
```

## Encryption and Key Management

| Scope | Control | KMS Key | Rotation |
|------|---------|---------|----------|
| Data at rest (Aurora) | Encrypted storage | CMK `alias/commercial-ops-db` | Annual rotation |
| S3 buckets (CUR and evidence) | S3 SSE-KMS | CMK `alias/commercial-ops-evidence` | Annual rotation |
| Secrets | AWS Secrets Manager | KMS default or CMK | 30 to 90 days rotation |
| In transit | TLS 1.2+ | N/A | Enforced by ALB and SDKs |

### KMS Key policy baseline

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnableRootPermissions",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::<account>:root"},
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "AllowKeyUseFromApps",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::<account>:role/app-*"},
      "Action": ["kms:Encrypt","kms:Decrypt","kms:GenerateDataKey*"],
      "Resource": "*",
      "Condition": {"StringEquals": {"kms:ViaService": "rds.<region>.amazonaws.com"}}
    }
  ]
}
```

## Secrets Management

- Store credentials in AWS Secrets Manager with rotation Lambdas
- Do not embed secrets in environment variables or code
- Grant retrieval rights only to runtime roles that need them
- Use Parameter Store for non-secret configuration

## Logging and Audit

- Structured JSON logs with correlation IDs and tenant_id attributes
- Audit events recorded in `audit_event` for every financial action
- CloudTrail enabled on all accounts and regions
- Log retention 90 days hot, 365 days cold for ops; evidence kept 24 months minimum

### Audit Event schema reminder

| Field | Description |
|------|-------------|
| actor_type | system, tenant_user, operator_user |
| action | invoice_issue, payment_capture, plan_change |
| object_type | invoice, payment, plan, tenant |
| object_id | entity identifier |
| metadata | context including evidence links |

## Backup and Recovery

- Aurora automated backups with PITR enabled
- Daily logical dumps of financial tables to S3 with KMS
- Restore drills at least quarterly
- Evidence bundles export reconciliation inputs and SQL to S3 for each month

## Vulnerability and Patch Management

- Weekly ECR image scans for containers
- Lambda runtimes updated quarterly
- Dependency checks in CI with fail on critical issues
- Third party libraries tracked with SBOM manifests

## Change Management

- Infrastructure as code for all resources
- Two person review for IAM, KMS, network changes
- Tag schema changes require finance and platform approval
- Production changes logged in `audit_event` and change tickets

## Incident Response

| Phase | Action | Owner |
|------|--------|-------|
| Detect | Alert triggers from Observability | On call |
| Triage | Classify severity and affected tenants | On call + billing ops |
| Contain | Disable risky access, rotate secrets | Platform |
| Eradicate | Patch systems, fix configuration | Platform |
| Recover | Restore service, verify evidence | Platform + finance |
| Review | Postmortem within 48 hours | Incident owner |

### Communication

- Tenants are notified for security incidents that affect their data
- Regulator or contractual notifications follow legal guidance
- All external communication approved by leadership

## Compliance Considerations

- SOC 2 style controls: access review, change control, incident response
- PCI DSS not in scope unless card data is processed directly
- GDPR considerations for PII: DSR handling, data minimization, regional storage on request
- Data retention policies documented per table and S3 bucket

## Validation Checklist

- IAM roles have least privilege and scoped resources
- KMS CMKs used for all at rest storage and evidence
- VPC endpoints in place for S3, Secrets Manager, KMS, CloudWatch
- Row level or API level tenant isolation enforced
- CloudTrail and audit_event capture critical actions
- Backups and restores verified by drill
- Alarms in place for CUR freshness, allocation variance, tag coverage, invoice lag

## Cross References

- data-model.md for table contracts and audit_event
- observability.md for alerts and evidence
- aws-cost-integration/tag-strategy.md for tag governance
- aws-cost-integration/troubleshooting.md for recovery steps
- runbook.md for operational procedures
