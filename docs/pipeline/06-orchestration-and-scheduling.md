# Orchestration and Scheduling

## Purpose
Define how jobs run, in what order, and under what triggers.

## Job types
- Ingestion
- Raw load
- GDP transform
- KPI materialization
- Compaction and vacuum
- Snapshot and export

## DAGs
Declare dependencies based on contracts and stages.
Calculate the run graph from selected contracts.

## Triggers
- Schedule
- Event
- Manual
- Replay

## Idempotency
Use run identifiers and idempotency keys.
Protect external calls with retries and backoff.

## Backfill
Support backfills over date or key ranges.
Protect freshness SLOs during large backfills.


## Stage gating, partial DAGs, and run profiles

## Stage gating and DAG reduction
Before a run starts, the system evaluates stage readiness.
Readiness requires an Active contract and an available target store.
If a stage is not ready, the scheduler removes it from the DAG.
The run continues with the remaining stages.

## Run profiles
Support these profiles:
- raw_only
- raw_plus_gdp
- kpi_only
- pre_fill
- backfill
- skeleton

Each profile selects a subset of stages.
Each profile sets default triggers and SLOs.

## Pre-fill
A pre-fill run loads historical Raw data.
It does not enforce a freshness SLO.
It records evidence and lineage.
It sets a checkpoint to protect later incremental runs.

## Idempotency across partial runs
Use the same idempotency rules for partial and full runs.
Use the same run identifiers and checkpoint scheme.
