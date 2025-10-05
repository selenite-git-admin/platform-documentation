# Dashboards

## Role in the Platform
Server-side rendered dashboards with caching, ACLs, and expiring share links. Built atop Activation APIs.

<a href="#fig-dashboards-sequence" class="image-link">
  <img src="/assets/diagrams/data-consumption/dashboards-sequence.svg" alt="Dashboards sequence diagram">
</a>
<div id="fig-dashboards-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-consumption/dashboards-sequence.svg" alt="Dashboards sequence diagram">
</div>
_Figure: Dashboards sequence_{.figure-caption}

## Responsibilities
- Render dashboard definitions
- Evaluate filters & permissions
- Cache tiles and hydrate client
- Generate secure share links

## Inputs
- Dashboard definitions
- Activation APIs
- Tenant roles & segments

## Outputs
- Rendered HTML/JSON
- Tile cache entries
- Audit logs

## Interfaces
- Render API
- Definition API
- Share API

## Operational Behavior
- Pre-render popular dashboards
- Invalidate on publish events
- Share links use expiring tokens

## Constraints
- No client secrets in embeds
- No unbounded export from tiles
- No remote code in layouts

## Examples in Action
- Render ‘Ops Overview’ with filters region=IN, week=40

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
