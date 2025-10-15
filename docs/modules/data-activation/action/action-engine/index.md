# Action Engine

## Role in the Platform
Evaluates rules against incoming events and creates action jobs.

<a href="#fig-action-engine-sequence" class="image-link">
  <img src="/assets/diagrams/action/action-engine-sequence.svg" alt="Action Engine sequence diagram">
</a>
<div id="fig-action-engine-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/action/action-engine-sequence.svg" alt="Action Engine sequence diagram">
</div>
_Figure: Action Engine sequence_{.figure-caption}

## Responsibilities
- Subscribe to KPI/state events
- Evaluate rules and conditions
- Resolve templates and variables
- Create idempotent jobs
- Debounce/aggregate to reduce noise

## Inputs
- Event streams
- Published templates
- Tenant rules and schedules
- Access decisions

## Outputs
- Job records
- Rule evaluation logs
- Metrics and traces

## Interfaces
- Rules API for CRUD
- Evaluate API for test runs
- Job status API

## Operational Behavior
- At‑least‑once processing with idempotency keys
- Batching for high‑volume events
- Backpressure with queues

## Constraints
- No side‑effects during evaluation
- Deterministic rule outcomes required
- Time windows use tenant calendars

## Examples in Action
- Rule `HighDefectRate` triggers `Incident Pager` job
- Aggregation suppresses duplicates within 5 min

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
