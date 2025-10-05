# Security

- AuthN: Bearer JWT; AuthZ: ABAC with owner/write roles.
- Tenant isolation on all reads/writes.
- PII: only metadata markers stored; sample payloads redacted.
- Compliance: all writes produce receipts; deprecations require approvals; audit via Evidence Ledger.
