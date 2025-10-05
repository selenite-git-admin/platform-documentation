# Evidence Ledger – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| evidence_appends_total | counter | count | tenant,kind | Throughput |
| ledger_verify_total | counter | count | result | Verification ops |
| ledger_latency_seconds | histogram | seconds | op | Append/verify latency |

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
