# Health

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Provide a uniform way to expose service and data health so operators, orchestrators, and external monitors can make fast, correct decisions. This module defines endpoint shapes, dependency checks, data freshness probes, and SLO-aligned alerting. It applies to API Gateway + Lambda services, containerized services, jobs, and the UI.

## Scope
Included
- Liveness and readiness endpoints for every service
- Startup probes and dependency gating
- Data health probes that reflect dataset freshness and schema validity
- Aggregation and fan-in patterns for fleet health
- Synthetic checks and smoke tests
- Observability mapping and incident hooks

Excluded
- Business KPIs and dashboards beyond availability and freshness
- Provider-specific deep diagnostics

## Design principles
- Clear separation of concerns: liveness, readiness, and data health are distinct
- Minimal, stable payloads designed for automation
- Tenant-safe: no cross-tenant data or identifiers in health responses
- Cheap to compute; heavy diagnostics stay in logs and traces
- Consistent semantics across runtimes

## Endpoint taxonomy
Every service exposes the following endpoints with identical behavior.

### `/healthz` (liveness)
Purpose: tell the platform "this instance is alive".  
Behavior: always fast and shallow. Does not call dependencies.

Response
```json
{ "status": "ok", "time": "2025-10-13T06:30:00Z" }
```

Status codes
- 200 when the process can accept a signal and the main loop is running
- 500 only on catastrophic failure (panic/boot loop)

Caching: allow intermediaries to cache for up to 10 seconds.

### `/readyz` (readiness)
Purpose: advertise ability to serve traffic safely.  
Behavior: checks critical dependencies that must be healthy for this service's core APIs.

Checks (examples)
- Database connectivity and low-latency query
- Secrets provider reachable and current
- Queue publish authority
- Config and feature flags loaded
- Warm cache if required for steady-state

Response
```json
{
  "status": "ok",
  "checks": [
    {"name":"db","status":"ok","latency_ms":12},
    {"name":"secrets","status":"ok","latency_ms":5},
    {"name":"queue","status":"ok","latency_ms":8}
  ],
  "time": "2025-10-13T06:30:00Z"
}
```

Status codes
- 200 when all mandatory checks are passing
- 503 when any mandatory check fails

Headers
- `Cache-Control: no-store`
- `X-Correlation-Id` echo if provided

### `/startupz` (startup gate)
Purpose: block traffic until service finishes one-time initialization (migrations, warm caches, JIT compiles).  
Status returns 200 only after startup sequence succeeds; before that respond 503.

### `/metrics` (telemetry)
Purpose: machine-readable metrics (Prometheus/OpenMetrics) with availability counters, error rate, latency, and health check timings.  
Security: authenticated in private networks; public endpoints expose only minimal counters.

## Dependency classification
- Critical: DB, secrets, config, message bus used on hot path
- Degraded: analytics sinks, non-critical caches
- Optional: best-effort enrichers and background exporters

Readiness fails for critical dependency failures. Degraded dependencies return 200 with `"status":"degraded"` on the check and a 200 at the endpoint level.

## Data health
Expose dataset-level health for user-facing freshness and validity signals.

### `/dataz` (data health summary)
Minimal, safe indicator for UI and orchestrators.

Response
```json
{
  "status": "ok",
  "datasets": [
    {"name":"kpi_store.daily_sales","fresh":"ok","as_of":"2025-10-13T06:00:00Z"},
    {"name":"gdp_store.ingest","fresh":"late","as_of":"2025-10-13T05:00:00Z","lag_minutes":90}
  ],
  "time": "2025-10-13T06:30:00Z"
}
```

Rules
- Determinations come from DRR and Schema Registry validations
- No tenant identifiers in the payload
- Limit list to datasets owned by the service

Status codes
- 200 even if some datasets are late; clients read per-item `fresh`
- 503 only if the module's core dataset is missing or corrupt

## Standard payload schema
```json
{
  "status": "ok | degraded | fail",
  "time": "RFC3339",
  "checks": [
    {"name":"<dep>","status":"ok|degraded|fail","latency_ms":0,"hint":"optional"}
  ]
}
```

Rules
- `status` summarizes overall outcome
- `hint` is short and non-sensitive, suitable for logs and UI
- Never include hostnames, secrets, or stack traces

## Security
- All health endpoints serve over HTTPS
- `/healthz` may be public; `/readyz` and `/dataz` require auth when exposed beyond cluster or VPC
- Rate limit to prevent abuse
- Responses include `Cache-Control: no-store` except `/healthz`
- Avoid cross-tenant leakage by scoping dataset names to public identifiers only

## Aggregation patterns
- Sidecar or agent scrapes `/readyz` and `/metrics` and pushes to the aggregator
- Fleet endpoint `/fleet/readyz` composes component readiness into a single rollup
- Use partial results. If one service is unreachable, return 207 Multi-Status from the aggregator with per-service details

Example aggregator response
```json
{
  "services":[
    {"name":"api","ready":"ok","ts":"2025-10-13T06:30:00Z"},
    {"name":"notifications","ready":"ok","ts":"2025-10-13T06:30:00Z"},
    {"name":"schema-registry","ready":"degraded","ts":"2025-10-13T06:29:30Z"}
  ]
}
```

## SLOs
- Availability: 99.9 percent per service per month
- Health endpoint latency: p95 < 50 ms
- Freshness: dataset late less than 1 percent of intervals per 7-day window

## Dashboards
- Uptime by service and region
- Readiness failures by dependency
- Data freshness lag histogram
- Health check latency trend
- Fleet rollup with drill-down

## Alerts
| Condition | Threshold | Action |
|---|---|---|
| Readiness failing | `/readyz` returns 503 for 2 consecutive checks | Page on-call |
| Health check slow | p95 `/readyz` latency > 200 ms for 10 minutes | Investigate dependency saturation |
| Data late | `fresh="late"` for a core dataset beyond SLO | Alert owning team |
| Fleet partial | >10 percent services missing from rollup | Investigate network or deploy |

## Synthetic checks
- External check hits public routes and validates HTML markers and 200/302 patterns
- Internal check calls authenticated APIs and verifies a short, read-only journey
- Data synthetic loads a stable test record and validates read path

## Implementation checklist
- [ ] Implement `/healthz`, `/readyz`, `/startupz`, `/metrics`, `/dataz` with schemas above
- [ ] Tag logs with `probe=health` and `probe=data`
- [ ] Emit `health.check.latency_ms` for each dependency
- [ ] Readiness gates deployments in orchestrator
- [ ] Wire DRR lookups for freshness signals
- [ ] Add synthetic checks to CI and post-deploy

## Runbook hooks
- If `/readyz` fails on DB, run connection pool diagnostics and retry with reduced concurrency
- If `/dataz` shows late datasets, pivot to DRR for lag source and trigger replay or backfill
- For repeated slow checks, capture traces and review index/capacity

## Examples

### Minimal Lambda handler (pseudo)
```python
def healthz(event, ctx):
    return 200, {"status":"ok","time":now_iso()}

def readyz(event, ctx):
    results = [
        check_db(),
        check_secrets(),
        check_queue()
    ]
    overall = "ok" if all(r.ok for r in results) else "fail"
    return 200 if overall=="ok" else 503, {
        "status": overall,
        "checks": [r.to_dict()],
        "time": now_iso()
    }
```

### Container probe config (Kubernetes)
```yaml
livenessProbe:
  httpGet: { path: /healthz, port: 8080 }
  periodSeconds: 10
  timeoutSeconds: 2
readinessProbe:
  httpGet: { path: /readyz, port: 8080 }
  periodSeconds: 10
  timeoutSeconds: 2
  failureThreshold: 3
startupProbe:
  httpGet: { path: /startupz, port: 8080 }
  periodSeconds: 10
  failureThreshold: 30
```

## Summary
A small, consistent set of health endpoints yields predictable automation, faster incident response, and trustworthy signals for operators and clients. With clear separation of liveness, readiness, and data health plus DRR-backed freshness, the platform remains transparent and dependable.