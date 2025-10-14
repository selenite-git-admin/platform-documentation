# Dataset Refresh Registry (DRR)

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Overview  
Data consumers across the platform—dashboards, APIs, and machine learning pipelines—depend on knowing whether their source data is fresh.  
Before DRR, teams solved this differently: some read scheduler tables, others queried orchestration logs, and many guessed based on timestamps. These divergent methods produced inconsistent freshness signals and undermined cross-layer trust.  

The Dataset Refresh Registry (DRR) provides a single, authoritative record of dataset freshness and scheduling state. It does not schedule or execute jobs. Instead, it maintains a clear, durable projection written by Runtime after each dataset job completes. DRR’s job is to tell every consumer *what just happened* and *what should happen next*—consistently, quickly, and securely.

## Design Principles  
- **Separation of concern:** Runtime executes jobs; DRR records their results.  
- **Authoritative freshness:** Every consumer sees the same status view.  
- **Low latency and high availability:** Reads must remain fast even during Runtime degradation.  
- **Tenant isolation:** Each tenant can only view its datasets.  
- **Predictable state:** Updates are idempotent and append-only.  

## Data Model in Context  
Each dataset registered in Storage has an entry in DRR. This entry captures:  
- The most recent successful run (`last_success_at`)  
- The next scheduled run (`next_scheduled_at`)  
- The computed freshness lag (`freshness_lag_sec`)  
- The derived status (`fresh`, `late`, `failing`, or `unknown`)  

When a Runtime job finishes, it posts a `refresh-state` update to DRR. The update is versioned by timestamp and becomes visible to all consumers within ten seconds. Downstream services query DRR directly or via the `describe` composite API, which merges DRR freshness data with Storage Catalog metadata.

### Example Interaction  
A reporting dashboard verifies KPI data freshness before showing numbers to a CFO.  
1. The dashboard calls `GET /storage/v1/datasets/kpi.cash_conversion_cycle_v2/freshness`.  
2. DRR responds:  
   ```json
   { "status": "fresh", "last_success_at": "2025-10-12T06:02:14Z", "freshness_lag_sec": 421 }
   ```  
3. The dashboard proceeds to query the dataset location provided by the Storage Catalog.  
If DRR returns `"late"` or `"failing"`, the UI surfaces a freshness warning and may defer query execution.

## Responsibilities  
- Persist and serve dataset freshness state with 99.99% availability.  
- Enforce single-writer model through Runtime with idempotent state updates.  
- Protect all tenant metadata via row-level security.  
- Expose low-latency read APIs to all authorized consumers.  
- Emit optional freshness-change events for observability pipelines.  

## Isolation and Ownership  
DRR belongs to the Storage domain but stores only metadata. Runtime is the exclusive writer; all other modules are read-only consumers. Multi-tenant enforcement applies at query level with `tenant_id` predicates.  

## Reliability Guarantees  
- **Availability:** 99.99 percent for reads.  
- **Propagation lag:** State visible within ten seconds of Runtime completion.  
- **Durability:** State persisted with WAL-backed storage replication.  
- **Staleness detection:** Datasets without updates for forty-eight hours automatically marked `unknown`.  

## Guardrails  
- Only Runtime service accounts may perform writes.  
- Stale updates older than the recorded timestamp are rejected.  
- Public APIs are read-only.  
- Datasets with failed updates remain in `failing` until new successful state is posted.  
- DRR never modifies scheduler or orchestration tables.  

## Dependencies  
- **Runtime:** Source of authoritative job completion events.  
- **Calendar Service:** Source of blackout and maintenance windows used by Runtime.  
- **Evidence Ledger:** Receives correlation identifiers for audit linking.  

## Summary  
The Dataset Refresh Registry provides a uniform truth for dataset readiness. It decouples orchestration from consumption, ensures deterministic freshness visibility, and maintains high trust boundaries across tenants. It is a foundational service for reliable, observable data delivery.