# Tenancy Module Security

**Audience:** Platform engineering, DevOps, and infrastructure security teams  
**Status:** Working draft  
**Purpose:** Define the operational and architectural security model for the Tenancy module. This document establishes access control, encryption, secret handling, network isolation, and audit architecture. It merges Tenant Management security definitions with Tenancy runtime controls. Compliance mappings are intentionally excluded and documented separately.

## Security Objectives

- Protect tenant data confidentiality, integrity, and availability.  
- Enforce least privilege across all identities and components.  
- Ensure deterministic encryption and auditable access for every tenant resource.  
- Maintain isolation boundaries across tenants at compute, network, and data levels.  
- Provide complete traceability of privileged actions.

## Core Principles

1. Zero trust across service boundaries.  
2. No shared credentials between components.  
3. Tenant-specific keys and identity separation.  
4. Automatic key rotation and secret renewal.  
5. Immutable audit trail for all mutating actions.  
6. Fail closed on policy or permission validation errors.

## Identity And Access Management

**Roles and boundaries**
```yaml
iam:
  roles:
    tenancyControllerRole: arn:aws:iam::111111111111:role/tenancy-controller
    registryRole: arn:aws:iam::111111111111:role/tenancy-registry
    webhookRole: arn:aws:iam::111111111111:role/tenancy-webhook
    policyRole: arn:aws:iam::111111111111:role/tenancy-policy-service
  boundaries:
    allowActions:
      - rds:*
      - kms:Encrypt
      - kms:Decrypt
      - secretsmanager:GetSecretValue
      - logs:PutLogEvents
      - sqs:SendMessage
      - sns:Publish
    denyActions:
      - s3:DeleteBucket
      - iam:CreateRole
      - iam:AttachRolePolicy
```

**Least privilege enforcement**
- Each component runs under its own IAM role.  
- No service uses instance profiles with broad privileges.  
- All IAM policies are managed as code and version controlled.  
- Actions not explicitly allowed are denied.  
- Roles are assumed only for specific task duration through STS.  

**Scoped access**
- Controller assumes the registry role only for metadata updates.  
- Webhook worker assumes webhook role only when dispatching events.  
- Audit service operates with write-only access to the audit log stream.  

## Authentication And Authorization

- Authentication uses short-lived OAuth 2.0 tokens issued by the Access service.  
- Tokens are scoped to tenant or environment and contain allowed actions.  
- Internal service-to-service calls rely on signed JWTs with workload identity trust.  
- Authorization is enforced through policy evaluation before any write.  
- Each action is validated against residency, plan, and role policies.  

**Policy hooks**
- Residency policy controls region selection and placement.  
- Encryption policy enforces key type and rotation interval.  
- Action policy restricts lifecycle operations and administrative actions.  

## Encryption And Key Management

**Hierarchy**
```yaml
encryption:
  kms:
    masterKeyRef: kms://keys/tenancy-master
    rotationDays: 90
    perTenantKeys:
      enabled: true
      templateRef: kms://templates/per-tenant
    auditLogKeyRef: kms://keys/audit-log
```

**Encryption model**
- All persistent data (registry, metadata, and configuration) is encrypted at rest using KMS.  
- Each tenant may use a dedicated key derived from the master tenancy key template.  
- Cross-region replication uses re-encryption on target KMS key.  
- Secrets, webhook payloads, and plan definitions use envelope encryption.  
- Audit logs use a dedicated key for forward secrecy.  

**Key rotation**
- Automatic rotation every 90 days for shared keys.  
- Per-tenant keys rotated during lifecycle state change (e.g., Activate or Renew).  
- Manual rotation triggers background re-encryption job validated by checksum.  

**Operational controls**
- Keys are created by the platform provisioning service.  
- KMS grants are scoped to component IAM roles only.  
- No direct console access to KMS operations.  
- Failed decrypt attempts are logged as security events.

## Secrets Management

**Provider**
```yaml
secrets:
  provider: aws-secrets-manager
  rotation:
    enabled: true
    intervalDays: 30
  namespaces:
    tenancyController: secret://tenancy/controller
    webhookSigning: secret://tenancy/webhooks/signing
    apiTokens: secret://tenancy/api/tokens
    dbCredentials: secret://tenancy/db/credentials
```

**Handling rules**
- Secrets are never stored in manifests or logs.  
- Secret access is programmatic through provider SDKs only.  
- Secrets are versioned, rotated, and audited.  
- Rotation scripts publish success metrics and error alerts.  
- Rollback to previous secret version is permitted only for recovery.  

**Reference pattern**
```yaml
webhooks:
  signingKeyRef: secret://tenancy/webhooks/signing
database:
  credentialsRef: secret://tenancy/db/credentials
```

## Network And Isolation

**Boundary types**
- VPC isolation by environment (prod, staging, dev).  
- Dedicated subnet tiers for control plane and data plane.  
- Network ACLs deny east-west traffic between tenant database clusters.  
- Security groups restrict component communication strictly to necessary ports.  
- Private subnets enforce all controller-to-registry traffic over TLS.  

**Ingress and egress**
- API Gateway terminates TLS 1.2+ with automatic certificate rotation.  
- Webhook endpoints restricted by allowed domain patterns.  
- Outbound internet access blocked except for specific integrations.  

**Isolation strategies**
```yaml
isolation:
  database:
    modes:
      - schemaPerTenant
      - dedicatedDatabase
  network:
    modes:
      - sharedVpc
      - dedicatedVpc
```

Isolation policies are validated by control plane before any provisioning. Dedicated mode enforces unique subnet and KMS key combination per tenant.

## Audit And Logging

**Audit events**
- Every create, update, delete, or lifecycle action emits an audit record.  
- Records include actor id, tenant id, action, request id, correlation id, timestamp, and outcome.  
- Immutable storage with write-once semantics using append-only log stream.  
- Tampering attempts trigger alerts.

**Log management**
```yaml
logging:
  format: json
  include:
    - timestamp
    - level
    - actor
    - tenantId
    - action
    - requestId
    - correlationId
  sampling:
    error: always
    info: 0.3
```

Audit logs are stored in a separate encrypted bucket with restricted read access. Retention is 180 days with lifecycle transition to cold storage.

## Security Event Monitoring

- Continuous CloudTrail integration captures API usage and KMS operations.  
- Failed policy evaluations are flagged as security events.  
- Unauthorized role assumption attempts generate alerts.  
- DLQ messages with specific error codes (AccessDenied, KMSFailure) are auto-categorized as security anomalies.  
- Weekly reports summarize anomalies by category and actor.

## Key Rotation And Revocation

**Process**
1. Generate new key version.  
2. Update component grants and re-encrypt data.  
3. Verify decryption success.  
4. Mark previous key as pending deletion after grace period.  
5. Update audit log with rotation summary.

**Triggers**
- Scheduled rotation.  
- Lifecycle transition event.  
- Manual rotation request after compromise detection.  

**Revocation**
- Immediate disablement of compromised keys.  
- Forced policy evaluation on tenants referencing revoked key.  
- Alert SREs and trigger incident response workflow.

## Administrative Overrides

**Safeguards**
- Admin overrides require justification and audit note.  
- Temporary IAM policy with TTL attached to performing user.  
- Automatic expiration and removal after window ends.  
- All admin overrides are logged with actor and reason.  

**Examples**
- Emergency read of registry for incident resolution.  
- Forced webhook requeue when automated retry disabled.  
- Temporary disablement of policy enforcement for recovery.

## Security Automation

**Automated checks**
- Validate IAM role trust policies weekly.  
- Verify secret rotation scripts executed successfully.  
- Scan for unused KMS keys and revoke stale grants.  
- Detect hardcoded credentials using static analysis in CI/CD.  
- Check network ACL and SG drift nightly.

**Continuous validation**
- Security Lambda validates configuration drift.  
- Policy service audits residency, encryption, and action policies continuously.  
- Unauthorized API requests blocked by gateway before reaching controller.

## Verification And Testing

**Periodic validation**
- Quarterly penetration test on tenancy control plane.  
- Monthly IAM simulation test to validate boundaries.  
- Weekly automated KMS access review.  
- Daily secret access diff report against allowed patterns.

**Pre-deployment checks**
- Static analysis for open security groups and overly permissive IAM.  
- Enforced review of all new IAM roles.  
- CI/CD validation for manifest and configuration integrity.

## Security Recovery Procedures

**Compromised key**
- Rotate immediately and re-encrypt affected data.  
- Invalidate dependent session tokens.  
- Notify affected tenants if policy mandates.

**Leaked secret**
- Revoke immediately and regenerate secret.  
- Identify dependent workloads using access logs.  
- Audit all access during compromise window.

**Unexpected privilege escalation**
- Disable suspect role.  
- Roll back IAM policy to last known good version.  
- Investigate CloudTrail and audit logs.

**Data exposure event**
- Trigger incident response playbook.  
- Rotate affected keys and secrets.  
- Validate data integrity and system state.  

## Validation And Hardening Checklist

- [ ] IAM roles scoped per component and tenant.  
- [ ] KMS keys rotated within 90 days.  
- [ ] Secrets rotated within 30 days.  
- [ ] Audit logs immutable and reviewed weekly.  
- [ ] Network isolation validated per tenant.  
- [ ] Admin overrides audited and expired.  
- [ ] Static analysis for credentials clean.  
- [ ] TLS enforced on all connections.  
- [ ] Error messages sanitized of sensitive data.

## Summary

The Tenancy security architecture implements a defense-in-depth model spanning identity, encryption, secrets, isolation, and audit. All components operate with least privilege and predictable key lifecycles. Every sensitive operation is both authenticated and authorized by policy evaluation, producing immutable audit artifacts. Security automation and validation ensure sustained compliance with the architectural baseline and reduce mean time to detect and respond to incidents.