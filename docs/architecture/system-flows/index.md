# System Flows

## Purpose
System flows describe how the platform behaves end to end for common scenarios. 
They provide a shared reference so developers and reviewers can reason about responsibilities, data movement, and control points.

## Scope
This section covers development time and runtime flows. 
It includes connector build and publish, tenant onboarding, incremental extraction, schema drift handling, failure and retry, secrets access, network connectivity, and catalog generation. 
Each flow is documented as a step by step narrative with clear inputs, outputs, and owned components.

## Principles
- Flows must show only platform responsibilities and contracts, not vendor specific logic. 
- Flows must identify control plane tables and registries that record state and decisions. 
- Flows must show security and compliance touch points. 
- Flows must be testable. Each step should have observable events or metrics.

## Next
- [Connector Build and Publish](flow-connector-build-publish.md)  
- [Tenant Onboarding](flow-tenant-onboarding.md)  
- [Incremental Run Lifecycle](flow-incremental-run.md)  
- [Schema Drift Handling](flow-schema-drift.md)  
- [Failure and Retry](flow-failure-retry.md)  
- [Secrets Access](flow-secrets-access.md)  
- [Network Connectivity](flow-network-connectivity.md)  
- [Catalog Generation](flow-catalog-generation.md)  
