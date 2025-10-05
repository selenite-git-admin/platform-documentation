# Activation APIs – Security

## Scope
Security posture for activation apis operations.

## Data Protection
- TLS 1.3, optional response signing, masking where applicable.

## Access Control
- Least privilege; scope checks per dataset/operation; throttling and quotas.

## Auditability
- Log all query/export/delivery operations with evidence ids.

## Notes
- Field-level masks per role/tenant
- Optional response signing
- Evidence for large exports
