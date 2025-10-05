# Action Engine – Security

## Scope
Security posture for action engine operations.

## Data Protection
- TLS 1.3, signed webhooks (HMAC), mTLS for private targets.

## Access Control
- Least privilege; per-tenant quotas; rule publish approvals.

## Auditability
- Record rule changes, template publishes, and deliveries with evidence ids.

## Notes
- Rule edits require approval
- Jobs are idempotent with keys
- All actions recorded with evidence ids
