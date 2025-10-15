# Ticketing Security

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Defines the security posture for the **platform‑scoped Ticketing Service**, which centralizes incident and request handling across all tenants. The objective is to preserve tenant privacy through strict access control and governance, while maintaining shared operational visibility for the platform team.

## Trust Model
- Ticketing is a **shared service**, not tenant-isolated. Logical separation is enforced by **RBAC** and **query-level scoping**.
- Platform operators can view and act on all tickets; tenant users can access only their own scope.
- Attachments and comments are sanitized for safe exposure.

## Authentication
- **Service‑to‑Service:** AWS IAM roles (Lambda, EventBridge, Notifications, Health).  
- **Human Users:** OAuth2/SSO via central Authentication service.  
- **Token Propagation:** JWT claims (`role`, `tenant_id`) validated by API Gateway authorizer.

## Authorization (RBAC)
| Role | Scope | Description |
|------|--------|-------------|
| `platform_admin` | global | Full CRUD, manage routing, SLA, escalation rules |
| `platform_operator` | global | Manage and triage all tickets |
| `tenant_user` | tenant | CRUD only within their tenant scope |
| `tenant_manager` | tenant | Assign and comment within tenant scope |
| `automation_service` | limited | Create/update tickets for system alerts |
| `readonly_auditor` | global | Read-only access, no modifications |

### Enforcement
- API Gateway injects claims → backend Lambda applies scoping filters.  
- PostgreSQL Row‑Level Security (RLS) optional for defense-in-depth.  
- Example predicate:
  ```sql
  (tenant_id = current_setting('app.tenant_id') OR visibility = 'platform_only')
  ```

## Data Protection
### Database (PostgreSQL)
- Encrypted at rest (KMS AES‑256).  
- Immutable audit trail (`ticket_history`, `ticket_comment`).  
- Redaction applied on write for sensitive content.  
- Point‑in‑time recovery enabled.  

### Object Storage (S3)
- Bucket prefix model: `s3://ticketing/attachments/<tenant_id>/`  
- SSE‑KMS encryption; optional tenant‑specific keys.  
- Signed URLs valid for ≤5 minutes.  
- Server-side validation prevents cross‑tenant access.

### In‑Transit Protection
- TLS 1.2+ enforced.  
- HMAC‑SHA256 signed webhooks with timestamp validation (≤ 5 min replay window).  
- JSON schema validation on API Gateway.

## Secrets Management
- AWS Secrets Manager for API keys and webhook tokens.  
- Access via Lambda IAM role only.  
- Automatic rotation every 90 days.

## Logging and Audit
- CloudWatch + OpenTelemetry for structured logs and distributed traces.  
- Sensitive fields masked.  
- Every state transition mirrored to Evidence Ledger.  
- Audit fields: `actor`, `action`, `timestamp`, `old_state`, `new_state`, `correlation_id`.

## Data Retention and Deletion
- Tickets: 24 months retention.  
- Attachments: 180 days unless linked to Evidence Ledger.  
- Ledger records immutable.  
- PII redaction on user deletion requests.

## Network Security
- Public endpoints: via API Gateway (tenant traffic).  
- Private routes: VPC-only for bulk imports, admin tasks.  
- VPC endpoints for RDS, S3, Secrets Manager, SQS.  
- Security groups follow least-privilege principle.

## Compliance Alignment
- **ISO 27001:** Access control, encryption, auditability.  
- **SOC 2:** Logical isolation, monitoring, and change control.  
- **GDPR:** Data minimization and right to erasure via field redaction.

## Incident Response
1. Detect anomaly via GuardDuty/SIEM.  
2. Suspend affected credentials or role.  
3. Quarantine suspicious tickets/attachments.  
4. Verify audit and Ledger entries.  
5. Rotate secrets, keys, tokens.  
6. Publish incident report within 48 hours.

## Security Testing
- Static scans in CI/CD (Bandit, Checkov).  
- Weekly dynamic API scans.  
- Quarterly penetration testing.  
- CloudFormation linted with cfn‑nag and IAM Access Analyzer.

## Summary
Ticketing runs as a platform‑wide service with logically enforced isolation through RBAC and RLS. All data paths are encrypted, every state change auditable, and operational access tightly governed.