# Conventions

## Scope
Unified conventions for platform modules, pipelines, and apps. Follow this unless an ADR states an approved divergence.

## Principles
- Clarity over cleverness.
- Determinism and replayability.
- Least privilege.
- Evidence-first.

## Identifiers
- snake_case fields, kebab-case paths, SCREAMING_SNAKE_CASE constants.
- Prefer ULIDs (sortable): `01J9Z9N6H5F8W42Q9YB4QQJ1G6`.
- Natural keys allowed in read paths but not as storage PKs.
- Composite keys as objects, not concatenated strings.

## Time & Duration
- ISO‑8601 UTC with `Z`. Example: `2025-10-05T06:42:10Z`.
- Durations ISO‑8601 (`P1D`, `PT5M`).
- Store/output UTC; accept user offsets on input.

## Money & Decimals
- Fixed‑point in storage; JSON strings for money: `"1234.56"`.

## Enums & Flags
- Enums as lowercase strings; prefer enums over multiple booleans.

## Resource Naming
- REST paths: `/{domain}/{collection}/{id}`; nested sparingly.
- KPI keys: `kpi:<namespace>.<name>`; Datasets: `dataset:<namespace>.<name>`.

## Pagination
- Cursor‑based only: `?cursor=...&limit=100`.
- Cursor: opaque, signed, base64url. Include `next_cursor`.
- Default limit 50; max 1000.

## Filtering & Search
- Filters object with arrays per field.
- Search via `query` param; date filters `from`/`to` (UTC).

## Versioning & Contracts
- URI versioning: `/api/v1/...`.
- Additive evolution only inside major versions.
- Older clients keep working; new fields must be optional.

## Error Model
```json
{ "error":"invalid_request", "message":"limit must be <= 1000", "request_id":"req_01J..." }
```
- Use 400, 401, 403, 404, 409, 422, 429, 500, 503.

## Idempotency
- Header: `X-Request-Id`. Same id + same payload ⇒ same effect.

## Retries & Backoff
- Client: exponential backoff + jitter; cap 60s; total 5m.
- Honor `Retry-After` on 429/503.

## Caching
- ETag/If‑None‑Match for GET; keys include auth scope and filters.

## Security Headers
- Authorization: Bearer JWT.
- X-Tenant-Id required for multi‑tenant ops.
- X-Request-Id for correlation.
- X-Evidence-Id optional for regulated actions.

## Telemetry
- OpenTelemetry traces/logs/metrics.
- Span attrs: tenant_id, resource_id, contract, result_count.

## Naming (Code)
- Packages: `company.module.component`.
- Env vars: `DATAJETTY_*`.
- Feature flags: `runtime.orchestrator.enable_backfill`.

## Retention
- Requests 30d; Metrics 90d; Evidence 180d+.

## Deprecation
- `Sunset:` header and CHANGELOG; support ≥ 6 months.

## Documentation
- Every module ships: index, api, data-model, observability, runbook, security, ui.
- Examples must be runnable.
