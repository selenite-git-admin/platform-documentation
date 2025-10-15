# Scheduler Options

## Purpose
The Scheduler Options stage defines how pipelines are triggered in the BareCount Data Action Platform. Scheduling ensures that data is ingested, transformed, and published at the right time to meet business needs while optimizing for cost and system load.

## Context
Enterprises need flexible scheduling because workloads vary by business process. Some require strict hourly or daily jobs, others depend on fiscal calendars, and still others are triggered by external events. BareCount provides a unified scheduler abstraction that supports cron-based schedules, event-driven triggers, and calendar-aware scheduling. All scheduling decisions are auditable and tied to governance policies.

## Key Capabilities

### Cron-Based Scheduling
- Pipelines can run on traditional cron expressions for hourly, daily, or weekly cycles.  
- Cron jobs are used for predictable workloads such as nightly ledger updates.  
- The scheduler manages retries and aligns jobs with SLO definitions.

### Event-Driven Scheduling
- Pipelines can be triggered by external events such as API calls, file drops, or webhook notifications.  
- Event-driven runs are common for near real-time ingestion and webhook connectors.  
- Events are logged in the Evidence Ledger with triggering metadata.

### Calendar-Aware Scheduling
- Pipelines can align with enterprise calendars such as fiscal periods, holidays, or regional working days.  
- Calendar services provide reusable definitions across tenants.  
- This prevents failures caused by scheduling jobs on non-business days.

### Conditional Scheduling
- Jobs can be triggered only when upstream dependencies complete successfully.  
- Conditions are enforced using orchestration metadata.  
- This ensures reliable sequencing across complex pipelines.

### Pause and Resume
- Pipelines can be paused during maintenance windows.  
- Resume operations honor state and lineage, preventing duplicate runs.  
- Governance policies define who can pause and resume jobs.

### SLA Alignment
- Scheduler integrates with freshness SLOs to ensure runs meet business timeliness requirements.  
- Missed schedules generate alerts routed to pipeline owners.  
- SLA breaches are recorded in the Evidence Ledger.

## Operating Model
- Developers declare schedules in pipeline manifests using cron syntax, event definitions, or calendar bindings.  
- Operators monitor schedule adherence in dashboards.  
- Governance teams review calendar bindings to ensure compliance with financial reporting cycles.  
- Schedule changes are versioned and tracked in the registry.

## Example
A Revenue KPI pipeline is scheduled to run every two hours during working days, excluding weekends and regional holidays. The manifest binds the pipeline to the enterprise calendar service. During a public holiday, the scheduler automatically skips the run. Evidence Ledger records the skipped execution along with calendar metadata for audit purposes.

## Notes
Scheduling in BareCount is flexible, auditable, and governance-aligned. Whether time-based, event-driven, or calendar-aware, every run is recorded with full context. This ensures that pipelines operate predictably and in harmony with enterprise business processes.
