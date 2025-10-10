# Subscription Enforcement – Security

## Scope
Security expectations, access control, classification, and audit for Subscription Enforcement. 【122†source】

## Ownership boundaries 【122†source】
- Processes: plan lookups, entitlement evaluation, decision computation.  
- Stores: short‑term decision cache; no long‑term PII.  
- Delegates: Evidence storage to Trust → Evidence Ledger; usage aggregation to Runtime → Metering.

## Data classification and retention 【122†source】
| Data | Class | Retention |
|------|------|-----------|
| Decision cache | Operational | < 24 h |
| Evidence pointer | Confidential | 90 days |
| Metrics/logs | Operational | 30 days |

Avoid PII unless necessary and documented in the plan registry.

## Data protection 【122†source】
- TLS 1.3 in transit; AES‑256 at rest.  
- KMS‑managed keys with 90‑day rotation.  
- Sensitive fields redacted in logs.

## Access control 【122†source】
| Role | Allowed actions |
|------|------------------|
| Tenant | Evaluate, Get Plan, Simulate |
| Admin | All tenant actions + override management |
| Service | Publish evidence, push usage deltas |

Principles: least privilege, scoped tokens, per‑tenant rate limits.

## Auditability 【122†source】
- Decision events recorded with `evidence_id`, policy identifiers, and request hash for correlation.  
- All admin actions produce audit logs with actor and reason.  
- Correlate incidents via `X‑Request‑Id` and trace IDs.

## Incident response hooks 【122†source】
- Alerts wire to `#sev-access-ops`.  
- Use runbook “Audit evidence chain” for verification.  
- Link incident timeline to Evidence Ledger export.

## References 【122†source】
- [Runbook](runbook.md)  
- [Observability](observability.md)  
- [API](api.md)
