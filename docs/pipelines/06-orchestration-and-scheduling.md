# Orchestration and Scheduling

## Purpose
The Orchestration and Scheduling stage defines how pipelines in the BareCount Data Action Platform are executed, monitored, and retried. It ensures that data flows occur in the right order, at the right time, and under the right governance checks. Orchestration enforces discipline across ingestion, transformation, and KPI materialization stages.

## Context
Enterprises often rely on brittle cron jobs or manually triggered workflows. These fail to manage dependencies or respond effectively to failures. BareCount introduces structured orchestration with declarative manifests. Runs are triggered by schedules or events, dependencies are explicit, and retries are managed consistently. Governance prerequisites such as contract approval are integrated into orchestration logic.

## Key Capabilities

### Dependency Graphs
- Each pipeline stage declares dependencies on upstream stages.  
- For example, KPI Materialization depends on GDP Transform, which depends on Raw Stage ingestion.  
- Orchestration engines compute run order based on this graph.  

### Contract Prerequisites
- No downstream stage can run until contract checks are complete.  
- Ingestion must register extractor schema and validate against contracts.  
- Transform and KPI stages proceed only if governance has approved contract drift or schema updates.

### Scheduling Options
- Time-driven scheduling (hourly, daily, weekly) with configurable windows.  
- Event-driven scheduling triggered by upstream system updates or contract approvals.  
- Dependency-driven scheduling where runs only begin after upstream jobs complete successfully.

### Retry and Backoff
- Failed runs automatically retry with exponential backoff.  
- Retries include lineage tags so that Evidence Ledger captures both failed and successful attempts.  
- Persistent failures generate alerts and route to responsible teams.

### Idempotency and Run Tokens
- Each run is tied to a unique run token.  
- Re-running a pipeline with the same token produces the same output and lineage.  
- This prevents duplicate publications and ensures exactly-once semantics.

### Backfill and Replay
- Orchestration supports controlled backfills of historical data.  
- Backfills reference contract versions and calendar partitions to maintain consistency.  
- All backfill operations are logged in Evidence Ledger for compliance.

## Operating Model
- Orchestration manifests declare schedules, dependencies, and contract prerequisites.  
- Scheduler services interpret manifests and trigger runs.  
- Observability dashboards display run statuses, retry counts, and dependency graphs.  
- Governance reviews are enforced as blocking tasks when drift or contract issues are detected.

## Example
A finance KPI pipeline is scheduled daily at midnight. Orchestration checks that the GDP for invoices has completed successfully and that no contract violations are pending. If ingestion failed due to schema drift, orchestration blocks downstream runs until governance approves the contract update. Once approved, the pipeline continues, recomputes GDPs, and publishes KPIs with a run token.

## Notes
Orchestration ensures that pipelines run predictably and transparently. By treating contracts as dependencies, BareCount guarantees that governance is not bypassed. This model avoids brittle scheduling and provides a clear chain of evidence for every published KPI.
