# Modules

## How to use this index
Start from a family, then drill into the module pages. Host is intentionally small. Governance and Data Utilities hold cross cutting capabilities. Avoid speculative scope; document only what is implemented or approved.

### Host Modules
[Tenant Management](host/tenant-management/index.md)
Onboard and manage tenant identity, lifecycle, residency, and routing tags.

[Platform Catalog](host/platform-catalog/index.md)
Infra and service knobs: regions, residency policies, environment codes, namespace prefixes, tag taxonomy, notification channels, escalation policies.

### Governance Modules
[Policy Registry](governance/policy-registry/index.md)
Central registry for guardrail policies.

Lineage Obligations (planned)
Location for lineage based governance rules.

### Data Utilities Modules
[Calendar Service](data-utilities/calendar-service/index.md)
Time semantics for the platform. Links: [Data Model](data-utilities/calendar-service/data-model.md), [API](data-utilities/calendar-service/api.md), [UI](data-utilities/calendar-service/ui.md), [Date Table](data-utilities/calendar-service/date-table.md), [Observability](data-utilities/calendar-service/observability.md), [Runbook](data-utilities/calendar-service/runbook.md), [Security](data-utilities/calendar-service/security.md).

[Data Contract Registry](data-utilities/data-contract-registry/index.md)
Contracts for extraction, raw, gold, and consumption layers.

Schema Registry (planned)
Engine agnostic schema evolution and compatibility checks.

Catalog and Discovery (planned)
Metadata and search across datasets and services.

Migration Service (planned)
Utilities for controlled data and schema migrations.

### Access Modules (planned)
Authentication, Authorization, Subscription Enforcement.

### Security Modules (planned)
Gateway, Network Security.

### Compute Modules (planned)
Ingestion, Normalization, KPI Build, Publish, Orchestration.

### Data Storage Modules (planned)
Raw Store, GDP Store, KPI Store, Published Store.

### Consumption Modules (planned)
Activation APIs, Exports, Webhooks, Catalog.

### Action Modules (planned)
Action Engine, Action Catalog, Action Delivery.

### Runtime Modules (planned)
Scheduler, Messaging and Events, Observability, Error Handling, Metering.
