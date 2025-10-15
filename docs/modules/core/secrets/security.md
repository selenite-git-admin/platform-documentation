# Secrets – Security

## Scope
Security expectations, data handling, and access control.

## Data Protection
- TLS 1.3, AES‑256 at rest, KMS key rotation (90d).

## Access Control
- Least privilege; scoped tokens; per‑tenant rate limits.

## Auditability
- Emit evidence and admin audit logs with actor and reason.

## Notes
- Deny by default for unknown paths
- No wildcard grants; path prefixes only
- All reads emit audit events with subject and reason
