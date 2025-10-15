# Gateway – Security

## Scope
Security posture for gateway operations.

## Data Protection
- TLS 1.3, HSTS, modern ciphers; secure cookie flags.

## Access Control
- Least privilege; per‑path policies; per‑tenant rate limits.

## Auditability
- Log all admin changes with actor, reason, and evidence ids.

## Notes
- HSTS enabled with preload
- OCSP stapling on
- Only TLSv1.2+; prefer v1.3
