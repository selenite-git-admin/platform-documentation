# Published Store

## Role in the Platform
Tenant-ready datasets for exports, BI, and downstream applications. Schema-stable, deduplicated, and governed by contracts.

<a href="#fig-published-store-sequence" class="image-link">
  <img src="/assets/diagrams/storage/published-store-sequence.svg" alt="Published Store sequence diagram">
</a>
<div id="fig-published-store-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/storage/published-store-sequence.svg" alt="Published Store sequence diagram">
</div>
_Figure: Published Store sequence_{.figure-caption}

## Responsibilities
- Publish curated tables and views
- Enforce schema contracts and backward compatibility
- Provide export APIs and connectors
- Track consumption lineage

## Inputs
- GDP datasets and KPIs
- Contract registry
- Tenant consumption configs

## Outputs
- Published datasets and snapshots
- Export artifacts and logs
- Consumption lineage

## Interfaces
- Export API
- Contract API
- Connector adapters

## Operational Behavior
- Snapshotting with atomic swaps
- Idempotent export jobs
- DLQ for failed exports

## Constraints
- No breaking changes without deprecation window
- Exported artifacts are immutable
- Contract violations block publish

## Examples in Action
- Export `orders_snapshot` to S3 and notify via webhook

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
