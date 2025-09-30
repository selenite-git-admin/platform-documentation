# KPI Services — Overview

## Purpose
Serve metrics with reliability and clear governance.
Provide a registry and APIs that sit on top of the platform data.

## Scope
- Keep metric definitions consistent through a registry.
- Serve metrics through stable APIs.
- Enforce freshness and completeness SLOs.
- Provide admin and operator views.
- Integrate with data quality and anomaly detection.
- Support outbound delivery at scale.

## Boundaries
KPI Services do not redefine tables.
KPI Services do not run transformations.
KPI Services depend on the Metrics Schema and the Pipeline.

## Dependencies
- Metrics Schema contracts: ../schema/07-metrics-schema-model.md
- Pipeline materialization: ../pipeline/05-metrics-materialization.md
- DQ engine: ../pipeline/07-data-quality-and-validation.md
- Anomaly integration: ../pipeline/16-anomaly-integration.md

## Interfaces
- Read APIs for metrics and dimensions.
- Admin APIs for catalog, schedules, and SLOs.
- Evidence and lineage emission to the Host App.
