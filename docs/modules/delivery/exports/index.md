# Exports

## Role in the Platform
Consumer-facing export jobs (CSV/Parquet/API handoff) across destinations; source snapshots live in Storage → Published Store.

<a href="#fig-exports-sequence" class="image-link">
  <img src="/assets/diagrams/data-consumption/exports-sequence.svg" alt="Exports sequence diagram">
</a>
<div id="fig-exports-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-consumption/exports-sequence.svg" alt="Exports sequence diagram">
</div>
_Figure: Exports sequence_{.figure-caption}

## Responsibilities
- Define export jobs & destinations
- Initiate exports from snapshots
- Track receipts & notify via webhooks
- Retry with backoff & DLQ

## Inputs
- Published snapshots (Storage)
- Tenant endpoints/targets
- Security policies

## Outputs
- Export jobs & artifacts
- Delivery receipts
- Metrics & traces

## Interfaces
- Export API
- Delivery webhooks
- Replay API

## Operational Behavior
- Snapshot validation before start
- Idempotent delivery & retries
- Watermark-based replay

## Constraints
- No unsupported targets
- No unbounded replay
- No PII unless contracted

## Examples in Action
- Export `orders_v24` to S3; receive signed webhook on completion

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
