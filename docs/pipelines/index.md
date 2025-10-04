# Pipelines

## Purpose
Pipelines describe the logical data lifecycle in the BareCount Data Action Platform. They define how data moves from source systems into governed Golden Data Points and then into published KPIs. Pipelines provide structure, predictability, and governance for every transformation, independent of the compute environment that executes them.

## Context
Enterprises often rely on ad hoc jobs and scripts that are difficult to operate and audit. BareCount uses a contract first model to make pipelines reliable and explainable. Every stream begins with an extractor schema from the connector and is validated against the Data Contract Registry before landing. Downstream stages use deterministic transforms, versioned specifications, and measurable acceptance thresholds.

## Stages at a Glance
- [Ingestion and Landing](02-ingestion-and-landing.md)  
  Contract validation at the boundary, controlled landing in the Raw Stage, state managed centrally, connectors remain stateless.

- [Raw Stage](03-raw-stage.md)  
  Immutable capture of source facts with partitioning, schema hash, contract version, and lineage stamps.

- [GDP Transform](04-gdp-transform.md)  
  Conformance into Golden Data Points with explicit join rules, survivorship, and late data handling.

- [KPI Materialization](05-kpi-materialization.md)  
  KPI as Code with versioned specs, tests, acceptance thresholds, and reconciliation against systems of record.

- [Orchestration and Scheduling](06-orchestration-and-scheduling.md)  
  Dependencies, schedules, retries, idempotency, and governed backfills.

- [Data Quality and Validation](07-data-quality-and-validation.md)  
  Contract checks at ingress, GDP shape checks, KPI acceptance gates, and clear escalation.

- [Lineage and Evidence](08-lineage-and-evidence.md)  
  Ledger entries for each run with inputs, code versions, contract versions, and record counts.

- [Observability, SLO, and Alerts](09-observability-slo-and-alerts.md)  
  Freshness, completeness, and accuracy targets with routed alerts.

- [Recovery, Replay, and DLQ](10-recovery-replay-and-dlq.md)  
  Point in time replays tied to contract versions and a triage playbook for dead letter queues.

- [Cost Controls and Scaling](11-cost-controls-and-scaling.md)  
  Storage and compute guardrails, retention classes, and tiered execution strategies.

- [Pipeline Configuration](12-pipeline-configuration.md)  
  Declarative manifests for streams, contracts, cursors, retention, and sensitivity tags.

- [Pipeline APIs](13-pipeline-apis.md)  
  Endpoints for run lifecycle, contract violations, lineage writes, and state operations.

- [Runners and Execution](14-runners-and-execution.md)  
  Separation of logic from machines so pipelines stay portable across environments.

- [Scheduler Options](15-scheduler-options.md)  
  Choices for time, event, or dependency driven runs with predictable outcomes.

- [Anomaly Integration](16-anomaly-integration.md)  
  Hooks that allow anomaly scores and narratives to enrich KPI activation.

## Operating Model
- Pipelines are declared as code and stored with version control.  
- Extractor schemas are compared with data contracts during ingestion.  
- Incremental state is stored in platform services so connectors remain stateless.  
- Each stage writes Evidence Ledger entries and emits metrics for observability.  
- Blocking versus warning policies are defined per stage and enforced consistently.

## Cross References
- Connectors Modules for extractor schemas and stateless design  
- Governance Modules for Data Contract Registry and policy enforcement  
- Trust Modules for Evidence Ledger and encryption services  
- Data Utilities for Calendar Service used by backfills and KPI windows

## Notes
Use the pages in this section as the authoritative guide for designing, operating, and evolving pipelines. Keep pipeline logic independent from runner choices so infrastructure can evolve without rewriting business logic.
