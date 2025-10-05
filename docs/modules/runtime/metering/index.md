# Metering

## Role in the Platform
Aggregates usage deltas from services into windowed counters for enforcement and billing reconciliation.

<a href="#fig-metering-sequence" class="image-link">
  <img src="/assets/diagrams/runtime/metering-sequence.svg" alt="Metering sequence diagram">
</a>
<div id="fig-metering-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/runtime/metering-sequence.svg" alt="Metering sequence diagram">
</div>
_Figure: Metering sequence_{.figure-caption}

## Responsibilities
- Ingest deltas from Enforcement and services
- Aggregate by tenant, feature, and window
- Expose counters to Enforcement and Billing
- Reconcile drifts and backfills

## Inputs
- Usage deltas (events)
- Tenant calendar
- Plan metadata for windowing

## Outputs
- Counters per window
- Drift reports
- Metrics and traces

## Interfaces
- Ingest API (events)
- Query API (counters)
- Reconciliation API

## Operational Behavior
- Idempotent upserts per (tenant,feature,window)
- Late events handled with watermarks
- Reconciliation jobs with diffs

## Constraints
- No destructive counter resets
- No cross‑tenant aggregation
- No opaque windows

## Examples in Action
- Ingest delta +1 for csv_export; counter reflects used_units
- Run reconciliation for last day across top tenants

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
