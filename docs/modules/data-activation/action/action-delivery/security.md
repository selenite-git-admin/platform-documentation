# Action Delivery – Security

## Scope
Security posture for action delivery operations.

## Data Protection
- TLS 1.3, signed webhooks (HMAC), mTLS for private targets.

## Access Control
- Least privilege; per-tenant quotas; rule publish approvals.

## Auditability
- Record rule changes, template publishes, and deliveries with evidence ids.

## Notes
- mTLS for private webhooks
- HMAC signing on all webhook deliveries
- Egress controlled by allow-lists
