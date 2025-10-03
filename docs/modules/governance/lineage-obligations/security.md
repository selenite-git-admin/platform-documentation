# Security

## Scope
Security expectations and controls for Lineage Obligations.

## Ownership boundaries
- Stores metadata about assets, processes, runs, and evaluation outcomes
- Does not store business data or payloads

## Data classification and retention
- Asset names and tags may contain internal names
- Evaluation details do not contain PII
- Retain ingest logs and evaluations per audit policy

## Data protection
- TLS for all API calls
- Encryption at rest for datastore
- Keys managed by platform KMS

## Access control
Roles
- Platform administrator can author obligations
- Operators can re-evaluate and read evaluations
- Service accounts for ingest with least privilege

Principles
- Enforce tenant isolation on every read and write
- Validate scope queries and tag filters
- Idempotency on ingest to avoid duplicate edges
- Rate limit ingest and evaluate routes

## Auditability
- Record writes in lineage_audit with actor, action, target, and timestamp
- Include correlation_id for tracing

## Incident response hooks
- Correlate incidents using correlation_id
- See Runbook for procedures

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
