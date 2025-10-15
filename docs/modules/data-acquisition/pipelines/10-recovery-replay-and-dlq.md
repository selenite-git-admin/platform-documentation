# Recovery, Replay, and DLQ

## Purpose
The Recovery, Replay, and Dead Letter Queue (DLQ) stage provides mechanisms to handle failures, recover lost data, and replay pipelines in the BareCount Data Action Platform. It ensures that errors do not compromise trust and that historical data can be reprocessed in a governed manner.

## Context
Failures are inevitable in enterprise data pipelines. Systems may be unavailable, schema drift may occur, or transformations may fail. Without structured recovery, teams resort to ad hoc fixes that erode lineage and trust. BareCount enforces governed recovery processes: replays are contract-aware, DLQs capture failed records with metadata, and lineage entries document all corrective actions.

## Key Capabilities

### Point-in-Time Replay
- Pipelines can be replayed from any Raw Stage partition or GDP version.  
- Replays reference the contract version and code version active at that time.  
- This guarantees reproducibility and allows historical reconciliation.

### Backfill
- Controlled reprocessing of historical data based on calendar partitions.  
- Backfills are tied to contract versions to prevent applying current logic to outdated definitions.  
- Governance teams approve backfills to avoid accidental restatements.

### Dead Letter Queue (DLQ)
- Records that fail validation or transformation are sent to a DLQ.  
- DLQ entries include payload samples, run ID, schema hash, and error descriptions.  
- DLQs are queryable for root cause analysis and triage.

### Triage Playbook
- Each DLQ has a standard triage process:  
  1. Review error description and sample payloads.  
  2. Determine if issue is transient (retry) or structural (contract update).  
  3. Escalate to governance if contracts must change.  
  4. Replay affected records once resolved.  
- Evidence Ledger entries link DLQ events to governance decisions.

### Immutable Evidence
- All replays and recoveries are logged as new runs with lineage back to the failed run.  
- Evidence Ledger ensures transparency that recovery occurred and which inputs were affected.  
- This prevents silent overwrites or loss of accountability.

## Operating Model
- Operators trigger replays or backfills through APIs with explicit parameters: run ID, partition, and contract version.  
- DLQs are monitored as part of observability dashboards.  
- Governance reviews ensure that structural changes are managed before replaying.  
- Recovery operations are treated with the same rigor as primary pipeline runs.

## Example
A GDP transform fails due to new field `AccountType` introduced in SAP. Affected records are routed to DLQ with error descriptions. Governance reviews the change and updates the contract. Once approved, operators replay the failed partition using the updated contract. Evidence Ledger records both the failed run and the replay, ensuring transparency.

## Notes
Recovery is not an exception process but part of the lifecycle. BareCount’s contract-first replay and DLQ design ensures that failures are visible, recoverable, and auditable. This preserves trust in KPIs even when errors occur.
