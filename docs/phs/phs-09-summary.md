# Platform Host Services (PHS) — Summary

## Purpose
Platform Host Services (PHS) provide the control plane for the BareCount Data Platform.  
They manage metadata, contracts, lineage, compliance, and shared services required to operate the platform.  
PHS never stores tenant business data; it governs metadata and enforcement only.

---

## Scope
- **Control Plane Services**: contract registry, versioning, lineage, audit evidence.  
- **Common Shared Services**: IAM, tenancy manager, policy/compliance, configuration, secrets, observability, orchestration, schema registry, storage fabric, API gateway.  
- **Security**: restricted to Platform Super Admin via CLI/CDK/CICD; MFA enforced.  
- **Storage**: metadata in Aurora, audit evidence in S3, transient state in Redis.  
- **Lifecycle Management**: contracts published via PHA; PHS enforces active versions.  
- **Outbound Connectivity**: deny by default; allowlist for specific connectors with TLS/mTLS.

---

## Design Principles
- **Metadata-only**: no tenant business data stored.  
- **Contract-driven**: all enforcement tied to an active version.  
- **Least privilege**: Super Admin role is narrow but high-power.  
- **Immutable evidence**: every enforcement outcome logged with evidence ID.  
- **Residency & Retention**: contract-driven, auditable, policy-enforced.  
- **AWS-native**: implemented with Aurora, S3, Redis, CDK, and IAM.

---

## Key Components
1. **Overview**  
   - Role as control plane, separation from tenant workloads.

2. **Infrastructure**  
   - Deployment via AWS CDK and CICD.  
   - Ready state = platform host infrastructure prepared for PHA deployment.

3. **Core Architecture**  
   - Ingress, Processing, Serving, Ops, Provisioning, Egress layers.  
   - Enforcement and observability embedded across layers.

4. **Security & NFRs**  
   - Super Admin CLI-only access, MFA, deny-by-default egress.  
   - Reliability targets, performance budgets, compliance guarantees.

5. **Storage Strategy**  
   - Aurora for metadata, S3 for evidence, Redis for transient state.  
   - Encryption via KMS CMKs; secrets in Secrets Manager.

6. **Storage Residency**  
   - Region binding enforced; no cross-region replication unless approved.  
   - Residency declared in contract headers and validated at publish time.

7. **Storage Operations**  
   - Backups, retention, restore drills, legal holds, monitoring, alerts.  
   - DR optional, policy-driven.

8. **Costs & Budget**  
   - Cost units tied to metadata volume, contract versions, evidence stored.  
   - Budget visibility through observability hub.

---

## Boundaries
- **PHA (Admin App)**: seeds and manages contract lifecycle.  
- **PHS**: enforces active versions, stores audit evidence.  
- **Tenant Apps**: consume validated outputs but do not interact with PHS directly.

---

## Differentiator
PHS provides a **secure, auditable, metadata-only control plane**.  
It ensures governance, compliance, and lifecycle separation, enabling tenant applications to operate safely without carrying control-plane complexity.
