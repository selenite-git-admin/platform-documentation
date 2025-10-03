# Connectors Module

## Purpose
The Connectors Module defines how the platform integrates with external data sources.  
Connectors are the first step in the data lifecycle. They reach out to enterprise systems, third party applications, or public datasets, and extract data into the platform’s Bronze layer.  

The primary purpose of this module is to provide a contract driven and repeatable way to build and operate connectors. By enforcing common standards, every connector, whether it is an SAP RFC adapter, a Salesforce REST client, or a generic file ingester, behaves predictably and can be tested, monitored, and evolved over time.  

Connectors are intentionally thin adapters. They handle only authentication, discovery, extraction, and delivery. All business logic, KPI mapping, or domain specific calculations are excluded. This separation of concerns ensures that connectors remain stable even as downstream models evolve.

## Scope
This module documents the complete lifecycle of connectors from design to retirement. The scope includes taxonomy and naming conventions, connector architecture and SDK contracts, deployment options and network modes, manifest schema and validation rules, observability and testing standards, security and compliance requirements, versioning and lifecycle policies, vendor specific connectors such as SAP, Salesforce, or NetSuite, and global connectors such as file, object storage, database, or API adapters.  

By covering each of these dimensions, the Connectors Module provides a complete reference for development teams. It ensures that connectors remain consistent, secure, and maintainable across the platform.

## Principles
The design and implementation of connectors in this platform follow a clear set of principles.  

**Contract first development**  
Every connector must ship with a manifest that fully describes its taxonomy, capabilities, supported runners, and network patterns. This manifest is the source of truth for both developers and the orchestration layer.  

**Separation of concerns**  
Connectors are only responsible for extracting raw data from a source system. They do not apply business rules, transformations, or KPI logic. Those responsibilities belong to downstream compute and storage modules.  

**Independent lifecycle**  
Each connector and method combination is treated as an independent artifact. It is versioned, tested, and released on its own schedule. A change in one connector does not affect others.  

**Stateless execution**  
Connectors run as stateless processes. The orchestration layer is responsible for managing state, retries, and checkpoints. This ensures that connectors can be scaled, retried, or replaced without complex migration steps.  

**Governed evolution**  
Schema drift, authentication changes, or API deprecations are surfaced through compatibility alerts. Connectors evolve under explicit versioning rules so that tenants can plan migrations with confidence.

## Relationships
Connectors interact closely with other parts of the platform.  

They provide data to compute modules, where the Bronze layer is normalized, transformed, and published.  
They register metadata into governance modules, enabling policy enforcement and lineage tracking.  
They are executed through runtime modules, which provide scheduling, retries, error handling, and metering.  
They rely on security modules for credential management, network restrictions, and compliance enforcement.  

This tight integration ensures that connectors are governed components of a larger enterprise data system and not disposable scripts.

## Exclusions
This module does not cover business semantics such as GDP definitions, KPI mappings, or transformations. These are addressed in compute and storage modules.  
It does not cover tenant onboarding instructions for administrators such as entering credentials or scheduling runs. These belong in implementation and support documentation.  
It does not include end user troubleshooting guides. The focus here is strictly on connector design, development, and lifecycle management.

## Next Sections

- [Taxonomy and Naming](taxonomy.md)  
- [Connector Scope](connector-scope-streams.md)  
- [Architecture](architecture.md)  
- [Deployment Options](deployment-options.md)  
- [Manifest Schema](manifest-schema.md)  
- [Incremental State](incremental-state.md)  
- [Observability and Testing](observability-testing.md)  
- [Security and Compliance](security-compliance.md)  
- [Versioning and Lifecycle](lifecycle.md)  
- [Catalog (Dev)](catalog-dev.md)  

### Global Connectors
- [File](vendors/global-connectors/global-file.md)  
- [Object Store](vendors/global-connectors/global-object-store.md)  
- [Database (JDBC/ODBC)](vendors/global-connectors/global-db.md)  
- [REST API](vendors/global-connectors/global-api-rest.md)  
- [SOAP API](vendors/global-connectors/global-api-soap.md)  
- [GraphQL API](vendors/global-connectors/global-api-graphql.md)  
- [Webhook](vendors/global-connectors/global-webhook.md)  
- [Streaming](vendors/global-connectors/global-streaming.md)  

### Vendor Connectors

#### **SAP**  

  - [RFC](vendors/sap-connectors/sap-rfc.md)  
  - [OData](vendors/sap-connectors/sap-odata.md)  
  - [CDS](vendors/sap-connectors/sap-cds.md)  
  - [Database Dump](vendors/sap-connectors/sap-db-dump.md)  
  - [CPI](vendors/sap-connectors/sap-cpi.md)  
  - [Excel Upload](vendors/sap-connectors/sap-excel-upload.md)  

#### **Salesforce**  

  - [REST](vendors/salesforce-connectors/salesforce-rest.md)  
  - [Bulk API](vendors/salesforce-connectors/salesforce-bulk.md)  
  - [Streaming API](vendors/salesforce-connectors/salesforce-streaming.md)  

#### **NetSuite**    

  - [REST](vendors/netsuite-connectors/netsuite-rest.md)  
  - [REST-let](vendors/netsuite-connectors/netsuite-restlet.md)  
  - [SOAP](vendors/netsuite-connectors/netsuite-soap.md)  

#### **Workday**    

  - [REST](vendors/workday-connectors/workday-rest.md)  
  - [SOAP](vendors/workday-connectors/workday-soap.md)  
  - [RAAS](vendors/workday-connectors/workday-raas.md)  
  - [EIB](vendors/workday-connectors/workday-eib.md)  

#### **Tally**    
  
  - [ODBC](vendors/tally-connectors/tally-odbc.md)  
  - [XML](vendors/tally-connectors/tally-xml.md)  
  - [Backup Dump](vendors/tally-connectors/tally-backup-dump.md)  
  - [Reference](vendors/tally-connectors/tally-backup-ingestion.md)  

#### **Google**    

  - [Google Ads](vendors/google-connectors/google-ads.md)
  - [Google AdSense](vendors/google-connectors/google-adsense.md) 
  - [Google Analytics](vendors/google-connectors/google-analytics.md) 
  - [Google Search](vendors/google-connectors/google-search-console.md) 
  - [Google YouTube](vendors/google-connectors/google-youtube.md) 

#### **Meta**    

  - [Facebook Pages](vendors/meta-connectors/facebook-pages.md)
  - [Instagram Graph](vendors/meta-connectors/instagram-graph.md)
  - [Meta Ads](vendors/meta-connectors/meta-ads.md)
  - [Meta Conversions](vendors/meta-connectors/meta-conversions-api.md)

#### **EDGAR**    

  - [REST](vendors/edgar-connectors/edgar-rest.md)  
  - [XBRL](vendors/edgar-connectors/edgar-xbrl.md)  