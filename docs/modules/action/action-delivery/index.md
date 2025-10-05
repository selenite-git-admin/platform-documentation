# Action Delivery

## Role in the Platform
Dispatches actions to external systems with retries, exponential backoff, and DLQ handling.

<a href="#fig-action-delivery-sequence" class="image-link">
  <img src="/assets/diagrams/action/action-delivery-sequence.svg" alt="Action Delivery sequence diagram">
</a>
<div id="fig-action-delivery-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/action/action-delivery-sequence.svg" alt="Action Delivery sequence diagram">
</div>
_Figure: Action Delivery sequence_{.figure-caption}

## Responsibilities
- Maintain protocol adapters (email, Slack, ITSM, webhook)
- Apply per-tenant rate limits
- Sign webhooks with HMAC/mTLS
- Manage DLQ and replays

## Inputs
- Jobs from Action Engine
- Tenant delivery configuration
- Secrets for endpoints
- Network policies

## Outputs
- Delivery receipts
- DLQ entries
- Metrics and traces

## Interfaces
- Delivery API for endpoint health
- DLQ API for inspection
- Replay API for selected messages

## Operational Behavior
- Idempotent dispatch with delivery keys
- Backoff with jitter; max attempts policy
- Quarantine noisy endpoints automatically

## Constraints
- No plaintext secrets in logs
- Strict egress allow-lists
- DoS protection on retries

## Examples in Action
- Webhook sent with signature; receiver verifies and returns 2xx
- Failed deliveries moved to DLQ and replayed after fix

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
