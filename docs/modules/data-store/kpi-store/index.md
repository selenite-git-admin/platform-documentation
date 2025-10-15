# KPI Store

## Role in the Platform
Curated KPIs with dimensional lookups and stable contracts for downstream apps.

<a href="#fig-kpi-store-sequence" class="image-link">
  <img src="/assets/diagrams/storage/kpi-store-sequence.svg" alt="KPI Store sequence diagram">
</a>
<div id="fig-kpi-store-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/storage/kpi-store-sequence.svg" alt="KPI Store sequence diagram">
</div>
_Figure: KPI Store sequence_{.figure-caption}

## Responsibilities
- Store KPI series and aggregates
- Maintain dimensions and slowly changing attributes
- Expose query APIs with filters and windows
- Guarantee backward-compatible contracts

## Inputs
- GDP datasets
- Dimension sources
- Calendar windows

## Outputs
- KPI tables and views
- Query results
- Contracts and docs

## Interfaces
- Query API
- Contract registry
- Dimension API

## Operational Behavior
- Time-partitioned storage with indexes
- Pre-aggregations for hot queries
- Cache popular windows

## Constraints
- No contract changes without version bump
- No ad-hoc writes
- SLA-bound query performance

## Examples in Action
- Query `revenue_mtd` with filters; return series and confidence

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
