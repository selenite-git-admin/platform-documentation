# Dashboards – Security

## Scope
Security posture for dashboards operations.

## Data Protection
- TLS 1.3, optional response signing, masking where applicable.

## Access Control
- Least privilege; scope checks per dataset/operation; throttling and quotas.

## Auditability
- Log all query/export/delivery operations with evidence ids.

## Notes
- Share links are short‑lived & signed
- Row/column security enforced server-side
- No third‑party JS by default
