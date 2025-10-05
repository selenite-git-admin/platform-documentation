# GDP Calendar

## Role in the Platform
Schedules and status for GDP refresh windows. Enables predictable data availability and SLAs.

<a href="#fig-gdp-calendar-sequence" class="image-link">
  <img src="/assets/diagrams/storage/gdp-calendar-sequence.svg" alt="GDP Calendar sequence diagram">
</a>
<div id="fig-gdp-calendar-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/storage/gdp-calendar-sequence.svg" alt="GDP Calendar sequence diagram">
</div>
_Figure: GDP Calendar sequence_{.figure-caption}

## Responsibilities
- Maintain refresh schedules per dataset
- Expose next/last run and status
- Publish maintenance windows
- Trigger notifications

## Inputs
- Dataset metadata
- Runtime scheduler
- Time zones/holidays

## Outputs
- Schedule entries
- Run history
- Notifications

## Interfaces
- Calendar API
- Status API
- Notification webhooks

## Operational Behavior
- Time‑zone aware scheduling
- Grace windows for long runs
- Idempotent status updates

## Constraints
- No overlapping runs without explicit config
- Calendar is source of truth for SLAs
- Backfills tracked separately

## Examples in Action
- Publish monthly schedule for ds_sales; send webhook on completion

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
