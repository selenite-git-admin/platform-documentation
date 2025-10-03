# Security

## Scope
Security expectations and controls for Policy Registry. This page covers data classification, access control, auditability, and operational safeguards that apply when operating the module.

## Ownership boundaries
- Policy Registry stores policy definitions, versions, bindings, evaluations, and audit entries.
- It does not manage identities or entitlements. Authentication and authorization are handled by Access Modules.
- It does not store secrets beyond configuration required to reach its datastore. Secrets are supplied by the platform secret manager.

## Data classification and retention
- Policy definitions and versions are configuration data. Treat as internal.
- Evaluations and evidence are operational records. Retain according to platform retention policy.
- Avoid storing subject payloads inside evaluations or evidence. Store references where possible.
- Audit entries are append only. Retain as defined in the platform audit policy.

## Data protection
- Encrypt network traffic using TLS for all API calls.
- Encrypt data at rest in the registry datastore.
- Manage encryption keys with the platform key management service. Rotate keys on the platform schedule.
- Remove sensitive fields from logs. Avoid including user supplied payloads in log messages.

## Access control
Roles
- Policy administrator can create and update policies and manage bindings.
- Operator can read policies, bindings, evaluations, and audit entries.
- Service account can call evaluate.

Permissions
- Create policy and version
- Set current version
- Create and disable bindings
- Evaluate
- Read evaluations and evidence
- Read audit entries

Principles
- Enforce least privilege for service accounts.
- Restrict write actions to administrators.
- Validate inputs on every write operation.

## Scope isolation
- Bindings are created for a specific scope_type and scope_ref.
- Evaluation resolves only the bindings that match the provided scope.
- Do not expose bindings outside their scope in API responses.

## Auditability
- Record administrative actions in audit_log with actor, action, target, and timestamp.
- Record every decision in evaluations with a reference to the policy version.
- Capture evidence references in evaluation_evidence.
- Include correlation_id on write operations and propagate through logs.

## Input validation and limits
- Validate policy definitions against a schema before accepting a version.
- Enforce request size limits for API calls.
- Enforce field length limits for names, categories, and identifiers.
- Reject unknown fields. Return clear error codes and messages.
- Apply idempotency for unsafe operations as described in the API page.

## Availability and abuse protection
- Apply per caller rate limits on write operations and evaluation requests.
- Use timeouts and retries with backoff when accessing the datastore.
- Protect against evaluation storms by setting concurrency limits.
- Add circuit breakers for downstream dependencies if present.

## Secrets management
- Store database credentials and API tokens in the platform secret manager.
- Load secrets at runtime using the platform mechanism. Do not embed secrets in images or configuration files.
- Do not print secrets to logs. Redact on error paths.

## Incident response hooks
- Include correlation identifiers in responses and logs to support tracing.
- Follow procedures in the Runbook for denial spikes, latency breaches, and store degradation.
- Respect legal hold and export procedures when handling evidence records.

## Checklists

Release
- Access controls configured for administrator, operator, and service accounts
- TLS enabled for API front door
- Encryption at rest enabled for datastore
- Metrics, logs, and traces emitting as defined in Observability
- Runbook linked from alerts

Runtime
- Rate limits and timeouts configured
- Secret rotation verified on schedule
- Audit entries observed during change windows
- Backups and restores tested according to platform policy

Change
- New policy schemas validated in a non production environment
- Migrations reviewed and applied with roll forward or rollback path
- Monitoring thresholds adjusted if evaluation volume changes

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
