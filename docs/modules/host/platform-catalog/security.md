# Security

## Scope
Security expectations and controls for Platform Catalog. This page covers data classification, access control, auditability, and operational safeguards.

## Ownership boundaries
- Stores reference tables and calendars for the platform
- Does not manage identities, billing, or secrets
- Publishes change events but does not call dependents

## Data classification and retention
- Reference data is internal configuration
- Audit entries are append only and retained per policy
- Calendar events do not include personally identifiable information

## Data protection
- TLS for all API calls
- Encryption at rest for datastore
- Key management via platform KMS with rotation

## Access control
Roles
- Catalog administrator can write reference tables and calendars
- Operator can read everything
- Service accounts can read with least privilege scopes

Permissions
- Read all reference sets
- Write specific resources by role

Principles
- Enforce least privilege for service accounts
- Validate inputs and reject unknown fields
- Use idempotency on write endpoints

## Auditability
- Record admin writes in catalog_audit with actor, action, target, and timestamp
- Include correlation_id for traceability
- Emit change events with resource identifiers

## Input validation and limits
- Enforce field length and value constraints
- Validate calendar events for overlapping ranges when kind requires it
- Reject unknown fields and return clear errors

## Availability and abuse protection
- Rate limit admin writes
- Cache reads with ETags
- Use timeouts and retries for datastore

## Incident response hooks
- Correlate incidents using correlation_id
- See Runbook for cache, write, and resolve procedures

## Checklists

Release
- Roles and permissions in place
- TLS and encryption at rest enabled
- Metrics, logs, and traces emitting
- Alerts wired to on call

Runtime
- Secret rotation verified on schedule
- Audit entries during change windows
- Backups and restores tested

Change
- Non production validation for schema and calendar changes
- Rollback path defined for each change

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
