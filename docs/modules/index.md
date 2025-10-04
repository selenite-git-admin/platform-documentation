# Modules

## Purpose
Modules describe the core building blocks of the BareCount Data Action Platform. Each module owns a clear responsibility and integrates with Pipelines, which are the backbone of the platform. The goal is a consistent, governed path from source data to activated outcomes.

## Context
Enterprises face fragmented tools and undocumented handoffs. BareCount standardizes the data lifecycle through Pipelines, while Modules provide the platform capabilities that feed, govern, execute, store, expose, and secure those pipelines. Every module below explains its role and how it connects to Pipelines so that teams can reason about the whole system, not just parts.

## Pipelines as the Backbone
Pipelines define the lifecycle of data from ingestion and raw capture to GDP, KPI, and publication. All modules either feed pipelines, constrain them with governance, execute them with runners, store their checkpoints, expose their outputs, or secure and observe their operation.
See Pipelines for the full lifecycle and stage details: [Pipelines](../pipelines/index.md)

## Module Families

### Host
Provides the administrative surface for the platform. Hosts tenants, catalogs, and operational controls.

How it connects to Pipelines
- Tenant creation, connector onboarding, and resource assignment prepare streams that feed ingestion
- Platform Catalog exposes pipeline, contract, and dataset metadata for operators and auditors

Start here:
- [Host Overview](host/index.md)
- [Platform Catalog](host/platform-catalog/index.md)
- [Tenant Management](host/tenant-management/index.md)

### Governance
Defines and enforces policies that make pipelines trustworthy.

How it connects to Pipelines
- Data Contract Registry validates extractor schemas during ingestion
- Policy Registry and Lineage Obligations set blocking and warning rules for pipeline runs

Start here:
- [Governance Overview](governance/index.md)
- [Policy Registry](governance/policy-registry/index.md)
- [Data Contract Registry](governance/data-contract-registry/index.md)
- [Lineage Obligations](governance/lineage-obligations/index.md)

### Runners
Provides execution contexts for pipelines. Abstracts AWS Lambda, Fargate, Glue, and EC2 so logic remains portable.

How it connects to Pipelines
- Pipeline manifests select runner type and network profile
- Orchestration triggers runs on the chosen runners with consistent observability and evidence

Start here:
- [Runners Overview](runners/index.md)
- [Ingestion Runner](runners/ingestion/index.md)
- [Normalization Runner](runners/normalization/index.md)
- [KPI Build Runner](runners/kpi-build/index.md)
- [Publish Runner](runners/publish/index.md)
- [Orchestration Runner](runners/orchestration/index.md)

### Data Storage
Implements durable stores for each pipeline checkpoint to preserve lineage and reproducibility.

How it connects to Pipelines
- Raw Store captures immutable ingested data
- GDP Store holds conformed entities
- KPI Store and Published Store expose governed outputs to consumers
- Calendar provides reusable time scaffolding for backfills and KPI windows

Start here:
- [Storage Overview](storage/index.md)
- [Raw Store](storage/raw-store/index.md)
- [GDP Store](storage/gdp-store/index.md)
- [KPI Store](storage/kpi-store/index.md)
- [Published Store](storage/published-store/index.md)
- [Calendar](storage/gdp-calendar/index.md)

### Consumption
Delivers pipeline outputs to applications and users.

How it connects to Pipelines
- Activation APIs, exports, and webhooks publish GDP and KPI products from the Published Store
- Catalog provides searchable access to datasets and versions produced by pipelines

Start here:
- [Consumption Overview](consumption/index.md)
- [Activation APIs](consumption/activation-apis/index.md)
- [Exports](consumption/exports/index.md)
- [Webhooks](consumption/webhooks/index.md)
- [Catalog](consumption/catalog/index.md)

### Action
Turns pipeline outputs into enterprise actions.

How it connects to Pipelines
- Action Engine consumes KPI events and thresholds
- Action Delivery pushes outcomes to enterprise systems for follow up

Start here:
- [Action Overview](action/index.md)
- [Action Engine](action/action-engine/index.md)
- [Action Catalog](action/action-catalog/index.md)
- [Action Delivery](action/action-delivery/index.md)

### Security
Applies platform security controls to pipeline execution and data access.

How it connects to Pipelines
- Gateway secures API access to pipeline products
- Network Security enforces runner connectivity choices such as PrivateLink and VPN

Start here:
- [Security Overview](security/index.md)
- [Gateway](security/gateway/index.md)
- [Network Security](security/network-security/index.md)

### Access
Controls identity and permissions for people and systems interacting with pipelines.

How it connects to Pipelines
- Authentication and Authorization protect pipeline APIs, manifests, and outputs
- Subscription Enforcement ties tenant entitlements to pipeline features

Start here:
- [Access Overview](access/index.md)
- [Authentication](access/authentication/index.md)
- [Authorization](access/authorization/index.md)
- [Subscription Enforcement](access/subscription-enforcement/index.md)

### Trust
Provides integrity guarantees and operational secrets for pipeline runs.

How it connects to Pipelines
- Evidence Ledger records lineage and evidence for every stage
- Secrets and Encryption secure credentials and data at rest and in transit

Start here:
- [Trust Overview](trust/index.md)
- [Evidence Ledger](trust/evidence-ledger/index.md)
- [Secrets](trust/secrets/index.md)
- [Encryption](trust/encryption/index.md)

### Runtime
Delivers shared platform services that keep pipelines reliable.

How it connects to Pipelines
- Scheduler and Messaging coordinate runs and events
- Observability, Error Handling, and Metering provide health, reliability, and cost signals

Start here:
- [Runtime Overview](runtime/index.md)
- [Scheduler](runtime/scheduler/index.md)
- [Messaging and Events](runtime/messaging-events/index.md)
- [Observability](runtime/observability/index.md)
- [Error Handling](runtime/error-handling/index.md)
- [Metering](runtime/metering/index.md)

### Data Utilities
Provides shared reference data and helpers that pipelines depend on.

How it connects to Pipelines
- Calendar Service standardizes fiscal calendars, holidays, and working days for backfills and KPI windows

Start here:
- [Data Utilities](data-utilities/index.md)
- [Calendar Service](data-utilities/calendar-service/index.md)

## Notes
Treat Pipelines as the backbone of BareCount. Design and review every module in terms of how it supplies, governs, executes, stores, exposes, or secures pipeline work. This alignment keeps the platform coherent and auditable end to end.
