# Taxonomy and Naming

## Purpose
The taxonomy provides a structured way to classify every connector in the platform.  
Without a clear classification system, connectors would be difficult to manage, certify, and evolve.  
The taxonomy ensures that developers, operators, and governance processes all speak the same language when referring to connectors.

## Scope
This document describes the five layer classification model that applies to every connector.  
It also defines the naming conventions used in code, manifests, and documentation.  
The taxonomy applies equally to vendor specific connectors such as SAP RFC or Salesforce REST, and to global connectors such as File, API, or Database adapters.

## Five Layer Model
Every connector must be fully identified by five layers. These layers are hierarchical and together form a unique identity for a connector method.

### 1. Data Origin
This describes where the data fundamentally comes from.  
Typical values include:
- Enterprise: internal systems operated by the organization  
- Third party: external partners or SaaS systems  
- Public: open datasets such as EDGAR filings  

### 2. Data Source (System Type)
This describes the class of system.  
Typical values include:
- ERP  
- CRM  
- MES  
- HRMS  
- Database  
- File or Object Storage  
- API (REST, SOAP, GraphQL)  
- Streaming or Messaging systems  
- Public database or dataset  

### 3. Provider
This describes the vendor or product family.  
Examples include SAP, Salesforce, NetSuite, Odoo, Oracle EBS, Workday, Tally, PostgreSQL, or EDGAR.  
Global connectors may not have a vendor, in which case the provider is generic such as File, JDBC, or REST.

### 4. Product or Version
This identifies the product line or major release.  
For SAP this might be ECC or S4HANA.  
For Salesforce this might be Salesforce Cloud.  
For NetSuite this might be version 2024_2.  
For global connectors this may be omitted or replaced with format information such as CSV or Parquet.

### 5. Connection Method
This describes the specific mechanism by which data is accessed.  
Examples include RFC, OData, CDS, JDBC, ODBC, REST, SOAP, GraphQL, SFTP, manual upload, data dump, webhook, or log based CDC.  
The method is the most important unit of versioning and lifecycle, because it determines runtime dependencies and supported execution environments.

## Naming Conventions
To keep connector identities consistent across code, manifests, and documentation, the following conventions are enforced.

- **Connector Slug**  
  `conn::<origin>::<source>::<provider>::<product>::<method>`  
  Example: `conn::enterprise::erp::sap::sap_s4hana::odata`

- **Package Name**  
  `connector-<provider>-<product>-<method>`  
  Example: `connector-sap-s4hana-odata`

- **Manifest File Location**  
  `connectors/<provider>/<product>/<method>/manifest.yaml`  
  Example: `connectors/sap/s4hana/odata/manifest.yaml`

- **Documentation File Name**  
  Each connector method has its own markdown file.  
  Example: `sap-odata.md`  

These conventions ensure that the connector registry, the orchestrator, and the documentation system all align on the same identity.

## Principles
- A connector is only valid if all five taxonomy layers are declared in its manifest.  
- Each connector method is versioned and certified independently.  
- Folder and file naming must match manifest fields.  
- No connector is admitted into the catalog unless taxonomy validation passes in CI.  

## Relationships
The taxonomy integrates directly with other modules.  
The Governance Modules use taxonomy fields for policy enforcement, lineage, and compliance.  
The Runtime Modules use taxonomy fields to select runner profiles and schedule workloads.  
The Catalog uses taxonomy fields to group connectors, auto generate capability matrices, and present filters in the user interface.

## Exclusions
This taxonomy does not define GDP, KPI, or downstream data modeling conventions.  
It also does not prescribe naming conventions for tenant specific connection profiles.  
The focus here is only on the identity of connector artifacts at the development and lifecycle level.
