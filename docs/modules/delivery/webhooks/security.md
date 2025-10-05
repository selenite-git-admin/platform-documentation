# Webhooks – Security

## Scope
Security posture for webhooks operations.

## Data Protection
- TLS 1.3, optional response signing, masking where applicable.

## Access Control
- Least privilege; scope checks per dataset/operation; throttling and quotas.

## Auditability
- Log all query/export/delivery operations with evidence ids.

## Notes
- HMAC signatures on payloads
- mTLS optional per tenant
- Ownership verification required
