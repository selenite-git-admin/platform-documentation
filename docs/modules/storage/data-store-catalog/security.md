# Data Store Catalog (Catalog) Security

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
This document defines the security model for the Data Store Catalog. It enforces authentication, authorization, and data protection policies that preserve dataset confidentiality, integrity, and traceability within the PostgreSQL-based platform.

## Security Objectives
- Ensure only authorized actors can read or modify Catalog records.
- Protect dataset metadata against tampering or unauthorized disclosure.
- Maintain full auditability for every write or migration.
- Avoid vendor dependencies for IAM or access control.

## Authentication
All Catalog endpoints require JWT authentication.

| Consumer | Token Type | Issuer | Lifetime | Validation |
|-----------|-------------|---------|------------|-------------|
| User | Access JWT | Identity Service | 60 min | JWK public key |
| Service | m2m JWT | Platform IAM | 24 hr | Mutual TLS + JWK |
| Maintenance Job | System Token | Platform Foundation | 8 hr | Static key rotation |

Tokens embed:
- `sub`: user or service id
- `tenant_id`: used for row-level security (RLS)
- `scopes`: list of allowed operations (`catalog.read`, `catalog.write`, `catalog.migrate`)
- `iat` / `exp`: validity timestamps

Catalog APIs reject requests without valid tokens or expired credentials.

## Authorization
Authorization is enforced using **row-level security (RLS)** on PostgreSQL tables and API-layer checks.

### Layers of Enforcement
1. **API Scope Filter**
   - Verifies token scope before accessing endpoint.
   - Example: only `catalog.write` allows POST or PATCH operations.
2. **Row-Level Security (RLS)**
   - Enforced at database level.
   - Policies defined per tenant and access class.
3. **Access Class Mapping**
   - Each dataset record references an `access_class` (e.g., `read_internal`, `read_external`, `restricted`).
   - Mapped to PostgreSQL roles defined in `catalog_access_policy`.

Example RLS policy:
```sql
CREATE POLICY tenant_access_policy
ON catalog_dataset
FOR SELECT
USING (tenant_scope = current_setting('app.tenant_id') OR tenant_scope = 'multi');
```

### Principle of Least Privilege
- Each API pod runs under its own IAM role.
- Internal tokens scoped narrowly to their dataset ownership.
- System jobs have write-only or audit-only roles as applicable.

## Encryption
- All data encrypted in transit (TLS 1.3).
- PostgreSQL storage encrypted at rest via AWS RDS-managed KMS.
- Schema documents (JSON) stored in S3 encrypted with SSE-S3.
- Secrets managed in AWS Secrets Manager with automatic rotation every 90 days.

### Sensitive Fields
| Field | Protection |
|-------|-------------|
| `owner_email` | Stored hashed via SHA-256 |
| `payload` in `catalog_audit` | Redacted PII before insert |
| `correlation_id` | UUID-v7, not guessable |

## Audit and Evidence Ledger Integration
Every change event written to Catalog is mirrored to the Evidence Ledger.

| Event | Logged Data | Retention |
|--------|--------------|------------|
| Dataset created | dataset_id, actor, timestamp | 365 days |
| Schema version updated | dataset_id, version, checksum | 365 days |
| Migration applied | migration_id, change_reason | 365 days |
| Dataset deprecated | dataset_id, reason, replacement | 365 days |

Evidence Ledger ensures non-repudiation and immutability.

Example audit payload:
```json
{
  "event_id": "evt_01J7KQ3R7C7TZ9",
  "dataset_id": "gdp.sales_invoice_v3",
  "actor": "platform-migration-service",
  "action": "migrate",
  "correlation_id": "req-9b8c",
  "ts": "2025-10-12T09:12:15Z"
}
```

## Data Retention
| Table | Retention | Purge Policy |
|-------|------------|--------------|
| catalog_dataset | Permanent | Manual delete by governance |
| catalog_location | Permanent | Manual delete by governance |
| catalog_schema_version | Permanent | Manual delete by governance |
| catalog_audit | 365 days | Auto purge |
| catalog_deprecation | Permanent | Updated manually |

All purges logged to the Evidence Ledger.

## Secrets Management
| Secret | Storage | Rotation |
|--------|----------|-----------|
| PostgreSQL credentials | AWS Secrets Manager | 90 days |
| API tokens (system) | Secrets Manager | 30 days |
| Signing keys (JWT) | Platform IAM | 90 days |
| Encryption keys (KMS) | AWS KMS | 1 year |

Rotation tested monthly in staging.

## Network Security
- API endpoints accessible only through HTTPS (443).
- Internal writes restricted to VPC subnets.
- Admin endpoints exposed via bastion host access only.
- Ingress and egress controlled through ALB security groups.

Security group example:
```hcl
ingress {
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/16"]
}
egress {
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}
```

## Threat Controls
| Threat | Mitigation |
|--------|-------------|
| SQL injection | Parameterized queries, ORM sanitation |
| Token replay | Short-lived JWTs + jti validation |
| Unauthorized writes | Scope-based access + RLS |
| Data tampering | Immutable audit log |
| Key leakage | Rotations and IAM boundaries |
| Insider access | Audit trail + differential roles |
| DDoS | WAF + rate limiting |

## Security Monitoring
- Metrics emitted for failed auth, rejected tokens, and 403 events.
- Alerts trigger on >5% auth failures within 10 minutes.
- Evidence Ledger reconciliation validates all critical writes daily.
- Weekly inspection of RLS policies and access-class mapping drift.

## Compliance Alignment
- Encryption and access policies align with **ISO 27001** and **SOC 2 Type II** practices.
- Audit retention and integrity mirror **CIS PostgreSQL Benchmark**.
- Identity and secret management conform to **AWS Well-Architected Security Pillar**.

## Ownership
| Function | Responsibility |
|-----------|----------------|
| Platform Foundation | RLS design, key management, and Ledger integration |
| DevOps | Secrets rotation, TLS management |
| SRE | Audit and drift monitoring |
| Governance | Compliance validation and policy review |

## Summary
Catalog security ensures all dataset metadata in PostgreSQL is protected, auditable, and compliant. Authentication, RLS-based authorization, encryption, and audit immutability together enforce the platform’s zero-trust and zero-engineering data governance philosophy.