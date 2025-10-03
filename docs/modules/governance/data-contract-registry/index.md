# Data Contract Registry

## Role in the Platform
Data Contract Registry owns dataset contracts across four layers: extraction, raw, gold, and activation. It ingests schema artifacts, versions them per dataset and per layer, selects a current version, and emits compatibility signals. It does not run human approval workflows. The schema artifact is the contract.

## Responsibilities
- Register datasets with ownership and lifecycle status
- Ingest schema artifacts per dataset and per layer
- Version schemas and mark one current per dataset per layer
- Classify changes for compatibility against the last version
- Publish read APIs for schemas, versions, and diffs
- Track consumer subscriptions by dataset and layer
- Emit signals when current changes or when a breaking change is detected

## Inputs
- Schema artifacts produced by connectors and pipelines
- Ownership and stewardship metadata
- Consumer subscriptions and required compatibility posture

## Outputs
- Current schema per dataset and layer with immutable history
- Diffs and compatibility classifications
- Events for downstream systems when current changes or breaks are detected

## Interfaces
- Read APIs for datasets, layers, versions, diffs, and subscriptions
- Write APIs for registration, schema ingest, and subscriptions
- Optional reference to Schema Registry for artifact storage and IDs

## Operational Behavior
- On ingest, compare the candidate artifact with the current version for the dataset and layer
- Classify compatibility and store a new version
- If the change is compatible, mark the new version current. If breaking, record and emit a signal for callers to act
- No side-channel conversations or approvals

## Constraints
- Does not store data rows or samples
- Does not perform identity or entitlement checks
- Does not schedule or execute jobs
- Avoids cyclic dependencies. Governance policies are evaluated outside this registry

## Examples in Action

Ingest extraction schema
A connector posts the SAP MARA feed schema to the extraction layer. The registry stores v1 and marks it current.

Advance gold schema
A modeling job posts an updated `materials.key_materials` schema to the gold layer. The registry classifies it as compatible and promotes v2 to current.

Activation schema for consumers
An Activation API reads the current activation schema for `materials.key_materials` and serves it to downstream applications.

## Module Documentation

[Data Model](data-model.md)
Entities, relationships, ERD placeholder, and DDL skeletons.

[UI](ui.md)
Screens, placement, API dependencies, and wireframe placeholders.

[API](api.md)
Operations, request and response schemas, idempotency, and errors.

[Observability](observability.md)
Metrics, logs, traces, dashboards, alerts, and SLOs.

[Runbook](runbook.md)
Operational procedures for incidents and routine tasks.

[Security](security.md)
Classification, access control, auditability, and safeguards.
