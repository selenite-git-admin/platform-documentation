# Action Catalog

## Role in the Platform
Maintains versioned action templates (notifications, tickets, webhooks, automations) that can be bound to KPI states.

<a href="#fig-action-catalog-sequence" class="image-link">
  <img src="/assets/diagrams/action/action-catalog-sequence.svg" alt="Action Catalog sequence diagram">
</a>
<div id="fig-action-catalog-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/action/action-catalog-sequence.svg" alt="Action Catalog sequence diagram">
</div>
_Figure: Action Catalog sequence_{.figure-caption}

## Responsibilities
- Create, review, and publish templates
- Parameterize targets and throttling
- Validate compatibility at publish time
- Provide sample payloads and schema contracts

## Inputs
- Template drafts and approvals
- Schema registry references
- Policy for publish approvals
- Tenant configuration

## Outputs
- Published templates
- Validation reports
- Audit events

## Interfaces
- Template API for CRUD
- Publish API with approvals
- Search API for discovery

## Operational Behavior
- Draft→review→publish workflow
- Versioned templates with immutable history
- Dry‑run validation against sample events

## Constraints
- No breaking changes after publish
- Templates are content‑addressed and signed
- External schemas must be stable

## Examples in Action
- Publish new ‘Incident: Sev‑1 Pager’ template and validate payload
- Search for ‘Export Completed’ webhook template

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
