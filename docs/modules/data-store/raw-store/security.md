# Raw Store – Security

## Scope
Security posture for raw store operations.

## Data Protection
- Encryption at rest (KMS envelope), TLS 1.3, row/column-level masking where applicable.

## Access Control
- Least privilege; dataset and field-level ACLs; per-tenant isolation.

## Auditability
- Ingest, transform, and access logs with evidence ids.

## Notes
- Default-deny bucket policies
- Server-side and client-side encryption
- Least-privilege access
