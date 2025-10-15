# Encryption – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| encrypt_requests_total | counter | count | tenant,alg | Throughput |
| encrypt_latency_seconds | histogram | seconds | tenant,alg | P95/P99 latency |
| kms_errors_total | counter | count | provider,code | Provider failures |

## Logs
Structured JSON with correlation IDs.

## Traces
- Root span per request; spans for cache, provider call, and persistence.

## Dashboards
- Throughput and latency percentiles.
- Error budget burn.

## Alerts
- High error rate, latency SLO breach, provider failure spikes.

## SLOs
- Availability ≥ 99.9% (30 days).
- P99 latency ≤ target per endpoint.
