# Dataset Refresh Registry (DRR) Security

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Objective
DRR manages operational metadata that determines dataset readiness and visibility across tenants. Security ensures data integrity, tenant isolation, and controlled system access without compromising performance.

## Security Model
The DRR security framework follows a zero-trust, least-privilege model implemented through five layers:

| Layer | Control | Purpose |
|--------|----------|----------|
| Network | VPC isolation, private subnets, security groups | Restrict access to internal APIs and database endpoints |
| Identity | Service accounts, short-lived JWT tokens | Authenticate both internal and external actors |
| Authorization | Role- and tenant-based policy | Control who can read or write dataset state |
| Data access | Row-Level Security (RLS), schema separation | Enforce tenant isolation and ownership integrity |
| Audit | Immutable logs and evidence correlation | Guarantee traceability for all state changes |

## Authentication
- All external consumers authenticate via OAuth2 JWT issued by the platform Identity service.  
- Internal services (Runtime, Storage Catalog) use machine-to-machine (M2M) tokens with scoped claims.  
- Tokens include: `sub`, `tenant_id`, `role`, `scope`, `iat`, `exp`.  
- Maximum token TTL: 1 hour for M2M, 15 minutes for user tokens.  

### Token Scopes
| Scope | Description |
|--------|--------------|
| `storage.read.refresh` | Read-only access to freshness APIs |
| `storage.write.refresh` | Internal writer role for Runtime |
| `storage.read.audit` | Restricted read for Evidence Ledger linkage |

## Authorization
DRR uses a hybrid RBAC + RLS model.

### RBAC
| Role | Permissions |
|-------|--------------|
| `reader` | GET `/storage/v1/datasets/*` endpoints |
| `runtime-writer` | POST `/storage-internal/v1/datasets/*/refresh-state` |
| `auditor` | SELECT access to freshness metadata via internal interface |

### RLS Enforcement
- Enforced on `dataset_refresh_state`, `dataset_run_log`, and `dataset_registry`.  
- Policy example:
```sql
CREATE POLICY tenant_isolation ON dataset_refresh_state
  USING (tenant_id = current_setting('app.tenant_id')::text);
```
- The application sets `app.tenant_id` context before query execution.  
- All read queries automatically filter by tenant context.  

### Schema Separation
- Each environment (dev, staging, prod) uses distinct logical schema.  
- Metadata tables stored in `storage_drr` schema; no direct joins to business data.  

## Secrets Management
- Secrets stored in AWS Secrets Manager with automatic rotation.  
- Database credentials rotated every 90 days.  
- M2M tokens issued dynamically and never hard-coded.  
- No secret values logged; only masked identifiers (`****`).  

## Data Encryption
| Type | Mechanism | Notes |
|------|------------|-------|
| In transit | TLS 1.3 | Enforced on all APIs and DB connections |
| At rest | AES-256 | Enabled on EBS and RDS volumes |
| Token | Signed with RS256 | Verified with platform public key |
| Event stream | KMS envelope encryption | Runtime → DRR event transport |

## Audit and Evidence
- Every API call generates an audit event with correlation ID.  
- Audit payload includes: `timestamp`, `actor_id`, `tenant_id`, `action`, `dataset_id`, `result`.  
- Audit trail is immutable and linked to Evidence Ledger by correlation ID.  
- Retention: 365 days for audit logs, 7 years for evidence snapshots.  

## Compliance Alignment
| Standard | Mapping |
|-----------|----------|
| ISO 27001 | Access control, audit logging, encryption |
| SOC 2 Type II | Availability and confidentiality controls |
| GDPR | Pseudonymization and data minimization (no PII stored) |
| HIPAA (conditional) | Applicable when DRR supports PHI metadata tracking |

## Threat Controls
| Threat | Mitigation |
|---------|-------------|
| Token theft | Short TTL + rotating signing keys |
| Cross-tenant read | Strict RLS enforcement and audit detection |
| Injection attacks | Parameterized queries and ORM-level validation |
| Replay attack | Idempotency-Key validation and nonce tracking |
| Insider modification | Write limited to service accounts + Evidence Ledger linkage |
| DB corruption | WAL-based replication and immutable backups |

## Security Monitoring
- Security events forwarded to SIEM with daily correlation reports.  
- Anomalous activity triggers auto-block rules in the API Gateway.  
- Unauthorized schema changes monitored via `pg_event_trigger`.  
- Key metrics: token validation failures, policy evaluation errors, RLS anomalies.  

## Incident Response
| Step | Action |
|------|--------|
| 1 | Contain access by disabling tokens and isolating DB writer role |
| 2 | Identify affected tenants via audit logs |
| 3 | Rotate credentials and purge stale tokens |
| 4 | File incident in Security Registry with classification `DRR-SC` |
| 5 | Conduct 72-hour post-incident review with root cause analysis |

## Hardening Checklist
- [x] TLS enforced at ingress and database layer  
- [x] IAM roles use minimum privileges  
- [x] RLS enabled for all tenant tables  
- [x] Secrets rotated automatically  
- [x] Idempotency and nonce validation enabled  
- [x] Signed tokens validated by platform public key  
- [x] Cross-region encryption keys independently managed  
- [x] Audit trail linked to Evidence Ledger  

## Ownership
| Role | Responsibility |
|------|----------------|
| Platform Foundation | Service security and RLS enforcement |
| Security Team | Policy validation, key rotation, SIEM monitoring |
| Data Platform SRE | Secrets lifecycle and credential hygiene |

## Summary
The DRR security model enforces isolation, auditability, and least privilege. It integrates with platform identity and evidence systems to ensure every write is authenticated, authorized, and traceable.  
Security posture is reviewed quarterly with automated control verification.