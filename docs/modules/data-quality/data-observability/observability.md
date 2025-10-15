# Observability

## Metrics
- `requests_total{endpoint,code}`
- `latency_ms_bucket{endpoint}`
- `errors_total{code}`
- `data-observability_resource_total{status}`
- `webhook_delivery_total{result}`

## Tracing
- Root span per request. Attributes: `tenant_id`, `resource_id`, `request_id`.

## Logging
- JSON logs with `request_id`, `tenant_id`, `subject`, `outcome`.

## Alerts (SLO-based)
- 5xx error rate > 1% (5 min)
- P95 > target for 10 min
- Dead-letter queue depth > 0 for 15 min

## SLO catalog

The service exposes a small set of SLOs that reflect timeliness and reliability of signals.

| SLO | Target | Notes |
|---|---|---|
| Metric emission delay | less than 60 seconds | from event to index |
| Alert delivery delay | less than 60 seconds | after rule evaluation |
| Snapshot availability | less than 3 minutes | after run completion |
| Dashboard freshness | less than 2 minutes | near real time views |

## Alert semantics

Alert objects use stable keys, severities, and suppression windows.

- key combines tenant_id, dataset_id, metric, and window
- severity uses info, warning, or critical
- dedup drops repeats on the same key during the suppression window
- suppression window defaults to 10 minutes, policy may override
- escalation maps severity to channels and ticketing routes

## Dashboards

Dashboards visualize freshness, completeness, drift, rule violations, and quality scores. Views exist per tenant, dataset, and layer. Filters include region, product, and partition key.

## Evidence linkage

Each promotion references a snapshot created by Observability. Evidence must include the snapshot identifier and hash so that the decision can be reconstructed.
