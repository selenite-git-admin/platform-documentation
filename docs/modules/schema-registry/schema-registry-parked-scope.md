# Schema Registry — Parked Scope
> Applies to: Platform Roadmap (Future Considerations) • Owner: Platform Engineering • Last updated: 2025-10-07

## Background
The Schema Registry currently operates under a **platform-owned, centrally governed model**.  
All schemas are curated, validated, and published by the Platform Engineering team.  
Tenants (client organizations) use these schemas during data-source onboarding and request changes through a controlled workflow.

However, as the platform matures, certain tenants will demand **greater autonomy and faster iteration** — especially for systems with custom extensions (SAP Z/Y tables, local CRMs, proprietary production data).  
This file captures those **deferred capabilities** that extend the Registry toward a more collaborative, semi-federated model while maintaining platform integrity.

---

## Opportunity
1. **Client-Admin Schema Authoring** – Allow tenant admins to define schemas for local or custom sources in a sandboxed environment.
2. **Tenant Schema Sandbox** – Provide a secure, isolated workspace where schema drafts can be validated and previewed without affecting the global registry.
3. **Automated Promotion Pipeline** – Introduce workflows to promote tenant schemas to global or shared scope after governance review.
4. **Schema Marketplace / Discovery** – Enable cross-tenant discovery of approved, reusable schemas.
5. **Policy-Driven Governance Automation** – Implement approval, version control, and validation as codified policies rather than manual reviews.
6. **AI-Assisted Schema Evolution** – Use AI models to propose compatible field mappings, detect semantic drift, and recommend normalization patterns.

---

## Deferred Scope
| Capability | Status | Reason for Deferral |
|-------------|---------|--------------------|
| Client-admin schema authoring | Not implemented | Requires strict isolation and audit controls |
| Tenant schema sandbox | Concept approved | Needs Registry multi-namespace and access model |
| Policy-driven approvals | Design draft only | Governance board automation pending |
| Schema marketplace | On hold | Requires strong metadata standardization |
| AI-assisted compatibility validation | Experimental | Accuracy and reproducibility not production-grade |

---

## Proposed Implementation (Future Phase)
### 1. Tenant Namespace Isolation
- Each tenant receives a private namespace (`tenant.<tenant_code>.<layer>.<subject>`).  
- Schemas authored within this namespace remain invisible to other tenants.  
- Publishing requires platform signing and compliance checks.

### 2. Validation & Approval Workflow
1. **Draft submission** by tenant admin through UI/API.  
2. **Automated validation** (syntax, naming, constraint checks).  
3. **Platform approval** with option to promote to global scope.  
4. **Publishing** → signed and indexed under tenant namespace.  

### 3. Marketplace & Discovery Portal
- Provide catalog search across global and tenant schemas.  
- Include metadata filters (domain, layer, compatibility, tenant).  
- Only **governance-approved** schemas visible to external tenants.

### 4. Policy-Driven Approvals
- Define governance rules in YAML-based policy packs.  
- Example:  
  ```yaml
  approval:
    require_signoff: true
    allowed_layers: ["extractor", "gdp"]
    max_fields_per_schema: 800
  ```
- Validation pipeline reads and enforces policies automatically.

### 5. AI-Assisted Schema Review (Experimental)
- Integrate AI model to detect anomalies, suggest type harmonization, and evaluate compatibility deltas.
- Output non-binding recommendations to governance reviewers.

---

## Prerequisites
- Multi-namespace registry support.  
- Fine-grained RBAC separating tenant admins from platform maintainers.  
- Secure signing infrastructure for tenant-scoped schemas.  
- Versioned policy engine integrated with Governance Service.  
- Observability extensions for sandbox activities.

---

## Impact (Expected)
| Area | Positive Impact | Risk / Mitigation |
|------|------------------|------------------|
| Tenant autonomy | Faster response to unique data sources | Governance sprawl — mitigated via namespaces |
| Platform workload | Reduced manual CR churn | Increased validation complexity |
| Schema quality | Broader coverage of real-world sources | Requires strong audit & observability |
| Ecosystem growth | Enables schema marketplace and reuse | Must enforce strict compatibility checks |

---

## Decision Gate
| Criterion | Requirement |
|------------|--------------|
| Registry namespace isolation ready | ✅ Required |
| Governance API refactored to handle policy packs | ✅ Required |
| Validation sandbox stable at scale | ✅ Required |
| AI validation accuracy > 95% on sample datasets | Optional |
| Governance board approval | ✅ Mandatory |

---

## References
- `modules/schema-registry/construction.md` – Defines canonical contract model.
- `modules/schema-registry/lifecycle/*` – Current production lifecycle.
- `modules/schema-registry/governance.md` – Policy and approval framework (active).
- This document: conceptual extension for **Phase 2 and beyond**.

---
