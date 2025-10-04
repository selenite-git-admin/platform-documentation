# Connector Catalog (Developer View)

## Purpose
The connector catalog is the single authoritative list of all available connectors in the platform.  
It provides developers, testers, and reviewers with a structured view of connector capabilities, supported versions, and lifecycle status.  
This document describes how the catalog is generated, what fields it contains, and how developers can use it for testing and validation.

## Scope
This catalog is focused on the **developer-facing view**.  
It includes technical details required for connector development, certification, and CI integration.  
It does not cover tenant-facing catalog presentation, which is part of the implementation and support documentation.  

The scope includes:
- How the catalog is built from connector manifests  
- What capability matrices are exposed  
- How connectors are grouped and filtered  
- How lifecycle and release channels are surfaced  
- How developers interact with catalog data during development and testing

## Catalog Generation
The catalog is automatically generated from connector manifests stored in the repository.  
Each connector method must publish a manifest, and the catalog build process validates, aggregates, and exports the results.

Steps:
1. Validate each manifest against the schema.  
2. Extract taxonomy, runtime, streams, and compliance data.  
3. Record lifecycle status and release channel.  
4. Publish aggregated catalog to the registry database and developer-facing documentation.  

The process ensures that no connector appears in the catalog unless it has a valid manifest and has passed validation checks.

## Catalog Structure
The catalog is structured by taxonomy fields.  
Connectors are grouped by **origin, source, provider, product, and method**.  

Example:
```
enterprise / erp / sap / s4hana / odata
enterprise / crm / salesforce / cloud / rest
enterprise / database / postgres / v15 / jdbc
public / datasets / edgar / sec / rest
```

Each catalog entry includes:
- Connector ID  
- Name and description  
- Supported runners (Lambda, Fargate, EC2, Glue)  
- Supported network patterns (VPN, PrivateLink, NAT, VPC endpoints)  
- Lifecycle status (stable, preview, deprecated)  
- Version and release channel  
- Streams count and discovery strategy  
- Compliance tags (PII, PCI, PHI)  
- Last certification date  

## Capability Matrix
The catalog also provides a capability matrix that allows developers to compare connectors.  
This matrix includes dimensions such as:
- Supported authentication methods  
- Supported runners  
- Supported network patterns  
- Incremental vs full refresh capability  
- Schema drift handling strategy  
- Certification status  

Example (simplified):

| Connector                  | Auth       | Runners           | Incremental | Drift Detection | Lifecycle |
|-----------------------------|------------|------------------|-------------|-----------------|-----------|
| SAP S4HANA OData            | OAuth2     | Lambda, Fargate  | Yes         | Yes             | Stable    |
| SAP ECC RFC                 | Basic Auth | Fargate, EC2     | Yes         | Partial         | Deprecated|
| Salesforce REST             | OAuth2     | Lambda           | Yes         | Yes             | Stable    |
| PostgreSQL JDBC             | User/Pass  | Fargate, Glue    | Yes         | Yes             | Preview   |

## Filtering and Navigation
Developers can filter the catalog by:
- Vendor (SAP, Salesforce, NetSuite)  
- Global connector type (File, Database, API, Streaming)  
- Lifecycle status (stable, preview, deprecated)  
- Compliance tags (PII, PCI, PHI)  
- Supported runner or network mode  

Example queries:
- “List all connectors that support AWS Lambda”  
- “List all connectors that handle PII”  
- “List all deprecated SAP connectors”  

## Lifecycle Surfacing
The catalog must surface lifecycle metadata clearly.  
- Stable connectors are marked as ready for production.  
- Preview connectors are marked as experimental with limited support.  
- Deprecated connectors are marked with retirement dates and replacement recommendations.  

Developers must be able to see at a glance whether a connector is safe to use in new builds.

## Developer Interaction
The catalog is not only a reference but also a tool for CI and testing.  
- CI pipelines query the catalog to validate that new connectors are correctly registered.  
- Developers use the catalog to confirm capability requirements before implementing new features.  
- Test harnesses use catalog metadata to select which connectors to run in regression suites.  

Examples:
- A regression pipeline may select all connectors tagged as `pii` for extra compliance testing.  
- A performance test may select all JDBC connectors to validate scaling behavior.  
- A deprecation pipeline may check for tenants still running deprecated versions.

## Principles
- The catalog is the single source of truth for all connector availability and capabilities.  
- Every connector entry must originate from a validated manifest.  
- Capability matrices must remain up to date with certification results.  
- Lifecycle metadata must always be visible and accurate.  
- Developers must rely on catalog queries for testing and validation instead of maintaining manual lists.  

## Relationships
- Connectors supply manifests that build the catalog.  
- The governance modules use the catalog to enforce compliance and policy rules.  
- The runtime modules use the catalog to validate runner and network compatibility.  
- The tenant-facing catalog is derived from this developer catalog, but simplified.  

## Exclusions
This document does not define how tenants browse connectors in the user interface.  
It also does not include onboarding instructions. The focus is on the developer-facing catalog for engineering and CI purposes.
