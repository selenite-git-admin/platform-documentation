# Encryption – Security

## Scope
Security expectations, data handling, and access control.

## Data Protection
- TLS 1.3, AES‑256 at rest, KMS key rotation (90d).

## Access Control
- Least privilege; scoped tokens; per‑tenant rate limits.

## Auditability
- Emit evidence and admin audit logs with actor and reason.

## Notes
- Keys never exported; only references stored
- Dual control for admin operations
- Residency‑aware key selection
