# Schema Services — Overview

## Purpose
Schema Services form the metadata backbone of the BareCount Data Platform.  
They define how source system schemas are represented, how they are standardized into Golden Data Points (GDP), and how Key Performance Indicators (KPIs) are derived.  
All contracts are versioned, auditable, and governed through the control plane.

---

## Scope
Schema Services provide:
- **Contract Registry** for Raw, GDP, and KPI schemas.  
- **Version Management** with Major–Minor–Update rules and immutable history.  
- **Mapping Definitions** between Raw → GDP → KPI layers.  
- **Enforcement & Validation** to ensure schema consistency, lineage integrity, and audit evidence.  
- **APIs** for publishing, validating, and consuming schemas across the platform.

---

## Design Principles
- **Canonicalization**: GDP layer abstracts raw detail into consistent business entities.  
- **Auditability**: every schema and mapping change is versioned and logged.  
- **ERP/CRM Agnostic**: contracts are independent of source vendor systems.  
- **Metadata-only**: Schema Services manage metadata and lineage, not tenant business data.  
- **Contract-driven**: enforcement is always tied to an active contract version.

---

## Database Representation
- **Aurora PostgreSQL**: relational store for contracts, versions, lineage, and mappings.  
- **S3 Evidence Buckets**: audit artifacts linked to schema enforcement.  
- **Redis Cache**: transient validation state (e.g., throttling counters).  
- Each GDP/KPI entity is represented as a relational table keyed by `contract_id`, `version`, and `tenant_id`.  
- Schema definitions are expressed as contracts and stored alongside lineage metadata for traceability.  

---

## Boundaries
- **PHS**: persists contracts, enforces active versions, and records audit evidence.  
- **PHA (Admin App)**: manages contract lifecycle (publish, activate, supersede).  
- **Tenant Apps**: consume GDP/KPI outputs but cannot alter contracts.  

---

## Sections
- [GDP Framework](gdp-framework.md) — canonical entities, database representation, and system design notes.  
- [Contracts & Versioning](contracts.md) — rules for contract lifecycle and immutable history.  
- [Enforcement & Validation](enforcement.md) — runtime enforcement, validation, and audit eventing.  

---

## Differentiator
Schema Services are the **core differentiator** of BareCount.  
They ensure that downstream metrics and analytics are always **traceable, versioned, and compliant**, regardless of underlying source systems.
