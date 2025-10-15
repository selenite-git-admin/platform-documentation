# Modules Framework

The DataJetty platform is organized into modular families, each with a clear boundary of responsibility.  
Every family encapsulates a specific capability area such as data ingestion, storage, governance, quality, activation, or intelligence, and exposes declarative interfaces to the rest of the system.  

This framework explains how the platform’s business value is realized through technical composition.  
It is written for developers and architects who need to understand how DataJetty works as a unified but decoupled system.

## Platform Overview

DataJetty is a metadata-driven, contract-first data intelligence platform.  
Its design objective is to give enterprises a governed, high-trust, and low-engineering environment where data flows from source systems to executive intelligence without manual effort.

Every capability in DataJetty - authentication, acquisition, validation, prediction, and delivery - is implemented as a module within one of the defined families.  
These modules are independently deployable and registered in metadata catalogs for discoverability and orchestration.

| Plane | Families | Role |
|-------|-----------|------|
| Core Plane | Core | Provides security, encryption, identity, and consistency across all components. |
| Control Plane | Platform Subscription, Platform Control, Platform Operations | Defines tenants, governance, and runtime policies. |
| Data Plane | Data Acquisition, Data Store, Data Quality, Data Intelligence, Data Activation | Moves, processes, validates, and operationalizes data. |

Each plane communicates through declared contracts and evidence records so that both data and control are verifiable end to end.

## Business Perspective  -  How Value Is Delivered

| Business Value | Delivered By | Description |
|----------------|--------------|-------------|
| Trust | Core + Platform Control + Data Quality | Establishes verifiable security, data lineage, and quality assurance. |
| Speed and Automation | Data Acquisition + Data Store + Data Activation | Provides fast, declarative data ingestion and distribution pipelines with zero manual ETL. |
| Insight and Predictive Foresight | Data Intelligence | Powers automated anomaly detection, forecasting, and executive-level insights. |
| Governance and Compliance | Platform Subscription + Platform Operations | Enforces tenant isolation, licensing, entitlements, and operational consistency. |

Each family represents a part of the enterprise contract with the customer. Together they make DataJetty’s business-first, compliance-assured architecture operational.

## Technical Perspective  -  How Workflows Operate

DataJetty functions as a governed data pipeline with distinct boundaries of control, data, and evidence.  
Each request or job moves through deterministic steps controlled by metadata.

```
User or API Request
   ↓
Core → Platform Families → Data Families
(Auth)   (Subscription + Control + Operations)   (Acquisition → Store → Quality → Intelligence → Activation)
```

1. Core authenticates and authorizes every request.  
2. Platform Subscription validates tenant context and entitlements.  
3. Platform Control provides schemas, policies, and contractual metadata.  
4. Platform Operations routes and secures runtime execution.  
5. Data Acquisition ingests datasets through configured connectors and runners.  
6. Data Store transforms and persists data across Bronze, Silver, Gold, and GDP layers.  
7. Data Quality validates and certifies datasets against declared contracts.  
8. Data Intelligence performs analytics, forecasting, and anomaly detection.  
9. Data Activation delivers curated datasets and insights to business applications.  
10. Evidence Ledger captures proofs for every critical operation.

## Interaction Model

### Control Plane
Defines who (tenants and users) and what (policies, contracts, schemas).  
Manages registry-based governance and runtime enforcement.  
Records lineage and evidence for every controlled entity.

### Data Plane
Handles how data moves and transforms.  
Includes ingestion, persistence, validation, and utilization.  
Operates in declarative mode - no custom ETL or hard-coded flows.

### Evidence Plane
Spans across both planes.  
Every data or operational event emits verifiable evidence into the Evidence Ledger.  
Enables auditability, replay, and compliance alignment.

## Design Principles Shared by All Families

- Metadata over code.  
- Contract-driven integration.  
- Audit by design.  
- Tenant isolation.  
- Composable architecture.  
- Predictable observability.  
- Declarative execution.

## Module Families Summary

| Family                | Description                                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Core                  | Foundational services for authentication, authorization, encryption, network policy, UUID generation, and error management. |
| Platform Subscription | Manages tenants, subscriptions, and entitlements. Defines plans, usage limits, and runtime enforcement.                     |
| Platform Control      | Governance backbone managing master data, policies, contracts, schemas, lineage obligations, and evidence.                  |
| Platform Operations   | Executes policies in real time, managing gateway routing, notifications, migrations, and health checks.                     |
| Data Acquisition      | Ingests external data from ERP, CRM, API, and file-based sources. Registers metadata in the control plane.                  |
| Data Store            | Maintains curated datasets in PostgreSQL-based layers. Implements declarative merges, retention, and audits.                |
| Data Quality          | Validates and monitors datasets for accuracy and SLA adherence. Records validation results as structured evidence.          |
| Data Intelligence     | Runs analytical and predictive workloads using governed data from the store.                                                |
| Data Activation       | Delivers verified outputs to systems, dashboards, and workflows. Converts insights into actions.                            |

## Example Flow  -  CFO KPI Dashboard Refresh

1. Core verifies credentials and retrieves tenant identity.  
2. Platform Subscription confirms entitlement to the Financial Intelligence pack.  
3. Platform Control fetches schemas and KPI definitions.  
4. Data Acquisition ingests SAP FI/CO transactions.  
5. Data Store merges new data into Silver and Gold layers.  
6. Data Quality validates completeness and reconciliation balance.  
7. Data Intelligence forecasts liquidity and margin trends.  
8. Data Activation updates the CFO dashboard and issues variance alerts.  
9. Evidence Ledger logs dataset freshness, validation results, and forecast IDs.

## Developer Guidance

- Identify the correct family before coding.  
- Register schema, policy, or KPI metadata before implementation.  
- Inter-family calls must go through schema or policy registries.  
- Emit evidence for every significant event.  
- Use runners, schedulers, and runtime modules instead of loops.  
- Respect tenant boundaries at all times.  
- Treat families as domain packages, not folders.

## Guardrails

These rules define what must not be violated when extending or integrating the platform.  
They protect integrity, traceability, and consistency across all modules.

### Architecture Boundaries
- Do not bypass registries or APIs when calling between families.  
- No direct writes into another module’s store.  
- No circular dependencies; communication occurs only through metadata or events.  
- All cross-family coordination happens via declarative contracts.

### Data and Schema Handling
- Schema evolution only through the Schema Registry.  
- No manual DDL or DML outside migration services.  
- Every dataset must have a contract ID and schema hash.  
- GDP and KPI layers are immutable except through controlled merges.

### Execution and Runtime
- No polling or long-running loops inside modules.  
- No direct file system access for ingestion or transformation.  
- All errors must propagate through the Error Handling module with trace IDs.  
- Logs must use the unified event structure with type, entity, status, and trace reference.

### Governance and Evidence
- Every operation emits evidence with operation ID, actor, hash, output reference, and timestamp.  
- No bypass of policy enforcement or subscription rules.  
- Credentials and tokens must be managed only by the Secrets module.  
- Absence of evidence means non-compliance.

### Security and Compliance
- Encryption at rest and in transit is mandatory.  
- Internal registries are never exposed externally.  
- Tenant-aware isolation is mandatory at data level.  
- Audit and compliance logs are append-only.

### Development Discipline
- Schema or policy registration precedes module creation.  
- Configuration belongs in Config or Policy registries, not environment variables.  
- Extend modules via metadata, not forks or copies.  
- Unit tests must verify metadata integrity and contract compliance.

## Summary

The Modules Framework converts DataJetty’s product vision into an executable architecture.  
Each family behaves as a self-contained service governed by contracts and evidence.  
Together they ensure the platform remains consistent in purpose:  
- business-first semantics
- technical precision
- audit by design
