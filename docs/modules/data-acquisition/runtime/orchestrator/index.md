# Orchestrator

## Role in the Platform
Central scheduler and DAG orchestrator for batch and near‑real‑time pipelines. Responsible for SLAs, retries, backfills, and dependency management.

<a href="#fig-orchestrator-sequence" class="image-link">
  <img src="/assets/diagrams/runtime/orchestrator-sequence.svg" alt="Orchestrator sequence diagram">
</a>
<div id="fig-orchestrator-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/runtime/orchestrator-sequence.svg" alt="Orchestrator sequence diagram">
</div>
_Figure: Orchestrator sequence_{.figure-caption}

## Responsibilities
- Register DAGs and schedules
- Manage dependencies and sensors
- Enforce retries, backoff, and circuit breaking
- Track run state and emit events
- Coordinate backfills and catch‑ups

## Inputs
- Job definitions and DAG specs
- Schedules and sensors
- Upstream dataset states
- Tenant calendars

## Outputs
- Run records and states
- Events to Streaming Bus
- Metrics and traces

## Interfaces
- Orchestrator API for DAGs and runs
- Callback webhooks for events
- Internal queue for run assignment

## Operational Behavior
- Use priority queues per tenant
- Detect and avoid deadlocks
- Resume from last checkpoint on retry

## Constraints
- No mutable global state in user code
- No unbounded fan‑out without quotas
- Calendar windows are authoritative

## Examples in Action
- Backfill ds_sales v24 across last week
- Pause DAG on upstream failure and auto‑resume

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
