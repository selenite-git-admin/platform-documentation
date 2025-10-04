# Pipeline APIs

## Purpose
The Pipeline APIs provide programmatic control and integration points for pipelines in the BareCount Data Action Platform. They allow operators, governance teams, and tenant administrators to manage pipelines consistently through well-defined interfaces.

## Context
Enterprises require more than user interfaces to manage pipelines. Automated systems, governance processes, and external tools must interact with pipelines. BareCount exposes APIs for every pipeline lifecycle action, ensuring consistency and auditability. These APIs follow contract-first design and integrate with lineage and evidence systems to provide complete transparency.

## Key Capabilities

### Management APIs
- Create, update, and delete pipeline manifests.  
- Promote pipelines across environments.  
- Apply tenant-specific overrides without modifying base manifests.  
- Query manifest history and version lineage.

### Execution APIs
- Start, stop, or pause pipeline runs.  
- Trigger replays from specific partitions or run IDs.  
- Launch backfills with explicit date ranges and governance approval.  
- Cancel active runs with safe rollback.

### Observability APIs
- Retrieve pipeline metrics such as run duration, record counts, and error rates.  
- Query logs filtered by run ID, stage, or error type.  
- Access lineage paths linking outputs to inputs.  
- Pull evidence records for audit purposes.

### Governance APIs
- Validate pipeline manifests against schema registry.  
- Retrieve SLO definitions and adherence status.  
- Access DLQ entries for triage workflows.  
- Submit governance decisions that unlock replays or contract updates.

### Integration APIs
- Webhook endpoints for pipeline state changes (success, failure, drift).  
- Event streams for real-time monitoring and orchestration.  
- Compatibility with CI/CD pipelines for automated deployment.  
- Role-based access control integrated with BareCount’s security model.

## Operating Model
- Developers interact with APIs to create and update pipelines.  
- Operators use APIs to run, replay, or recover pipelines.  
- Governance teams use APIs to validate manifests, approve changes, and audit evidence.  
- APIs are protected by authentication, authorization, and audit logging.

## Example
A tenant admin uses the Execution API to replay a failed partition for the Revenue KPI pipeline:
- `POST /pipelines/replay` with parameters: run ID `rev_kpi_20251004_01`, contract version `v3.2`, and partition `2025-10-04`.  
- The API validates the request against the Evidence Ledger.  
- The replay is approved and executed.  
- Observability APIs confirm the run succeeded and produced reconciled output.  

## Notes
Pipeline APIs make BareCount pipelines programmable, auditable, and integrable. They are the foundation for automation, governance, and large-scale adoption across enterprises. Every API call leaves an evidence trail, ensuring accountability in all operations.
