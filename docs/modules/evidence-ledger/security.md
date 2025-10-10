# Evidence Ledger – Security

## Scope
Security expectations, data handling, and access control.

## Data Protection
- TLS 1.3, AES‑256 at rest, KMS key rotation (90d).

## Access Control
- Least privilege; scoped tokens; per‑tenant rate limits.

## Auditability
- Emit evidence and admin audit logs with actor and reason.

## Notes
- Append‑only store; no update/delete APIs
- Separate signer for hash calculation
- Access to exports restricted to audit roles
