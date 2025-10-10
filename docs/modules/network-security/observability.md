# Network Security – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| provisions_total | counter | count | type,status | Provisioning throughput |
| egress_blocks_total | counter | count | tenant,domain | Blocked attempts |
| network_latency_seconds | histogram | seconds | link | Connectivity health |

## Logs
Structured JSON with correlation IDs.

## Traces
- Root span per request; spans for WAF eval, JWT check, routing, and rate limit.

## Dashboards
- Traffic, block rates, latency, and error budget burn.

## Alerts
- DDoS conditions, JWT failures surge, cert expiry.

## SLOs
- Availability ≥ 99.99% (30 days).
- P99 routing latency ≤ 20ms.
