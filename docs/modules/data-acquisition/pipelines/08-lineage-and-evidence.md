# Lineage and Evidence

## Purpose
The Lineage and Evidence stage establishes traceability for every pipeline run in the BareCount Data Action Platform. It records how data moved, what transformations were applied, and which contracts and code versions governed the process. This stage ensures that every KPI can be traced back to its source records with verifiable evidence.

## Context
Without lineage, enterprises cannot answer basic audit questions such as “Where did this number come from?” or “Which version of the logic was applied?” BareCount embeds lineage and evidence capture into pipelines by default. Each run generates immutable records in the Evidence Ledger that describe inputs, outputs, code versions, and contract versions. This design allows regulators, auditors, and executives to validate outcomes with confidence.

## Key Capabilities

### End-to-End Lineage
- Captures lineage across ingestion, Raw Stage, GDP Transform, and KPI Materialization.  
- Each stage records run ID, upstream dependencies, and output locations.  
- Lineage allows queries such as tracing a KPI back to its raw source batches.

### Evidence Ledger Integration
- Each pipeline run writes entries into the Evidence Ledger.  
- Entries include run ID, contract version, schema hash, code version, input partitions, and record counts.  
- Ledger entries are immutable and time-stamped for compliance.

### Contract and Code Version Tracking
- Lineage links each dataset to the specific contract and code version applied.  
- Changes in definitions automatically create new lineage paths.  
- Historical queries can reconstruct results under prior definitions.

### Quarantine and Drift Records
- Violations or quarantined data are also logged in the Evidence Ledger.  
- Evidence entries include reasons for drift, sample payloads, and governance actions taken.  
- This ensures transparency even when runs deviate from expectations.

### Query and Audit Support
- Evidence Ledger supports queries by run ID, contract, KPI, or time period.  
- Audit trails can demonstrate compliance with data retention, reconciliation, and quality policies.  
- Evidence can be exported for regulators or external auditors without exposing internal pipelines.

## Operating Model
- All pipeline jobs are required to publish lineage and evidence as part of completion.  
- Failures to write ledger entries are treated as blocking issues.  
- Evidence entries are replicated across environments to ensure durability.  
- Dashboards surface lineage paths for operators and governance teams.

## Example
A Revenue KPI run produces 10,000 records. The Evidence Ledger entry shows:  
- Run ID: `rev_kpi_20251004_01`  
- Contract version: `v3.2`  
- Code version: `hash_a12b3c`  
- Input GDP partitions: `gdp/revenue/2025/10/04/*`  
- Record count: `10,000`  
- Drift events: none  

An auditor later queries the Evidence Ledger and traces this KPI back to Raw Stage invoice batches ingested from SAP on the same date. This allows full reconciliation of KPI values with the system of record.

## Notes
Lineage and Evidence make every KPI explainable. By embedding evidence capture into pipelines, BareCount ensures that data-driven decisions are defensible and auditable. Trust is not an afterthought; it is recorded with every run.
