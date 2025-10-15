# Catalog

## Role in the Platform
Consumer-facing discovery of published datasets & KPIs with business-friendly descriptions, freshness, and contracts.

<a href="#fig-catalog-sequence" class="image-link">
  <img src="/assets/diagrams/data-consumption/catalog-sequence.svg" alt="Catalog sequence diagram">
</a>
<div id="fig-catalog-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-consumption/catalog-sequence.svg" alt="Catalog sequence diagram">
</div>
_Figure: Catalog sequence_{.figure-caption}

## Responsibilities
- Curate metadata (title, summary, freshness, owner, SLA, contract)
- Provide search/tags/collections
- Surface examples and approved joins
- Link to lineage/evidence (read-only)

## Inputs
- Published Store metadata
- KPI registry
- Contracts (Governance)

## Outputs
- Catalog entries & collections
- Badges for contracts/SLA
- Metrics & traces

## Interfaces
- Browse API `/resources`
- Details `/resources/{id}`
- Collections `/collections`

## Operational Behavior
- Periodic metadata sync from Storage/Governance
- De-duplicate aliases
- Expose stable ids

## Constraints
- Read-only; no authoring
- No cross-tenant leakage
- No unverifiable freshness claims

## Examples in Action
- Search ‘Revenue’ and open resource; view contract v1 and freshness P1D

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
