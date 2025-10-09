# Security

## AuthN/Z
- Bearer JWT + `X-Tenant-Id` on all endpoints.
- ABAC enforced per resource; scopes map to CRUD and replay.

## Data protection
- TLS 1.3 in transit. At rest via platform KMS policies.
- PII fields must be masked in logs and traces.

## Webhooks
- HMAC signatures `X-Signature: sha256=...` with per-tenant secret; mTLS optional.

## Compliance
- Evidence receipts for all writes.
- Sunset headers on deprecations (≥ 6 months).
