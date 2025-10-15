# Webhooks

## Role in the Platform
Push notifications for exports, refreshes, and events; reliable delivery with retries and DLQ.

<a href="#fig-webhooks-sequence" class="image-link">
  <img src="/assets/diagrams/data-consumption/webhooks-sequence.svg" alt="Webhooks sequence diagram">
</a>
<div id="fig-webhooks-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-consumption/webhooks-sequence.svg" alt="Webhooks sequence diagram">
</div>
_Figure: Webhooks sequence_{.figure-caption}

## Responsibilities
- Manage webhook endpoints
- Filter events by resource/rules
- Deliver with retries/backoff
- Provide replay from watermark

## Inputs
- Events from Exports/Runtime
- Tenant endpoints
- Security policies

## Outputs
- Delivery receipts & DLQ
- Metrics & traces
- Audit logs

## Interfaces
- Webhook API
- Delivery API
- Replay API

## Operational Behavior
- Debounce noisy sources
- Jittered backoff
- Signed requests

## Constraints
- No open endpoints without verification
- No unbounded replay
- No PII unless contracted

## Examples in Action
- Subscribe to KPI change for `revenue_mtd` region=IN; receive signed webhook

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
