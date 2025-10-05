# API Standards

## Scope
Standards for HTTP/REST and GraphQL across platform services.

## Transport
- HTTPS (TLS 1.3). HTTP/2 preferred.

## AuthN/Z
- Bearer JWT (≤ 1h). Scopes enforce ABAC/RBAC.
- mTLS optional per tenant (webhooks/exports).

## Versioning
- URI versioning `/api/v1/...`. No breaking changes in a major version.

## Headers
| Header | Dir | Purpose |
|---|---|---|
| Authorization | req | Bearer token |
| X-Tenant-Id | req | Tenant scoping |
| X-Request-Id | both | Idempotency + tracing |
| X-API-Version | resp | Echo active version |
| Retry-After | resp | Backoff hint |
| ETag | resp | Cache validation |
| Content-Type | both | `application/json` |

## Media Types
- `application/json; charset=utf-8`. Large binaries via signed URLs.

## REST Design
- Nouns: `/exports/jobs`, `/catalog/resources`.
- Subresources when lifecycle ties: `/jobs/{id}/artifacts`.
- Actions: `/jobs/{id}:retry` when needed.

## Methods
- GET (safe), POST (create/action), PUT (replace), PATCH (partial), DELETE (remove).

## Status Codes
- 200, 201, 202, 204; 400, 401, 403, 404, 409, 422, 429; 500, 502, 503, 504.

## Error Schema
```json
{ "error":"invalid_request", "message":"limit must be <= 1000", "request_id":"req_01J...", "details":[{"field":"limit","issue":"too_large"}] }
```

## Pagination
- Cursor‑based only.
```json
{ "items":[...], "next_cursor":"...", "total_estimate":12345 }
```

## Filtering / Sorting / Search
- Filters: object of arrays. Sorting: `sort=field:asc,other:desc`. Search: `query=...`.

## Idempotency
- `X-Request-Id` required for mutating calls. Server stores hash ≥ 24h. Mismatch → 409.

## Rate Limits
- Default 10 rps per tenant per endpoint class.
- Return `X-RateLimit-*` headers.

## Caching
- Support ETag/If‑None‑Match for GET. `Cache-Control: private` unless stated.

## Retries
- Retry 408/409(idempotent)/429/500/502/503/504 with backoff + jitter; honor `Retry-After`.

## OpenAPI
- Publish OpenAPI 3.1 for each service. Examples must round‑trip in CI.

## GraphQL
- Use when schema‑driven UIs benefit. Auth in resolvers. Prefer reads; justify mutations.

## Webhooks
- HMAC signatures (`X-Signature: sha256=...`); optional mTLS; jittered retries; `/replay` endpoint.

## Observability
- Tracing per request; metrics for throughput/latency/error; JSON logs with `request_id`/`tenant_id`.

## Stability & Deprecation
- `experimental` → `beta` → `ga` via `x-stability` in OpenAPI.
- Use `deprecated: true` and `Sunset` header. Maintain ≥ 6 months.

## Examples
### Create export
```bash
curl -X POST https://api.example.com/api/v1/data-consumption/exports/jobs   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_01J..."   -H "X-Request-Id: req_01J..."   -H "Content-Type: application/json"   -d '{ "dataset":"orders","version":"v24","format":"parquet","target":"s3://tenant/exports/orders" }'
```
### Paginate catalog
```bash
curl "https://api.example.com/api/v1/data-consumption/catalog/resources?limit=100&cursor=$CURSOR"   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_01J..."   -H "X-Request-Id: req_01J..."
```
