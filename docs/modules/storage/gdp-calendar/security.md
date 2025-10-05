# GDP Calendar – Security

## Scope
Security posture for gdp calendar operations.

## Data Protection
- Encryption at rest (KMS envelope), TLS 1.3, row/column-level masking where applicable.

## Access Control
- Least privilege; dataset and field-level ACLs; per-tenant isolation.

## Auditability
- Ingest, transform, and access logs with evidence ids.

## Notes
- Signed webhooks
- Role-based access to schedules
- Evidence for status changes
