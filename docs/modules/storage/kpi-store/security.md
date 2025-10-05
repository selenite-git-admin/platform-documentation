# KPI Store – Security

## Scope
Security posture for kpi store operations.

## Data Protection
- Encryption at rest (KMS envelope), TLS 1.3, row/column-level masking where applicable.

## Access Control
- Least privilege; dataset and field-level ACLs; per-tenant isolation.

## Auditability
- Ingest, transform, and access logs with evidence ids.

## Notes
- Contracts enforced at query layer
- Row/column-level security for tenants
- Access logged with evidence ids
