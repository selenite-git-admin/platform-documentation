# Data Pipeline — Overview

## Purpose
Describe the runtime system that moves data from sources to Gold.
Use schema contracts to drive every step.
Provide reliable, observable, and cost aware runs.

## Scope
Cover ingestion and landing, raw load, GDP transforms, and KPI materialization.
Cover orchestration, data quality, lineage, evidence, observability, recovery, and cost controls.
Do not cover visualization or end user UI.
Do not cover source system behavior.

## Stages
- Extraction to landing
- Raw stage in Bronze
- GDP transforms in Silver
- KPI materialization in Gold

## Control planes
- Orchestration and scheduling
- Data quality and validation
- Lineage and evidence
- Observability, SLOs, and alerts
- Recovery and replay

## Interfaces
- Reads schema contracts. See ../schema/02-schema-contracts.md
- Applies enforcement rules. See ../schema/03-schema-enforcement.md
- Uses extraction schema to create landing. See ../schema/04-extraction-schema-model.md
- Uses raw schema to create Bronze. See ../schema/05-raw-schema-model.md
- Uses GDP schema to create Silver. See ../schema/06-gdp-schema-model.md
- Uses KPI schema to create Gold. See ../schema/07-kpi-schema-model.md
- Emits evidence and lineage to Host App stores. See ../host-app/ha-02e-observability.md

## Inputs and outputs
Inputs:
- Schema contract headers
- Schema contract payloads
- Run configuration

Outputs:
- Tables or files at each stage
- Evidence records
- Lineage records
- Logs and metrics

## Success metrics
- Freshness within target SLO
- Completeness within target SLO
- Cost per run within budget
- Time to recovery within target


## Stage readiness and partial runs

### Stage readiness and partial runs
The pipeline does not require all stages to be ready.
You can run the pipeline with only Raw ready.
You can run pre-fill runs that load historical Raw only.
You can enable GDP and KPI later without re-ingesting the source.

Define these run profiles:
- raw_only: ingest and load Raw only
- raw_plus_gdp: ingest, Raw, and GDP
- kpi_only: materialize KPI from existing GDP
- pre_fill: historical Raw only, no freshness SLO
- backfill: recompute GDP or KPI for a time window
- skeleton: validate contracts and DDL without moving data

The scheduler builds a DAG that includes only the stages that are ready.
Stages that are not ready are excluded.
Skipped stages do not block other stages that are ready.
