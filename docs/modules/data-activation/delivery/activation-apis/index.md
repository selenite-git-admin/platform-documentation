# Activation APIs

## Role in the Platform
Tenant-facing query layer over KPIs and Published datasets with uniform filtering, paging, and contracts.

<a href="#fig-activation-apis-sequence" class="image-link">
  <img src="/assets/diagrams/data-consumption/activation-apis-sequence.svg" alt="Activation APIs sequence diagram">
</a>
<div id="fig-activation-apis-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-consumption/activation-apis-sequence.svg" alt="Activation APIs sequence diagram">
</div>
_Figure: Activation APIs sequence_{.figure-caption}

## Responsibilities
- Expose query endpoints with contracts
- Join KPI & dimension data
- Apply row/column security
- Cache and paginate results

## Inputs
- Published Store datasets
- KPI series
- Auth scopes and segments

## Outputs
- JSON/GraphQL results
- Signed cursors
- Metrics & traces

## Interfaces
- REST `/query` and GraphQL `/graphql`
- Resource discovery `/resources`
- ETag/caching

## Operational Behavior
- Prefer cached responses; invalidate on publish events
- Stable cursors for paging
- Per-tenant limits and field masks

## Constraints
- No ad-hoc writes
- No cross-tenant joins
- No breaking contract changes

## Examples in Action
- Query KPI with filters and join dimensions; paginate with cursor

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
