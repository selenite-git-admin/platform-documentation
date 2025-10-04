# Manifest Schema

## Purpose
The manifest is the central contract for every connector.  
It describes what the connector is, what it can do, and how it must be executed.  
The orchestrator, governance modules, and catalog all rely on the manifest as the single source of truth.  
Without a manifest, a connector cannot be certified, deployed, or exposed to tenants.

## Scope
This document defines the schema that every connector manifest must follow.  
It specifies mandatory fields, optional fields, validation rules, and usage scenarios.  
The schema applies to all connector types including vendor specific connectors and global connectors.  
It is enforced in CI to prevent incomplete or inconsistent connectors from entering the catalog.

## Structure
A manifest is written in YAML.  
It is divided into clear sections that describe identity, taxonomy, runtime, and compliance.  
The schema is versioned so that future changes can be introduced without breaking existing connectors.

### Top Level Fields
- **manifest_version**  
  The version of the manifest schema. Used to manage backward compatibility.  

- **id**  
  A unique identifier for the connector method. Must align with taxonomy and naming conventions.  

- **name**  
  A human readable name. Example: "SAP S4HANA OData Connector".  

- **description**  
  A short description of the connector’s purpose.  

- **tags**  
  Keywords for search, filtering, and governance classification.  

### Taxonomy Section
- **origin**  
  Values include enterprise, third_party, or public.  

- **source**  
  The system class such as ERP, CRM, MES, Database, File, or API.  

- **provider**  
  Vendor or product family such as SAP, Salesforce, or NetSuite.  

- **product**  
  Product line or version such as ECC, S4HANA, or Salesforce Cloud.  

- **method**  
  The specific connection method such as RFC, OData, JDBC, or REST.  

### Runtime Section
- **supported_runners**  
  A list of runners where this connector can execute. Examples: lambda, fargate, ec2, glue.  

- **network_patterns**  
  Supported networking options such as vpn, private_link, vpc_endpoint, or nat_allowlist.  

- **dependencies**  
  Required libraries or drivers. Example: `pyodbc>=4.0`.  

- **timeout**  
  Recommended execution timeout in seconds.  

- **max_parallelism**  
  Maximum supported concurrent streams.  

### Streams Section
- **entities**  
  List of entities or tables the connector can extract. Each entity includes a name, schema, primary key, cursor field, and whether incremental extraction is supported.  

### Compliance Section
- **sensitive_data**  
  Flags for whether the connector can handle PII, PCI, or PHI.  

- **security_controls**  
  Requirements for credential handling such as KMS, Secrets Manager, or HashiCorp Vault.  

- **data_residency**  
  Geographic constraints if any.  

### Example Manifest

```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::erp::sap::sap_s4hana::odata
name: SAP S4HANA OData Connector
description: Extracts master and transactional data from SAP S4HANA using OData services.
tags:
  - sap
  - erp
  - odata
taxonomy:
  origin: enterprise-connectors
  source: erp
  provider: sap
  product: s4hana
  method: odata
runtime:
  supported_runners:
    - lambda
    - fargate
  network_patterns:
    - private_link
    - vpn
  dependencies:
    - requests>=2.31
  timeout: 900
  max_parallelism: 5
streams:
  - name: GLAccounts
    primary_key: AccountID
    cursor_field: LastUpdated
    schema: {...}
    incremental: true
compliance:
  sensitive_data: pii
  security_controls: secrets_manager
  data_residency: in-region-only
```

## Principles
- Every connector must have a manifest and it must pass validation before release.  
- The manifest must declare taxonomy fields completely.  
- Supported runners and network patterns must match real tested capabilities.  
- Compliance metadata must be explicit so that governance policies can be enforced.  
- The manifest is immutable once published. Changes require a new version.  

## Relationships
- The orchestrator reads manifests to launch connectors in the correct runner and network mode.  
- The governance modules use manifests to check compliance with security and data residency requirements.  
- The catalog displays manifest data to tenants during onboarding.  
- CI pipelines use manifests to validate, test, and certify connector artifacts.  

## Exclusions
The manifest schema does not define downstream mapping to GDP, KPI, or transformation layers.  
It also does not cover tenant specific configuration such as credentials or schedules.  
Those aspects are handled during onboarding and support, not in connector development.
