# Raw Stage

## Purpose
The Raw Stage provides the immutable landing zone for all ingested data in the BareCount Data Action Platform. Its role is to preserve the original source facts exactly as received, while attaching metadata for lineage, reproducibility, and governance. The Raw Stage acts as the single source of truth for what was ingested, when, and under which contract.

## Context
Enterprises often lose traceability by applying transformations too early. This leads to disputes when KPI values cannot be reconciled back to source records. BareCount prevents this by enforcing a strict Raw Stage policy. Data is written exactly as ingested, with no business transformations. Metadata such as contract version, schema hash, and run ID is recorded alongside payloads. Any change downstream can always be traced back to an immutable Raw Stage record.

## Key Capabilities

### Immutable Storage
- All ingested records are written as-is.  
- No updates or deletions are permitted.  
- Corrections or restatements are handled by replaying ingestion, never by editing Raw Stage data.

### Partitioning and Metadata
- Data is partitioned by load date and run ID.  
- Metadata includes extractor schema, contract version, source ID, and system build information.  
- This metadata ensures reproducibility for audits, backfills, and reprocessing.

### Schema Hashing
- Each landed file or batch is stamped with a schema hash derived from the extractor schema.  
- Differences in schema hash across runs signal drift and are tied to governance actions.  
- Schema hashes are stored in the Evidence Ledger for verification.

### Evidence Ledger Integration
- Each Raw Stage write is recorded in the Evidence Ledger with run ID, contract version, schema hash, record counts, and storage location.  
- Evidence entries provide a permanent record for compliance, audit, and reconciliation.

### Quarantine Reference
- Records that failed extractor schema parsing are excluded from the Raw Stage.  
- Instead, they are sent to a quarantine area with links back to the run metadata.  
- This ensures the Raw Stage remains clean and trusted.

## Operating Model
- All downstream transformations reference the Raw Stage as their source of truth.  
- Reprocessing or backfilling begins by replaying data from Raw Stage partitions.  
- Access to Raw Stage data is restricted and logged, since it may contain sensitive system fields.  
- Data retention policies are applied based on classification and regulatory requirements.

## Example
A connector ingests invoices from a CRM system. Each batch is landed in the Raw Stage partitioned by `load_date=2025-10-04/run_id=001`. Metadata records include extractor schema hash `abc123`, contract version `v2`, and record count `57,320`. The Evidence Ledger logs the run with these details, making it possible to later verify that every KPI derived from these invoices traces back to this immutable batch.

## Notes
The Raw Stage is not a workspace. Its purpose is preservation, not exploration. Queries, analysis, and transformations should be performed in later stages such as GDP Transform and KPI Materialization. This separation ensures trust in the lineage of all published KPIs.
