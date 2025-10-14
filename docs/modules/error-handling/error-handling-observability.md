# Error Handling Observability

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Make failures visible early, actionable quickly, and verifiable end-to-end. This document prescribes the metrics, logs, traces, SLOs, and alerts that all services and jobs must implement around the canonical error envelope. The approach is vendor-agnostic and fits serverless and container runtimes.

## Design Objectives
- Detect abnormal error rates in under 5 minutes
- Attribute errors by code, service, endpoint, and tenant cohort
- Correlate spikes to dependencies and deployments
- Measure retry effectiveness and client backoff behavior
- Keep signals small and cheap to emit; heavy lifts happen offline

## Golden Signals for Errors
| Signal | Definition | Why it matters |
|--------|------------|----------------|
| `error.rate` | errors / total requests (or jobs) | SLO breach lead indicator |
| `error.by_code` | counter labeled by `code` | Separates client vs platform faults |
| `retry.success_rate` | successful retries / retries | Validates guidance and backoff |
| `latency.p99` | 99th percentile | High latency often precedes 5xx |
| `dependency.errors` | downstream failures | Root-cause correlation |
| `rate_limited.count` | 429 responses | Abuse detection and capacity signals |

## Canonical Metrics
All metrics are emitted with structured labels. Suggested schema:

```
service, endpoint, code, http_status, retryable, tenant_cohort, region
```

### Required Counters/Gauges
- `requests.total` (counter)
- `errors.total` (counter; increment when returning a 4xx/5xx)
- `error.by_code` (counter; label: `code`)
- `retry.attempts` / `retry.success` (counters)
- `latency.p50` `latency.p95` `latency.p99` (gauges or histograms)
- `dependency.errors` (counter; label dependency name or class)
- `throttle.rate_limited` (counter; label `limit`, `window_sec` if practical)

### Example (pseudo)
```json
{ "metric":"error.by_code", "value":1, "labels":{"service":"catalog","endpoint":"GET /datasets","code":"dependency_unavailable","http_status":"503","region":"ap-south-1"} }
```

## Structured Logs
Emit one structured log per error with the canonical fields:
```
ts, service, endpoint, code, message_safe, correlation_id, http_status, tenant_cohort, retryable, details_redacted
```
- `message_safe` is the public-safe message. Detailed internals belong in a separate debug log guarded by role access.
- Never log secrets or PII. Use redaction and allow-lists for `details`.

## Tracing
- Every request/job carries `X-Correlation-Id` as trace attribute.
- Tag spans with `error.code`, `error.retryable`, `http.status_code`, and `dependency.name` where applicable.
- For batch jobs, start a new span per batch; attach item counts and failure counts as span attributes.

## SLOs
### Availability SLO (per service)
- **Objective:** `error.rate` ≤ 1% over rolling 30 days.
- **Burn alerting:** 2% over 1h, 5% over 5m.

### Latency SLO
- **Objective:** p99 within module-specific budgets (e.g., 150 ms for read-heavy APIs).

### Retry Efficacy
- **Objective:** `retry.success_rate` ≥ 95% for retryable codes.

## Dashboards
Each service should expose a standard “Errors” dashboard with:

1. **Overview**
   - Error rate (stacked by code)
   - Requests vs Errors
   - p99 latency

2. **Breakdowns**
   - Errors by code and endpoint
   - Retry success by code
   - Rate-limited responses over time

3. **Correlation**
   - Dependency errors vs service errors
   - Deployments vs error spikes (release markers)
   - Region comparison heatmap

4. **Drill-down**
   - Top correlation IDs contributing to the spike
   - Sample error logs with complete envelope

## Alert Policy
| Condition | Threshold | Window | Action |
|-----------|-----------|--------|--------|
| Platform P1 | `error.rate` > 1% across 3+ services | 5m | Page on-call, initiate incident |
| Endpoint P2 | `error.by_code{code="internal_error"}` grows > 5x baseline | 10m | Escalate to owning team |
| Dependency P2 | `dependency.errors` spike above baseline | 5m | Engage dependency owner |
| Abuse P3 | `rate_limited` rises while traffic stable | 15m | Throttle tenant, contact owner |
| Retry Drift | `retry.success_rate` < 90% for retryable codes | 30m | Review backoff, check limits |

### Alert Hygiene
- Noise control: apply per-endpoint and per-tenant cohort filters to avoid paging on single client misuse.
- Use grouping keys: service, endpoint, region.
- Include example `correlation_id`s in the alert note for fast forensic pivoting.

## Runbook Hooks
- For every alert, link to the service’s runbook with mitigations for `timeout`, `dependency_unavailable`, `serialization_failure`, `rate_limited`.
- Include a one-click query in your logging tool: `code=IN (...) AND correlation_id IN (...)`

## DRR and Evidence Ledger Correlation
- Overlay DRR freshness incidents with error spikes for data-dependent APIs.
- Use the same `correlation_id` to stitch write failures in Evidence Ledger with API errors seen by clients.

## Data Retention
- Metrics: 14–30 days (per your storage cost posture).
- Logs: 7–30 days hot, then cold for 90–180 days if required by compliance.
- Traces: 7 days hot, sampling-based.
- Mirror high-level counts in `error_aggregate_daily` for long-term trending.

## Serverless Considerations
- Cold starts: track `platform.cold_start.count` and correlate with p99 and 5xx.
- Throttles: emit `lambda.throttles` and link to concurrency limits.
- Provisioned concurrency changes should annotate dashboards.

## Container Considerations
- Record pod restarts and OOM kills; correlate with error bursts.
- Capture saturation metrics: CPU throttling, connection pool exhaustion.

## Testing and Verification
- Synthetic checks exercise `429`, `412`, and `503` flows.
- Chaos tests inject dependency failures; verify alerting and retry efficacy.
- Load tests evaluate whether `error.rate` stays under SLO at target QPS.

## Ownership
- SRE: alert routing, baseline calibration, and shared dashboards.
- Service teams: metric emission, runbook updates, and remediation automation.

## Summary
Operational visibility around the canonical error model is non-negotiable. With standard metrics, structured logs, tracing, SLOs, and crisp alerts, teams can detect issues fast, retrace failures via correlation IDs, and prove recovery via dashboards — without vendor lock-in or heavy engineering overhead.