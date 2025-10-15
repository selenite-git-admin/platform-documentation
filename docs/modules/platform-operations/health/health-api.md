# Health API

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define a consistent contract for liveness, readiness, startup, metrics, and data freshness across services. The API is automation friendly, cache aware, and safe to expose to orchestrators and monitors.

## Base path
Service local root. All endpoints are relative to each service, not a shared gateway path.

## Common headers
| Header | Direction | Purpose |
|---|---|---|
| `X-Correlation-Id` | in/out | echo for logs and traces |
| `Cache-Control` | out | controls cache behavior per endpoint |
| `Content-Type` | out | `application/json` for JSON responses |
| `Authorization` | in | bearer token for protected endpoints |

Authentication
- `/healthz` is usually public
- `/readyz`, `/startupz`, `/dataz`, `/fleet/*` require auth when exposed outside trusted networks
- `/metrics` is private and scraped by the platform collector

Errors
- On 4xx or 5xx, responses use the standard error envelope

```json
{"code":"dependency_unavailable","message":"database not reachable","correlation_id":"01J...","details":{"retryable":true}}
```

## Liveness
`GET /healthz`

Purpose
- Indicates the process is running and able to accept work

Behavior
- No dependency calls
- Fast and constant time

Response example
```json
{ "status": "ok", "time": "2025-10-13T07:30:00Z" }
```

Status codes
- 200 when the service loop is running
- 500 for catastrophic failure only

Caching
- `Cache-Control: public, max-age=10`

## Readiness
`GET /readyz`

Purpose
- Indicates the service can safely serve traffic

Behavior
- Checks critical dependencies only

Response example
```json
{
  "status": "ok",
  "checks": [
    {"name":"db","status":"ok","latency_ms":12},
    {"name":"secrets","status":"ok","latency_ms":5},
    {"name":"queue","status":"ok","latency_ms":8}
  ],
  "time": "2025-10-13T07:30:00Z"
}
```

Status codes
- 200 when all mandatory checks pass
- 503 when any mandatory check fails

Headers
- `Cache-Control: no-store`

## Startup gate
`GET /startupz`

Purpose
- Blocks traffic until one time initialization is complete

Status codes
- 200 only after startup completes
- 503 while initialization is in progress or failed

Headers
- `Cache-Control: no-store`

## Metrics
`GET /metrics`

Purpose
- Expose OpenMetrics or Prometheus format for scraping

Security
- Private. Collector authenticates within the network

Content Type
- `text/plain; version=0.0.4`

Example
```
# HELP service_uptime_seconds Process uptime
# TYPE service_uptime_seconds counter
service_uptime_seconds 12345
```

## Data freshness
`GET /dataz`

Purpose
- Advertise freshness and validation state of datasets owned by the service

Response schema
```json
{
  "status": "ok | degraded | fail",
  "datasets": [
    {"name":"kpi_store.daily_sales","fresh":"ok","as_of":"2025-10-13T07:00:00Z"},
    {"name":"gdp_store.ingest","fresh":"late","as_of":"2025-10-13T06:00:00Z","lag_minutes":90}
  ],
  "time": "2025-10-13T07:30:00Z"
}
```

Status codes
- 200 even if some datasets are late
- 503 only if the core dataset is missing or invalid

Headers
- `Cache-Control: no-store`

## Fleet rollup
`GET /fleet/readyz`

Purpose
- Aggregate readiness across multiple services for dashboards or external probes

Behavior
- Returns per service status with partial success when a subset is unavailable

Response example
```json
{
  "services":[
    {"name":"api","ready":"ok","ts":"2025-10-13T07:30:00Z"},
    {"name":"notifications","ready":"ok","ts":"2025-10-13T07:30:00Z"},
    {"name":"schema-registry","ready":"degraded","ts":"2025-10-13T07:29:55Z"}
  ]
}
```

Status codes
- 200 when the aggregator responds with any data
- 207 for partial results
- 503 when the aggregator is unavailable

Headers
- `Cache-Control: no-store`

## Dependency classification
- Critical checks block readiness
- Degraded checks report "status":"degraded" in `checks` but do not block readiness
- Optional dependencies are not included in readiness

## Rate limits
- `/healthz` no rate limit beyond network controls
- `/readyz`, `/startupz`, `/dataz` soft limit 10 RPS per caller
- `/fleet/readyz` soft limit 2 RPS per caller

## OpenAPI excerpt
```yaml
openapi: 3.0.3
info:
  title: Health API
  version: "2025-10-13"
paths:
  /healthz:
    get:
      operationId: healthz
      responses:
        '200':
          description: Alive
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, enum: [ok] }
                  time: { type: string, format: date-time }
  /readyz:
    get:
      operationId: readyz
      responses:
        '200':
          description: Ready
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, enum: [ok, degraded, fail] }
                  checks:
                    type: array
                    items:
                      type: object
                      properties:
                        name: { type: string }
                        status: { type: string, enum: [ok, degraded, fail] }
                        latency_ms: { type: integer }
                  time: { type: string, format: date-time }
        '503':
          description: Not ready
  /startupz:
    get:
      operationId: startupz
      responses:
        '200': { description: Started }
        '503': { description: Starting or failed }
  /dataz:
    get:
      operationId: dataz
      responses:
        '200':
          description: Data health
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, enum: [ok, degraded, fail] }
                  datasets:
                    type: array
                    items:
                      type: object
                      properties:
                        name: { type: string }
                        fresh: { type: string, enum: [ok, late, missing, invalid] }
                        as_of: { type: string, format: date-time }
                        lag_minutes: { type: integer }
                  time: { type: string, format: date-time }
```

## Curl examples

Liveness
```bash
curl -sS https://service.example.com/healthz
```

Readiness with correlation id
```bash
curl -sS -H "X-Correlation-Id: 01JC2Q0..." https://service.example.com/readyz
```

Data freshness with auth
```bash
curl -sS -H "Authorization: Bearer $TOKEN" https://service.example.com/dataz
```

## Security notes
- Always serve over HTTPS
- Avoid exposing hostnames, schema names, or credentials in responses
- Use short, non sensitive hints and push details to logs and traces
- Rate limit protected endpoints to avoid abuse

## Implementation checklist
- Return stable JSON shapes with correct cache headers
- Keep checks cheap and avoid synchronous calls to slow dependencies
- Use the platform correlation id and structured logging
- Provide configuration to toggle optional checks without code changes

## Summary
The Health API gives a small, repeatable set of endpoints that let orchestrators and people see if a service is alive, ready, and serving fresh data. It keeps payloads stable and safe while leaving deep diagnostics to logs, metrics, and traces.