# Gateway – Observability

## Metrics
| Name | Type | Unit | Labels | Purpose |
|------|------|------|--------|---------|
| edge_requests_total | counter | count | code,method,path | Throughput |
| edge_latency_seconds | histogram | seconds | path | Routing latency |
| waf_blocks_total | counter | count | rule | Blocks by rule |
| jwt_failures_total | counter | count | reason | Authn/z failure reasons |

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
