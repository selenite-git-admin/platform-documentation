# Pipeline Configuration

## Purpose
The Pipeline Configuration stage defines how pipelines are declared, versioned, and executed in the BareCount Data Action Platform. It provides a manifest-driven approach that balances developer flexibility with governance requirements.

## Context
Ad hoc configuration leads to drift, inconsistency, and errors across environments. BareCount enforces contract-driven pipeline configuration. Each pipeline is defined declaratively in a manifest file. Manifests are version-controlled, validated against schemas, and stored in the registry. This ensures that pipelines are portable, reproducible, and aligned with enterprise governance.

## Key Capabilities

### Manifest Structure
- Each pipeline is defined using a YAML or JSON manifest.  
- Required sections include pipeline metadata, input streams, transformations, outputs, and SLOs.  
- Optional sections include tags, owners, and alerts.  
- Manifests must pass validation against a schema registry before deployment.

### Tenant Overrides
- Tenants can override runtime parameters such as schedules, retention classes, or alert routing.  
- Overrides are applied declaratively without modifying the base manifest.  
- This allows a single pipeline definition to serve multiple tenants while respecting unique needs.

### Versioning
- Manifests are version-controlled and linked to contract versions.  
- Updates create new versions rather than mutating existing definitions.  
- Historical runs can always be traced back to the manifest version in effect.

### Environment Promotion
- Pipelines are promoted across environments (dev, test, prod) by moving validated manifests.  
- Promotion includes validation checks for compatibility with contracts and governance rules.  
- Drift detection prevents unauthorized configuration changes between environments.

### Registry Integration
- All manifests are stored in the BareCount registry.  
- Registry provides APIs to query pipeline definitions, owners, and version history.  
- Governance teams use the registry to audit and approve changes.

## Operating Model
- Developers author pipeline manifests and submit them for validation.  
- The registry enforces schema checks and governance policies.  
- Approved manifests are deployed to environments through CI/CD pipelines.  
- Tenant admins apply overrides to adjust schedules or alerts without affecting core definitions.

## Example
A KPI pipeline manifest declares:
- Source: SAP OData connector  
- Transform: GDP Revenue normalization v2.0  
- Output: KPI Revenue Materialized Table  
- Freshness SLO: 2 hours  
- Owner: Finance Data Engineering  

The manifest is validated, stored in the registry, and deployed to production. Later, a tenant override adjusts the schedule from daily to hourly, without modifying the manifest itself.

## Notes
BareCount uses manifest-driven configuration to ensure consistency, traceability, and governance. Pipelines are not coded as scripts but declared as contracts. This design reduces errors, improves auditability, and accelerates enterprise adoption.
