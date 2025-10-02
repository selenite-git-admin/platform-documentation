# Platform modules

The platform is organized into clear **modules**.  
Each domain is a container that defines boundaries and scope, and lists the **modules** that implement its responsibilities.  
Modules are the independent architectural units: they expose APIs, manage contracts, own data where applicable, and meet SLOs.  
This separation ensures that responsibilities do not blur and that modules remain replaceable without ripple effects.

## Host Domain
The Host Domain provides authority. It owns the approval of data contracts, policy evaluation, tenant lifecycle, and lineage obligations.  
Modules here define what can and cannot enter the platform, but they do not execute jobs or store datasets.

- **Policy Engine Module** — Evaluates incoming requests against policy.  
- **Data Contract Registry Module** — Stores and versions data contracts.  
- **Tenant Management Module** — Governs onboarding, entitlements, and lifecycle.  
- **Lineage Obligations Module** — Declares evidence and lineage rules.

## Compute Domain
The Compute Domain transforms data. It ingests raw feeds, normalizes formats, builds GDP and KPI datasets, and publishes governed outputs.  
It is stateless by design, with outputs always written to Data Storage modules.

- **Ingestion Module** — Captures source data into Raw Store.  
- **Normalization Module** — Aligns types, keys, and structure.  
- **KPI Build Module** — Applies contract rules to construct KPI datasets.  
- **Publish Module** — Delivers governed products into Published Store.  
- **Orchestration Module** — Coordinates workflows, dependencies, and retries.

## Data Storage Domain
The Data Storage Domain persists all governed datasets.  
It is the only authority for storing data at each stage: raw, GDP, KPI, and published.

- **Raw Store Module** — Immutable landing of source data.  
- **GDP Store Module** — Stores Golden Data Points under contract.  
- **KPI Store Module** — Stores contract-built metrics and dimensions.  
- **Published Store Module** — Holds consumption-ready, versioned datasets.

## Consumption Domain
The Consumption Domain exposes data outward. It provides APIs, exports, webhooks, and catalogs for downstream users and systems.  
It does not alter datasets; its job is controlled distribution.

- **Activation APIs Module** — Serves governed APIs.  
- **Exports Module** — Generates file-based or batch outputs.  
- **Webhooks Module** — Pushes events and updates externally.  
- **Catalog Module** — Lists published products with metadata.

## Action Domain
The Action Domain links insights to outcomes. It hosts engines that trigger business workflows based on governed data, closing the loop between numbers and action.

- **Action Engine Module** — Runs playbooks tied to KPI thresholds.  
- **Action Catalog Module** — Defines reusable action templates.  
- **Action Delivery Module** — Connects to external systems to execute actions.

## Application Domain
The Application Domain provides user-facing applications. It does not generate or store data, but surfaces platform functions to administrators and customers.

- **Admin App Module** — Manages tenants, policies, and operations.  
- **Customer App Module** — Provides dashboards and self-service data access.

## Security Domain
The Security Domain enforces perimeter security. It ensures that only authenticated and verified traffic enters, and that data is protected in transit.

- **Gateway Module** — Controls ingress, egress, and rate limiting.  
- **Network Security Module** — Provides network isolation and TLS enforcement.

## Access Domain
The Access Domain governs identity and permissions.  
It authenticates users and services and enforces authorization rules.

- **Authentication Module** — Validates identity claims.  
- **Authorization Module** — Enforces role and entitlement checks.

## Trust Domain
The Trust Domain provides assurance. It manages audit evidence, secrets, and encryption, ensuring that data and operations are provable, confidential, and compliant.

- **Evidence Ledger Module** — Records actions and approvals immutably.  
- **Secrets Module** — Manages credentials and keys.  
- **Encryption Module** — Provides encryption at rest and in transit.

## Runtime Domain
The Runtime Domain is the execution backbone.  
It handles scheduling, messaging, error management, and observability across all modules.

- **Scheduler Module** — Runs recurring and ad-hoc jobs.  
- **Messaging and Events Module** — Provides queues and event topics.  
- **Observability Module** — Metrics, logs, and traces.  
- **Error Handling Module** — Retries, DLQs, and compensations.

## Data Utilities Domain
The Data Utilities Domain supports schema, discovery, and migration.  
It ensures that schemas are defined, cataloged, and versioned, and that data can move safely across versions.

- **Schema Registry Module** — Stores and governs all schemas.  
- **Catalog and Discovery Module** — Provides search and metadata.  
- **Migration Service Module** — Manages schema and dataset migrations.

Together, these modules and their modules ensure that the platform is consistent, auditable, and actionable from raw data to governed actions.
