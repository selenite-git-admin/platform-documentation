# Schema Services — Overview

## Purpose
Provide consistent data structures across the platform.
Define contracts and models for extraction, raw, GDP, and KPI schemas.
Enable safe change, repeatable validation, and clear evidence.

## Scope and Boundaries
Schema Services include schema contracts, enforcement, layer models, schema database guidance, and schema management.
Schema Services do not include visualization or end user UI.
Schema Services do not include general infrastructure provisioning.

## Platform Context
The data pipeline uses Schema Services at every stage.
Connectors read configuration, connect to sources or destinations, and produce or consume data.
The pipeline creates landing artifacts from extraction contracts.
The pipeline loads Bronze tables from raw contracts.
The pipeline creates Silver tables from GDP contracts.
The pipeline materializes Gold tables from KPI contracts.
The Host App records evidence, lineage, and SLO metrics.

See also:
- Pipeline module: `../pipeline/index.md`
- Connectors module: `../connectors/01-overview.md`
- Host App observability: `../host-app/ha-02e-observability.md`

## Contract Pattern
Each schema contract has two parts.
The header identifies the contract and its governance.
The payload defines the table or landing structure.

All concrete contracts inherit rules from the Meta Schema.
Contracts cover these types:
- extraction
- raw
- gdp
- kpi
- outbound

## Flow
1. Extraction Schema creates the landing artifact.
2. Raw Schema creates Bronze tables with near source fidelity.
3. GDP Schema creates Silver tables with conformed dimensions.
4. KPI Schema creates Gold tables for serving.

You can run the pipeline with a subset of stages.
You can keep Raw loading while GDP and KPI are not ready.
You can enable GDP and KPI later without a new extraction.

## Interfaces and Dependencies
Schema Services depend on metadata storage for contracts, rules, and lineage.
Schema Services expose validation APIs to the pipeline and connectors.
Schema Services produce evidence and lineage for audits.

## Glossary
Extraction Schema: landing contract for a source object.
Raw Schema: Bronze table contract with keys and types.
GDP Schema: Silver table contract with conformed semantics.
KPI Schema: Gold table contract for serving metrics.
