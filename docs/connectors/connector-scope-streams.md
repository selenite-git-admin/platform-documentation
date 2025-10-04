# Reference: Connector Scope and Stream Discovery

## Purpose
This reference explains how connectors should be scoped and how streams are discovered and managed.  
Connectors are the entry point to the platform. If their responsibilities are unclear, the system will accumulate technical debt, with duplication of logic across connectors, pipelines, and governance modules.  
This document establishes a single model for connector scope and stream discovery so that developers, operators, and governance teams work against the same expectations.

## Connector Scope
A connector represents a **source system and access method**, not an individual table or object.  
Connectors are designed to be stable building blocks. They do not change when a new table appears or when a tenant wants to onboard an additional object. Instead, the connector remains the same, and the registry records new streams.

Examples:
- **SAP S4HANA OData** connector: fetches data from SAP via OData services. It can expose multiple streams such as `sap.s4hana.gl_accounts`, `sap.s4hana.customers`, and `sap.s4hana.sales_orders`.  
- **SAP ECC RFC** connector: fetches data from SAP ECC via RFC calls. It may expose streams like `sap.ecc.bseg` and `sap.ecc.bkpf`.  
- **Salesforce REST** connector: fetches Salesforce objects such as `sf.account`, `sf.opportunity`, or `sf.contact`.  
- **PostgreSQL JDBC** connector: lists all accessible tables and views in the schema, such as `jdbc.public.customers` or `jdbc.sales.invoices`.  

In all of these cases, one connector handles many streams. You never create a separate connector for each table.

## Stream Discovery
Connectors must implement a **discovery function** that lists available streams. This is a core requirement of the connector SDK.  
At run time, discovery populates the **stream catalog**, which is compared with the registry.

Examples:
- JDBC: `discover()` queries the system catalog to return all tables and views with their column definitions.  
- OData: `discover()` queries the `$metadata` endpoint to list entity sets.  
- Salesforce: `discover()` calls the `describeGlobal()` API and then `describeSObject()` for each object.  
- File/Object Store: `discover()` lists files matching a configured pattern, such as `s3://bucket/invoices/*.csv`. Each pattern is treated as a stream.  

The connector then emits a structured catalog:
```yaml
streams:
  - id: sap.s4hana.gl_accounts
    key: [AccountID]
    cursor: LastUpdated
  - id: sap.s4hana.customers
    key: [CustomerID]
    cursor: UpdatedOn
```

## Stream Identity
Stream identifiers must be **stable, unique, and human readable**. They follow a `<namespace>.<entity>` format. The namespace derives from the provider and product.  

Examples:
- `sap.s4hana.gl_accounts`  
- `sap.ecc.bseg`  
- `sf.opportunity`  
- `jdbc.public.customers`  
- `file.s3.sales_orders_csv`  

This stability is important. If a table is renamed at the source, the registry still keeps the old stream id mapped to the new schema. This avoids breaking downstream models unexpectedly.

## Stream Selection
Not all streams are relevant for a tenant. Selection filters allow administrators to control what is ingested.

Example selection configuration:
```yaml
stream_selection:
  mode: discovery
  include: ["sap.s4hana.*", "sf.(account|opportunity)"]
  exclude: ["*.audit*", "*.tmp*"]
  limit: 200
```

This allows a tenant to pull only SAP general ledger accounts and Salesforce accounts and opportunities, while excluding audit and temporary tables.

## Keys, Cursors, and Schemas
Connectors must declare enough metadata to support idempotent and incremental reads.

### Keys
- JDBC connectors read primary keys from the catalog. If missing, they require explicit config.  
- Salesforce connectors use the `Id` field automatically provided by the platform.  
- File connectors generate synthetic keys (file path + row number).  

### Cursors
- SAP OData may use `LastUpdated` or `ChangeTimestamp`.  
- Salesforce may use `SystemModstamp`.  
- JDBC may use an `updated_at` column, if configured.  
- If no cursor exists, connectors fall back to full refresh.  

### Schemas
- Connectors emit schema definitions at discovery.  
- Schemas are stored in the **schema_registry** with versioning.  
- Manifests declare the schema strategy (discovery or reference) but do not embed the full schema inline.  

Example manifest fragment:
```yaml
streams:
  strategy: discovery
  selection:
    include: ["sap.s4hana.*"]
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
  validation:
    required_keys: true
    allow_type_promotions: [int->long, float->double]
    forbid_field_removals: true
```

## Registry Responsibilities
The platform, not the connector, owns validation and governance. Registries are the system of record.

- **stream_registry**: holds the catalog of streams and their schema hashes.  
- **schema_registry**: stores JSON Schema or Avro definitions, with versioning and compatibility checks.  
- **mapping_registry**: ensures GDP and KPI mappings are still resolvable.  
- **policy_registry**: applies governance checks such as PII tagging or residency constraints.  
- **compat_alerts**: records drift events and their downstream impact.  

Connectors never enforce these rules. They only emit data. Registries validate and control promotion of schemas.

## Principles
- One connector per source and method, not per table.  
- Many streams per connector, discovered dynamically.  
- Stream identities must be stable and human readable.  
- Schemas must be discovered and registered, not embedded inline.  
- Validations and governance are performed in registries, not inside connectors.  
- Bronze layer always lands data as-is. Failures occur at Silver mapping or policy enforcement.  

## Exclusions
This reference does not describe GDP or KPI mapping.  
It does not cover tenant onboarding or support playbooks.  
Its sole focus is the developer-facing model for connector scope and stream discovery.
