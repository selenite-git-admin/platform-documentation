# Catalog – Security

## Scope
Security posture for catalog operations.

## Data Protection
- TLS 1.3, optional response signing, masking where applicable.

## Access Control
- Least privilege; scope checks per dataset/operation; throttling and quotas.

## Auditability
- Log all query/export/delivery operations with evidence ids.

## Notes
- Read-only surface
- Contract/version badges on responses
- No PII in metadata fields
