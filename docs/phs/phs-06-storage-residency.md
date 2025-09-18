## Purpose
Define how residency rules are applied to metadata stored in Platform Host Services (PHS).  
Residency policies determine where metadata (contracts, lineage, audit, and policy state) is stored and how cross-region access is controlled.

---

## Principles
- **Metadata scope only**: PHS stores contracts, lineage, and evidence metadata — not tenant business data.
- **Region binding**: All metadata pinned to a specific AWS region at deployment.
- **Deny by default**: No cross-region replication unless explicitly configured and approved.
- **Policy enforcement**: Residency is contract-driven; Raw/GDP/KPI contracts declare residency requirements.
- **Audit evidence**: All residency decisions are recorded in audit logs and exportable for compliance.

---

## Residency Decision Matrix

| Dimension         | Option                     | Default Behavior                          | Notes |
|-------------------|----------------------------|-------------------------------------------|-------|
| **Region**        | Single Region              | PHS metadata pinned to deployment region  | Default model |
|                   | Multi-Region Active/Passive| Cross-region read-replicas with controlled failover | Optional for DR |
|                   | Multi-Region Active/Active | Not supported for PHS metadata            | Avoid conflict in contract state |
| **Data Type**     | Contracts & Versions       | Regional Aurora DB                        | Snapshots encrypted + retained |
|                   | Audit Evidence             | Regional S3 bucket, versioned + locked    | Object lock enabled |
| **Tenant Scope**  | Multi-tenant SaaS          | Shared metadata region                    | Isolation at row/object level |
|                   | Single-tenant SaaS         | Metadata pinned to tenant’s chosen region | Provisioned via Admin App |
|                   | On-prem/Hybrid             | Residency delegated to customer infra     | PHS stores only control metadata |

---

## Enforcement Points
- **Contract metadata**: Residency declared as attribute; validated at publish time.
- **Ingress/Egress**: Residency enforced before metadata is accepted/exported.
- **Storage tiering**: Residency rules applied to Aurora, S3, Redis independently.
- **Backups**: Snapshots remain in-region unless cross-region DR explicitly enabled.
- **Audit**: All residency decisions and overrides logged with evidence IDs.

---

## Exceptions & Overrides
- Residency exceptions require explicit contract flag (`allow_cross_region = true`).
- Overrides must be applied via CDK/Pipeline with approval workflow.
- Audit evidence includes approver identity, change request, and effective time window.
- No ad-hoc console edits permitted.

---

## Time-to-Live (TTL)
- Contracts and metadata: retained until superseded + 90-day grace TTL.
- Audit logs: 365 days minimum (configurable).
- Evidence objects: default 7 years, configurable per compliance requirement.

---

## End State
Storage residency for PHS metadata is **deterministic, contract-driven, and auditable**.  
It ensures metadata never leaves its designated region without explicit policy, while still supporting compliance, DR, and hybrid deployments when required.