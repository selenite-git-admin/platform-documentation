# Schema Services — Summary

## Purpose
Schema Services form the metadata backbone of the BareCount Data Platform.  
They define, store, and enforce contracts across **Raw**, **Golden Data Points (GDP)**, and **KPI** layers.  
They ensure downstream analytics are traceable, versioned, and compliant, while never persisting tenant business data.

## Scope
- **Raw Contracts**: declare source system schemas and ingestion requirements.  
- **GDP Contracts**: define canonicalized entities (Calendar, Currency, Org, etc.).  
- **KPI Contracts**: specify metrics, formulas, thresholds, and SLAs.  
- **Versioning**: Major–Minor–Update rules with immutable history.  
- **Validation**: schema checks, lineage integrity, audit evidence.  
- **APIs**: registry and runtime enforcement services exposed via PHS.

## Design Principles
- **Canonicalization**: unify raw attributes into GDP entities.  
- **Auditability**: every contract version and enforcement outcome logged with immutable evidence.  
- **Agnostic**: independent of ERP/CRM source systems.  
- **Metadata-only**: no tenant business data is stored.  
- **Governance vs Enforcement**: lifecycle in PHA; active enforcement in PHS.

## Key Components
1. **GDP Framework**  
   - Canonical entities modeled in Aurora tables.  
   - DB patterns, DDL/DBML, design notes for fiscal calendars, FX, org hierarchies, headcount.  
   - Ensures KPIs are built on a consistent canonical base.

2. **Contracts & Versioning**  
   - Addressing scheme: `<contract_type>/<tenant>/<contract_id>/<major.minor.update>`.  
   - Version semantics: Major (breaking), Minor (extension), Update (non-structural).  
   - Lifecycle states: draft → review → approved → published → active → superseded → retired.  
   - YAML examples for Raw, GDP, and KPI contracts.

3. **Enforcement & Validation**  
   - Enforcement points at ingress, canonicalization, KPI evaluation.  
   - Validators for schema, mappings, references, formulas, policies.  
   - Immutable audit evidence in S3, references stored in Aurora.  
   - Quarantine/error handling integrated with observability.

## Boundaries
- **PHS**: stores contracts, enforces active versions, persists audit evidence.  
- **PHA (Admin App)**: seeds and manages contract lifecycle.  
- **Tenant Apps**: consume validated GDP/KPI outputs but cannot modify contracts.

## Differentiator
Schema Services are the **core differentiator** of BareCount.  
They enable CFO- and C-suite–ready metrics to be generated from **auditable, versioned, canonical definitions**, independent of ERP/CRM complexity.
