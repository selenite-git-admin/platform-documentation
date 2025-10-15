# Error Handling

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Problem Statement
Inconsistent error shapes and retry semantics create avoidable outages and support churn. We standardize a single envelope, taxonomy, and set of contracts that work for HTTP APIs, background jobs, and UI surfaces — all without leaking internals or vendor‑specific details.

## Design Goals
- Predictable: same envelope, same codes, same HTTP mapping everywhere.
- Actionable: every error communicates retryability and next steps.
- Traceable: correlation id binds logs, metrics, and Evidence Ledger.
- Tenant‑safe: no data leakage across tenants; messages are safe for display.
- Low‑ops: zero extra services; simple SDK adapters; works in Lambda and containers.

## Non‑Goals
- We will not standardize third‑party connectors that cannot conform; adapters translate them.
- We will not expose internal stack traces or dependency names in client responses.

## Canonical Envelope
All client‑facing errors use this shape. It is stable and version‑agnostic.

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

### Field Semantics
| Field | Required | Type | Description |
|------|----------|------|-------------|
| `code` | yes | string | Stable symbolic identifier. |
| `message` | yes | string | Safe, human‑readable explanation. No PII. |
| `correlation_id` | yes | uuid (v7) | End‑to‑end trace id. Echoed by gateway if provided. |
| `details` | no | object | Machine‑readable context. Keys are stable where defined. |

### Stable `details` Keys
- `field` (string): failing input field for validation errors.
- `retryable` (bool): client hint for backoff logic.
- `hint` (string): optional human guidance.
- `limit`, `window_sec` (numbers): for `rate_limited` responses.
- `expected_etag` (string): for `stale_read` remediation.

## Error Taxonomy
We group errors by responsibility. Codes are stable; do not invent per‑service codes.

| Domain | Codes | Rationale |
|--------|-------|-----------|
| Request | `invalid_request`, `validation_failed`, `unsupported_media_type` | Client can fix payload. |
| Auth | `unauthenticated`, `forbidden`, `scope_insufficient` | Identity/authorization issues. |
| Resource | `not_found`, `conflict`, `already_exists` | State mismatch or idempotency. |
| Rate | `rate_limited` | Platform backpressure. |
| Runtime | `timeout`, `dependency_unavailable`, `internal_error` | Transient or platform faults. |
| Data | `constraint_violation`, `serialization_failure`, `stale_read` | Database invariants and concurrency. |

## HTTP Mapping
| HTTP | Typical Codes | Cacheability |
|------|---------------|--------------|
| 400 | `invalid_request`, `validation_failed` | no-store |
| 401 | `unauthenticated` | no-store |
| 403 | `forbidden`, `scope_insufficient` | no-store |
| 404 | `not_found` | no-store |
| 409 | `conflict`, `already_exists` | no-store |
| 412 | `stale_read` | no-store |
| 415 | `unsupported_media_type` | no-store |
| 429 | `rate_limited` | respect `Retry-After` |
| 500 | `internal_error` | no-store |
| 502‑504 | `dependency_unavailable`, `timeout` | retry with backoff |

### Headers
- `X-Correlation-Id`: echo inbound or generate if absent.
- `Retry-After`: required on `429`, optional on `503`.
- `Cache-Control: no-store`: default for 4xx/5xx; prevents leaking identifiers.
- `ETag` and `If-None-Match`: pair with `412 stale_read` semantics.

## Retry Contract
| Code | Client Action | Default Backoff |
|------|---------------|------------------|
| `rate_limited` | retry | exponential with jitter, honor `Retry-After` |
| `timeout` | retry | exponential with jitter |
| `dependency_unavailable` | retry | linear for 30s then exponential |
| `serialization_failure` | retry | up to 3 attempts at SERIALIZABLE |
| `stale_read` | refetch | refresh ETag or re‑GET before write |
| others | do not retry | fix input, auth, or state |

## Idempotency
- **Writes** must accept `Idempotency-Key` and return the same result on replays within a 24h window.
- **Conflicts** should return `409 conflict` with a pointer to existing resource id in `details.existing_id`.

## Multi‑Tenant Safety
- Never leak whether a resource exists across tenants. Prefer `404 not_found` to `403` when revealing existence is unsafe.
- Include `tenant_id` in server logs only; never echo in the response body.

## Gateway Behavior
- Normalizes raw errors to the canonical envelope.
- Generates `X-Correlation-Id` if missing and injects into downstream calls.
- Scrubs messages for secrets and PII tokens.

## SDK Guidance
- Provide `isRetryable(code)` helper.
- Surface `correlationId` and `details` in exceptions.
- Built‑in exponential backoff with jitter; read `Retry-After` when present.

## Evidence Ledger
- For write attempts, log both failure and eventual success using the same `correlation_id` to create a verifiable chain.

## Examples
### Validation
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{ "code":"validation_failed","message":"`name` must not be empty","correlation_id":"01J...","details":{"field":"name","retryable":false} }
```

### Rate Limited
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 8
Content-Type: application/json

{ "code":"rate_limited","message":"Too many requests","correlation_id":"01J...","details":{"retryable":true,"limit":2000,"window_sec":60} }
```

### Stale Read
```http
HTTP/1.1 412 Precondition Failed
ETag: "d41d8cd98f00b204e9800998ecf8427e"

{ "code":"stale_read","message":"Resource changed; GET latest and retry","correlation_id":"01J...","details":{"retryable":true,"expected_etag":"d41d8..."} }
```

## Edge Cases
- **Partial failures** in batch endpoints: return 207 Multi‑Status only for truly heterogeneous outcomes; otherwise fail the batch with a single envelope and list bad items in `details.bad_items`.
- **Webhooks**: respond `2xx` only after durable enqueue; on processor errors, use the same envelope but never expose internal queue names.
- **Streaming**: errors carried in control channel with the same shape; include `offset` in `details`.

## Observability Contract
- Metrics: `error.by_code`, `error.rate`, `retry.success_rate`.
- Logs: include `code`, `correlation_id`, `tenant_id?`, `endpoint`, `http_status`.
- Traces: tag spans with `error.code`, `error.retryable`.

## Runbook Hooks
- P1: 5xx > 1% for 5m across services → page on‑call, check shared dependencies, roll back last alias if correlated.
- P2: spikes in `serialization_failure` → inspect DB locks and hot partitions; reduce batch size.
- P3: `rate_limited` spikes → audit offending tokens and adjust per‑client limits.

## Security Guardrails
- No stack traces to clients.
- No secrets or emails in `message`.
- `Cache-Control: no-store` on all 4xx/5xx.

## FAQs
**Should we ever use service‑specific codes?** No. Use the stable taxonomy; put specifics in `details`.  
**Can clients depend on messages?** No. Only `code`, `correlation_id`, and documented `details` keys are stable.  
**Is `code` per‑HTTP status?** No. Status indicates class; `code` communicates action.

## Summary
This spec makes errors predictable, debuggable, and safe. Use it for every API and job, and wire the SDK helpers to the same taxonomy and retry semantics.