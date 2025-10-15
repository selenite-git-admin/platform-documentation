# Action Catalog – Security

## Scope
Security posture for action catalog operations.

## Data Protection
- TLS 1.3, signed webhooks (HMAC), mTLS for private targets.

## Access Control
- Least privilege; per-tenant quotas; rule publish approvals.

## Auditability
- Record rule changes, template publishes, and deliveries with evidence ids.

## Notes
- Templates are signed at publish
- Approvals required with two‑person rule
- Only published versions are resolvable at runtime
