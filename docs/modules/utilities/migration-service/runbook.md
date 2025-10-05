# Runbook

## First response
1. Capture `request_id`, `tenant_id`, endpoint and time window.
2. Check dashboards for error spikes and DLQ depth.
3. Classify: auth, quota, data contract, infra.

## Common incidents
- **429/Quota**: raise limits temporarily; confirm backoff headers; file follow-up for right-sizing.
- **Contract validation failures**: retrieve last good spec; compare drift; roll back or patch with ADR.
- **Webhook failures**: inspect DLQ; replay with `events/replay` after tenant confirms receiver health.

## Rollback
- Revert to previous `spec` version (immutable receipts).
- Re-run validation. Attach `X-Evidence-Id` to the change.
