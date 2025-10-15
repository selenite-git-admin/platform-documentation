# Secrets – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| secret_reads_total | counter | count | tenant,path | Throughput |
| lease_issues_total | counter | count | role | Issued credentials |
| secrets_latency_seconds | histogram | seconds | op | P95/P99 per op |

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
