# Platform Modules

## Purpose
The platform is organized into Modules. Each Module represents an independent architectural unit with a clear boundary, a defined contract, and its own lifecycle. Modules can be developed, deployed, and replaced without impacting unrelated parts of the system.

## Structure
Modules are grouped into functional categories (Host, Compute, Data Storage, Consumption, Action, Security, Access, Trust, Runtime, Data Utilities). Each category contains one or more Modules that together cover all responsibilities of the platform.

- **Host Modules** — manage platform policies, data contracts, tenants, and lineage obligations.
- **Compute Modules** — ingest, normalize, transform, and publish Golden Data Points (GDPs) and KPIs.
- **Data Storage Modules** — provide governed storage layers for raw data, GDPs, KPIs, published outputs, and calendar alignment.
- **Consumption Modules** — expose data products through APIs, exports, webhooks, and catalogs.
- **Action Modules** — link KPIs to workflows and activate outcomes in external systems.
- **Security Modules** — provide perimeter security, gateway functions, and network protections.
- **Access Modules** — handle authentication, authorization, and subscription enforcement.
- **Trust Modules** — embed evidence, secrets, and encryption into the platform’s core.
- **Runtime Modules** — power execution with scheduling, messaging, observability, error handling, and metering.
- **Data Utilities Modules** — supply schema registry, discovery, and migration services.

## Navigation
Each Module has its own documentation with the following structure:
- **Overview** — purpose, scope, and boundaries
- **Contracts** — what it guarantees
- **Interfaces** — how other modules and apps connect
- **Lifecycle** — deployment, upgrades, and retirement
- **Operations** — monitoring, runbooks, and SLOs
- **Dependencies** — internal and external
- **Storage** — schemas and persistence, if any
- **Examples** — patterns of use
- **Changelog** — history of changes

Use this section to understand each Module in isolation and in relation to others.
