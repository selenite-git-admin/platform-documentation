# Platform Governance

The **Platform Governance** family defines the control plane of DataJetty.  
It maintains the registries, policies, schemas, and evidentiary records that govern how data moves, evolves, and complies within the platform.  
These modules form the authoritative reference layer for lineage, schema integrity, and contractual consistency between producing and consuming systems.

Platform Governance does not process business data directly.  
Instead, it describes and validates how data must be handled across runtime environments.  
It provides policy resolution, contract registration, and immutable evidence recording for every governed action.  
This layer ensures that compliance, lineage, and traceability remain verifiable across all operational layers.

### Functional Coverage

- Defines and enforces governance policies, contracts, and schemas across the platform.  
- Manages canonical master data and shared reference sets.  
- Hosts registries for policies, data contracts, and schema definitions.  
- Tracks lineage obligations and records immutable evidence for audit and compliance.  
- Integrates governance decisions into runtime and quality planes for live enforcement.  
- Publishes authoritative metadata for acquisition, store, and intelligence modules.  
- Maintains business calendars and scheduling windows for jobs and reporting systems.

### Core Documents

[Governance Overview](governance-overview.md)  
Defines the role, scope, and principles of governance across the DataJetty platform.

[Governance Policies](governance-policies.md)  
Describes how policies are authored, versioned, tested, and published as executable governance logic.

[Governance Enforcement](runtime-governance-enforcement.md)  
Explains how governance decisions are enforced in real time during runtime execution.

[Governance Integrations](governance-integrations/index.md)  
Outlines integration points with Data Quality, Runtime, and Evidence Ledger layers.

### Modules

[Master](master/index.md)  
Maintains reference and dimensional master data used across modules for consistent lookups and joins.

[Policy Registry](policy-registry/index.md)  
Maintains access and operational policies that guide execution, visibility, and compliance enforcement.

[Data Contract Registry](data-contract-registry/index.md)  
Stores and versions producer–consumer interface contracts that describe expected data and event shapes.

[Schema Registry](schema-registry/index.md)  
Tracks schema evolution, validates compatibility, and manages change propagation for all structured datasets.

[Lineage Obligations](lineage-obligations/index.md)  
Defines required lineage checkpoints and compliance rules for datasets and pipelines.

[Evidence Ledger](evidence-ledger/index.md)  
Captures immutable proofs of contract adherence, data validation, and SLA compliance events.

[Calendar Service](calendar-service/index.md)  
Provides business and fiscal calendars, scheduling windows, and blackout periods for orchestration and reporting systems.
