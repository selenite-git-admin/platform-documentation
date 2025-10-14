# Error Handling API

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define how services and clients exchange errors over HTTP, gRPC, and events using a single canonical envelope. The contract is stable across modules and environments (Lambda, containers, batch). It prioritizes diagnosability, safe retries, and tenant safety.

## Design Tenets
- One envelope everywhere (REST, gRPC metadata, event bus)
- Stable symbolic codes with explicit retry semantics
- Correlation first: every error binds to logs, traces, and the Evidence Ledger
- No leakage: safe messages for clients; rich context stays server-side
- Idempotent writes with explicit replay guidance

## Canonical Envelope
All client-facing errors must conform to this JSON shape.

```json
{
  "code": "invalid_request",
  "message": "Field `tenant_id` is required",
  "correlation_id": "01JAH8ZJ0Z8Z0N7M1X6JZ8QW0T",
  "details": {
    "field": "tenant_id",
    "retryable": false,
    "hint": "Provide a non-empty tenant id"
  }
}
```

### Fields
| Field | Required | Type | Notes |
|------|----------|------|------|
| `code` | yes | string | Stable symbolic identifier |
| `message` | yes | string | Safe human-readable text; no PII |
| `correlation_id` | yes | uuid (v7) | Echo inbound or gateway-generated |
| `details` | no | object | Machine-readable context (stable keys documented below) |

Stable `details` keys:
- `retryable` (bool) – client hint
- `field` (string) – for validation errors
- `limit`, `window_sec` (numbers) – for `rate_limited`
- `expected_etag` (string) – for `stale_read`
- `existing_id` (uuid) – for `already_exists`/`conflict`

## HTTP Contract

### Status Mapping
| HTTP | Codes | Guidance |
|------|-------|----------|
| 400 | `invalid_request`, `validation_failed` | No retry. Fix payload. |
| 401 | `unauthenticated` | Re-authenticate. |
| 403 | `forbidden`, `scope_insufficient` | Request access or scope. |
| 404 | `not_found` | Verify id or tenancy. |
| 409 | `conflict`, `already_exists` | Use `details.existing_id` or idempotency key. |
| 412 | `stale_read` | Re-GET with ETag then retry write. |
| 415 | `unsupported_media_type` | Fix `Content-Type`. |
| 429 | `rate_limited` | Honor `Retry-After`. |
| 500 | `internal_error` | Retry not advised unless instructed. |
| 502–504 | `dependency_unavailable`, `timeout` | Retry with backoff. |

### Required Headers
| Header | Direction | Notes |
|--------|-----------|-------|
| `X-Correlation-Id` | in/out | UUIDv7; gateway generates if missing |
| `Retry-After` | out | Required on 429; optional on 503 |
| `Cache-Control` | out | `no-store` for 4xx/5xx |
| `ETag` | out | With `412 stale_read` flows |
| `Idempotency-Key` | in | For replay-safe writes (24h window) |

### REST Examples

Validation (400)
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
X-Correlation-Id: 01JAH8...

{ "code":"validation_failed","message":"`name` must not be empty","correlation_id":"01JAH8...","details":{"field":"name","retryable":false} }
```

Conflict (409)
```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{ "code":"conflict","message":"Tenant already exists","correlation_id":"01JAH8...","details":{"existing_id":"7c7f..."} }
```

Stale Read (412)
```http
HTTP/1.1 412 Precondition Failed
ETag: "d41d8cd98f00b204e9800998ecf8427e"

{ "code":"stale_read","message":"Resource changed; GET latest and retry","correlation_id":"01JAH8...","details":{"retryable":true,"expected_etag":"d41d8..."} }
```

Rate Limited (429)
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 10

{ "code":"rate_limited","message":"Too many requests","correlation_id":"01JAH8...","details":{"retryable":true,"limit":2000,"window_sec":60} }
```

Dependency (503)
```http
HTTP/1.1 503 Service Unavailable

{ "code":"dependency_unavailable","message":"Downstream dependency unavailable","correlation_id":"01JAH8...","details":{"retryable":true} }
```

## gRPC Contract
- Use `google.rpc.Status` for the envelope (`code` maps to `status.details`).
- Include `x-correlation-id` in metadata for every call and propagate downstream.
- Map HTTP-equivalent semantics:
  - `INVALID_ARGUMENT` → `validation_failed`
  - `NOT_FOUND` → `not_found`
  - `ALREADY_EXISTS` → `already_exists`
  - `FAILED_PRECONDITION` → `stale_read`
  - `RESOURCE_EXHAUSTED` → `rate_limited`
  - `UNAUTHENTICATED` / `PERMISSION_DENIED` → `unauthenticated` / `forbidden`
  - `ABORTED` → `serialization_failure`
  - `UNAVAILABLE` / `DEADLINE_EXCEEDED` → `dependency_unavailable` / `timeout`

## Events and Webhooks
- Event payloads include `error` using the same envelope when a job fails permanently.
- Webhook responses must use the envelope on non-2xx outcomes. Do not leak internal queue names.
- For durable processing, acknowledge (2xx) only after enqueue; otherwise surface an error with `code` and `correlation_id`.

## Idempotency
- Writes accept `Idempotency-Key`. On replay within 24 hours, return the original outcome with the same `correlation_id` and `ETag` if applicable.
- For `already_exists`, include `details.existing_id` and make the operation safe to repeat.

## Multi-tenant Safety
- Prefer 404 over 403 when revealing existence is unsafe across tenants.
- Never include `tenant_id` in the response body; keep it in logs only.

## SDK Requirements
- Provide typed exceptions with `code`, `message`, `correlationId`, `details`.
- `isRetryable(code)` helper implements the retry table.
- Built-in exponential backoff with jitter; read `Retry-After` when present.
- ETag helpers for `If-Match` / `If-None-Match` and `412` handling.
- Idempotency helper to set and persist `Idempotency-Key` per write attempt.

## Evidence Ledger
- For write attempts, emit an audit with `correlation_id`, `code`, and request summary on failure. On success, emit a matching success audit using the same `correlation_id`.

## Versioning
- Envelope is version-agnostic. Introducing new `details` keys requires doc updates but must remain backward compatible.
- Service-specific codes are prohibited; use the taxonomy and put specifics in `details`.

## Testing Checklist
- 1xx/2xx/3xx unaffected (no envelope).
- Each 4xx/5xx correctly maps to a documented `code`.
- `X-Correlation-Id` echoes and traces end-to-end.
- 429 includes `Retry-After` and SDK honors it.
- 412 round-trip with ETag passes with a refetch + retry.
- Idempotent write replays return identical bodies and status.

## Summary
This API contract makes failure modes predictable and recoverable. Implement the envelope, status mapping, headers, idempotency, and multi-tenant protections uniformly across services. The result is lower support load and safer automation in clients and jobs.