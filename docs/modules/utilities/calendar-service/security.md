# Security

## Scope
Security expectations and controls for Calendar Service. This page covers data classification, access control, auditability, and safeguards.

## Ownership boundaries
- Stores calendar definitions, events, sets, overlays, fiscal calendars
- Publishes change events but does not call dependents

## Data classification and retention
- Calendar data is internal configuration
- Overlays contain tenant identifiers only
- Audit entries are append only

## Data protection
- TLS for all API calls
- Encryption at rest for datastore
- Keys managed by platform KMS

## Access control
Roles
- Calendar administrator can write definitions, events, sets, overlays, fiscal calendars
- Operator can read everything
- Service accounts can read with least privilege scopes

Principles
- Validate inputs and reject unknown fields
- Use idempotency on writes
- Rate limit admin writes

## Auditability
- Record admin writes in calendar_audit with actor, action, target, and timestamp
- Include correlation_id for traceability

## Incident response hooks
- Correlate incidents using correlation_id
- See Runbook for procedures

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)


## Tenant settings
- Tenant settings writes are allowed to users with tenant admin roles in Tenant App
- Validate `business_hours` payloads for overlapping or invalid ranges
- Audit PUT /tenants/{tenant_id}/settings with actor and correlation_id

## Date Table exports
- Exports contain no PII. Treat as internal artifacts
- For signed URLs, constrain lifetime and scope
- Audit profile changes and materializations with actor and correlation_id
