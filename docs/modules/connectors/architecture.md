# Connector Architecture

## Purpose
The architecture defines how connectors are designed and how they interact with the platform.  
Connectors must not be ad hoc scripts. They are governed artifacts that follow consistent contracts, packaging rules, and lifecycle processes.  
This section explains the core components that make a connector predictable, testable, and maintainable.

## Scope
This document covers the architecture of connectors at the development level.  
It defines the standard SDK contracts that every connector must implement, the role of the manifest, the packaging and deployment requirements, and how connectors interact with the orchestrator.  
It also describes the state and registry components that track connector runs and versions.

## Connector Responsibilities
A connector performs a limited set of responsibilities:
- Authenticate to the source system  
- Discover available entities or streams  
- Read data from one or more entities, either in batch or incrementally  
- Emit records in a uniform format to the Bronze layer  
- Report metrics and structured errors  

A connector does not perform business logic, KPI calculations, or downstream transformations. These responsibilities belong to compute and storage modules.

## SDK Contracts
All connectors are implemented using a shared SDK.  
The SDK defines the following required functions:

- **authenticate()**  
  Establishes a session with the source system. Supports multiple methods such as OAuth2, basic authentication, API keys, or SAML based tokens.  

- **discover()**  
  Returns a list of entities or streams that the connector supports, including schemas, primary keys, and cursor fields.  

- **read(stream, since, cursor)**  
  Extracts records from the source system. Supports both batch and incremental reads. Returns records along with updated state information.  

- **checkpoint(state)**  
  Persists the connector’s state in the orchestrator’s registry so that runs can resume incrementally.  

- **emit(records)**  
  Delivers records to the Bronze layer in a standard envelope format.  

Connectors may also implement optional hooks such as health checks, schema drift detection, or cost estimation.  

## Manifest
Every connector must include a manifest file.  
The manifest declares identity, taxonomy, capabilities, supported runners, network patterns, streams, and compliance metadata.  
The manifest is used by the catalog, the orchestrator, and the governance modules as the source of truth.  
No connector is admitted into the platform without a valid manifest.

## Packaging
Each connector method is packaged as an independent artifact.  
Packaging rules require:
- One artifact per connector method  
- Semantic versioning in the artifact name and manifest  
- Distribution in a container image or equivalent runtime package  
- Dependencies bundled with the artifact to avoid runtime failures  

Artifacts are published through the connector catalog and can be rolled back independently.

## Orchestrator Interaction
The orchestrator manages the lifecycle of connector runs.  
It performs scheduling, launches the appropriate runner, injects secrets, and manages retries.  
The orchestrator also collects metrics, logs, and state checkpoints.  
Connectors must remain stateless. Any attempt to persist state locally is considered a violation.

## Registry Tables
The following registries support connector architecture:
- **connector_definitions**: lists all available connectors and their versions  
- **tenant_connections**: maps tenants to the connectors they have onboarded  
- **connector_runs**: records every run, its status, metrics, and cost  
- **connector_run_state**: stores incremental state for each stream  
- **stream_registry**: tracks entity schemas and versions  
- **compat_alerts**: records schema drift and other compatibility warnings  

These registries provide observability, governance, and safe upgrade paths.

## Principles
- All connectors must implement the SDK contracts fully.  
- All connectors must provide a manifest that passes schema validation.  
- Connectors must be stateless and idempotent.  
- Packaging must allow independent deployment and rollback.  
- Orchestrator and registry integration is mandatory.

## Relationships
Connector architecture interacts directly with:
- The Runtime Modules, which provide the execution environment  
- The Governance Modules, which enforce policy through manifest metadata  
- The Catalog, which exposes certified connectors to tenants  
- The Security Modules, which manage secrets and credentials  

## Exclusions
This architecture does not describe tenant onboarding flows, which belong to implementation documentation.  
It does not define downstream GDP or KPI mapping, which is covered in compute and storage modules.
