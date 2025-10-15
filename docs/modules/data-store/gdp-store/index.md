# GDP Store

## Role in the Platform
Governed, versioned data product with schemas, transformations, lineage, and validation gates.

<a href="#fig-gdp-store-sequence" class="image-link">
  <img src="/assets/diagrams/storage/gdp-store-sequence.svg" alt="GDP Store sequence diagram">
</a>
<div id="fig-gdp-store-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/storage/gdp-store-sequence.svg" alt="GDP Store sequence diagram">
</div>
_Figure: GDP Store sequence_{.figure-caption}

## Responsibilities
- Maintain versioned schemas and contracts
- Transform raw to curated GDP tables
- Validate data quality with gates
- Record lineage for audits

## Inputs
- Raw objects and events
- Schema registry
- DQ rules
- Calendar windows

## Outputs
- GDP datasets and versions
- DQ reports
- Lineage graph

## Interfaces
- Schema API
- Transform API
- Lineage API

## Operational Behavior
- Write transforms are idempotent per version
- Blue/green dataset swaps
- Backfill with checkpoints

## Constraints
- No destructive schema changes without version bump
- DQ gates block publish on failure
- Lineage is append-only

## Examples in Action
- Transform v24 publishes after passing DQ; lineage links raw→gdp

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
