# Observability

## Metrics
- `requests_total{endpoint,code}`
- `latency_ms_bucket{endpoint}`
- `errors_total{code}`
- `migration-service_resource_total{status}`
- `webhook_delivery_total{result}`

## Tracing
- Root span per request. Attributes: `tenant_id`, `resource_id`, `request_id`.

## Logging
- JSON logs with `request_id`, `tenant_id`, `subject`, `outcome`.

## Alerts (SLO-based)
- 5xx error rate > 1% (5 min)
- P95 > target for 10 min
- Dead-letter queue depth > 0 for 15 min
