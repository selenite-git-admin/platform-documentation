# Observability

## Metrics
- `schema_versions_total{tenant,subject,kind}`
- `validation_fail_total{reason}`
- `breaking_change_blocked_total`
- `alias_resolution_total{subject}`
- `webhook_delivery_total{result}`

## Tracing
- Root span per request; attrs: `tenant_id`, `subject`, `version`, `compatibility`, `request_id`.

## Dashboards
- Versions over time per subject
- Validation failure reasons
- Deprecation countdowns
