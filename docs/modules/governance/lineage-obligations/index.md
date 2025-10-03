# Lineage Obligations

## Role in the platform
Lineage Obligations evaluates whether data movement and transformation respect declared guardrails. It observes lineage produced by pipelines, relates it to contracts and policies, and records evaluation results that other modules can read.

## Responsibilities
- Ingest lineage events about assets and runs
- Maintain a lineage graph per tenant
- Express obligations that target assets or runs by scope and tags
- Evaluate obligations against lineage and record results
- Expose APIs to query graph, obligations, and evaluations
- Emit change events when obligations or evaluations change state

## Non goals
- Does not author data contracts. Use Data Contract Registry
- Does not store business data. Stores metadata and evaluation results only
- Does not perform access control. Access Modules enforce authn and authz

## Inputs
- Lineage events from compute and orchestration modules
- Contracts and tags from Data Contract Registry
- Policies from Policy Registry

## Outputs
- Lineage graph nodes and edges scoped by tenant
- Obligation evaluation results with pass or fail state
- Events for consumers that react to failures

## Interfaces
- Read APIs for graph traversal and evaluations
- Write APIs for lineage event ingestion and obligation authoring
- Outbound events for evaluation outcomes

## Dependencies
- Data Contract Registry for asset identifiers and tags
- Policy Registry for policy references and parameters
- Platform Catalog tags for classification

## Diagrams
<a href="#fig-lo-erd" class="image-link">
  <img src="/assets/diagrams/lineage-obligations/lineage-obligations-erd.svg" alt="Lineage Obligations ERD">
</a>

<div id="fig-lo-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/lineage-obligations/lineage-obligations-erd.svg" alt="Lineage Obligations ERD">
</div>

_Figure 1: Lineage Obligations ERD_{.figure-caption}

<a href="#fig-lo-flow" class="image-link">
  <img src="/assets/diagrams/lineage-obligations/lineage-flow.svg" alt="Lineage event flow">
</a>

<div id="fig-lo-flow" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/lineage-obligations/lineage-flow.svg" alt="Lineage event flow">
</div>

_Figure 2: Lineage event flow_{.figure-caption}

## Module documentation

[Data Model](data-model.md)
Entities, relationships, DBML, DDL, and validation queries.

[UI](ui.md)
Screens to browse lineage, manage obligations, and review evaluations.

[API](api.md)
Operations for event ingest, graph traversal, obligation authoring, and evaluations.

[Observability](observability.md)
Metrics, logs, traces, dashboards, alerts, and SLOs.

[Runbook](runbook.md)
Procedures for routine operations and incidents.

[Security](security.md)
Classification, tenant isolation, access control, and audit.
