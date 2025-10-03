# Security

## Scope
Security expectations and controls for Data Contract Registry. This page covers data classification, access control, auditability, and operational safeguards for the four layer, artifact only model.

## Ownership boundaries
- Data Contract Registry stores dataset records, schema versions per layer, subscriptions, and audit entries.
- It does not manage identities or entitlements. Authentication and authorization are provided by Access Modules.
- It does not store data rows or samples. Schema artifacts are the only payloads it accepts.
- It may reference an external Schema Registry by storing an identifier. Artifact storage can remain external.

## Data classification and retention
- Dataset metadata and schemas are internal configuration. Treat as internal.
- Subscriptions identify consuming services. Treat as internal.
- Audit entries are append only and retained per the platform audit policy.
- Do not embed secrets or production sample data inside schemas. If discovered, reject or scrub the payload.

## Data protection
- Encrypt network traffic with TLS for all API calls.
- Encrypt data at rest in the registry datastore.
- Manage keys with the platform key management service. Rotate keys on the platform schedule.
- Remove sensitive fields from logs. Log identifiers and hashed values when needed.

## Access control
Roles
- Registry administrator can create datasets and ingest schemas for any layer.
- Operator can read datasets, versions, diffs, and subscriptions.
- Service accounts can read and, when authorized, ingest for specific datasets and layers.

Permissions
- Create dataset
- Ingest schema for a layer
- Read datasets, versions, and diffs
- Create and read subscriptions
- Read audit entries

Principles
- Enforce least privilege for service accounts at dataset and layer granularity.
- Restrict write operations to administrators or designated service accounts.
- Validate inputs on every write operation.

## Scope isolation
- All operations are scoped by dataset and layer. Enforce access checks for both.
- Do not expose schemas or subscriptions outside the caller’s authorization scope.
- Maintain clear separation between extraction, raw, gold, and activation layers.

## Auditability
- Record administrative and write actions in audit_log with actor, action, target, and timestamp.
- Record version creation with dataset_id, layer, version, classification, and is_current.
- Include correlation_id on write operations and propagate to logs for tracing.
- Provide immutable history for each dataset and layer.

## Input validation and limits
- Validate schema_json for well formed structure before accepting a version.
- Enforce request size limits for API calls.
- Enforce field length limits for namespace, name, owner, and identifiers.
- Reject unknown fields. Return clear error codes and messages.
- Apply idempotency on ingest to prevent duplicate versions.

## Availability and abuse protection
- Apply per caller rate limits on ingest and subscription writes.
- Use timeouts and retries with backoff when accessing the datastore.
- Protect against ingest storms by setting concurrency limits.
- Add circuit breakers for downstream dependencies if Schema Registry is called.

## Secrets management
- Store database credentials and API tokens in the platform secret manager.
- Load secrets at runtime using the platform mechanism. Do not embed secrets in images or configuration files.
- Do not print secrets to logs. Redact on error paths.

## Incident response hooks
- Include correlation identifiers in responses and logs to support tracing.
- Follow procedures in the Runbook for breaking changes, ingest failures, and store degradation.
- Respect legal hold and export procedures when handling audit records.

## Checklists

Release
- Roles and permissions configured for administrator, operator, and service accounts
- TLS enabled for the API front door
- Encryption at rest enabled for the datastore
- Metrics, logs, and traces emitting as defined in Observability
- Runbook linked from alerts

Runtime
- Rate limits and timeouts configured
- Secret rotation verified on schedule
- Audit entries observed during change windows
- Backups and restores tested per platform policy

Change
- Schema validation logic updated in a non production environment first
- Migrations reviewed and applied with roll forward or rollback path
- Monitoring thresholds revisited if ingest volume changes

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
