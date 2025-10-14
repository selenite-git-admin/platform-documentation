# Error Handling Security

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define security controls for error surfaces across APIs, jobs, and UI. The goal is to prevent data leakage, preserve tenant isolation, and maintain strong forensic value without exposing sensitive context. This document is aligned with the canonical error envelope and the platform's PostgreSQL-first approach.

## Threat Model
- Information disclosure via verbose error messages
- Cross tenant inference of resource existence
- Token or secret leakage in messages or logs
- Replay abuse of write endpoints
- Amplification through retry storms
- Correlation id misuse for tracking beyond intended scope

## Principles
- Least information to the client
- Rich context to server-side logs only
- Tenancy safe defaults
- Idempotent write paths with replay detection
- Uniform transport security across all modules

## Client Response Hygiene
- Do not include stack traces, SQL, hostnames, or dependency names
- Do not include PII such as emails, phone numbers, customer names
- Messages are short, action oriented, and safe to render in UI
- Include `code`, `message`, `correlation_id`, and a small `details` map only
- Add `Cache-Control: no-store` on all 4xx and 5xx responses

## Tenant Isolation
- Prefer 404 `not_found` over 403 `forbidden` when revealing existence would leak cross tenant information
- Do not echo tenant identifiers in responses
- Store tenant in logs as a one-way hash or tokenized form when possible
- Access checks run before data fetches to avoid timing side channels

## Authentication and Authorization
- 401 `unauthenticated` when token is missing or invalid
- 403 `forbidden` when authenticated but not authorized
- `scope_insufficient` communicates the missing scope without enumerating all scopes
- Gateway validates tokens and injects principal context downstream

## Headers and Transport
- HTTPS only
- `Strict-Transport-Security` enabled for public surfaces
- `X-Correlation-Id` required for all requests and echoed back
- `Retry-After` present on 429 and select 503 to reduce client storms
- ETag and `If-Match` required for read-modify-write flows to prevent lost updates

## Idempotency
- All mutating endpoints accept `Idempotency-Key`
- Replays within 24 hours return the same outcome and `correlation_id`
- Reject duplicate conflicting payloads with `409 conflict` and `details.existing_id` when safe

## Logging and Redaction
- Structured logs include: `code`, `message_safe`, `correlation_id`, `service`, `endpoint`, `http_status`, `retryable`, and a redacted `details`
- Server-only diagnostic logs may include deeper context but are access controlled and redacted
- Secrets, tokens, cookies, and Authorization headers are never logged
- Apply allow-list to `details` keys and truncate oversize values

## Database and DRR Interaction
- Database errors map to safe `data` codes such as `constraint_violation` or `serialization_failure`
- Do not leak table or column names to clients
- DRR incidents are referenced by ID only. Detailed root cause stays internal

## Evidence Ledger
- All write failures emit a failure audit with `correlation_id`, `code`, and a minimal request summary
- Successful writes emit a matching audit using the same `correlation_id`
- The ledger does not store secrets or payload bodies

## Privacy and Retention
- Error events in PostgreSQL store `tenant_hash` instead of tenant plaintext
- Retention for raw error events is 90 days by default and configurable by Store Policies
- Aggregates may be kept up to 2 years as counts without identifiers
- Access to error data is role-gated and audited

## Rate Limiting and Abuse
- Enforce global and per-tenant limits
- Return 429 with `Retry-After` and optional `limit` and `window_sec` in `details`
- Monitor for tokens that ignore `Retry-After` and throttle or suspend if necessary

## Input Validation
- Validate `X-Correlation-Id`, `Idempotency-Key`, and any user-controlled fields used in error pathways
- Sanitize strings that feed logs or traces to prevent log injection
- Cap `details` map size and key count to avoid memory abuse

## Webhooks and Events
- Webhook responses use the same envelope for non-2xx outcomes
- Acknowledge webhooks only after durable enqueue on our side
- Do not include internal queue names or hostnames in responses

## Testing Checklist
- Negative tests verify no stack traces or SQL are leaked
- Snapshot tests ensure the envelope shape and keys remain stable
- Fuzz tests for error inputs and oversized payloads
- Tenant isolation tests for 404 vs 403 decisions
- Replay tests verify idempotency and outcome stability

## Incident Workflow
- For P1 or P2, scrub recent logs for any accidental leakage patterns
- Rotate any keys suspected of exposure even if not logged
- If leakage reached clients, notify Governance and follow the disclosure policy

## Configuration Defaults
| Setting | Default | Purpose |
|---------|---------|---------|
| `ERROR_BODY_MAX_BYTES` | 4 KB | Prevent oversized responses |
| `ERROR_DETAILS_ALLOWED_KEYS` | allow list per module | Keep payload predictable |
| `ERROR_MESSAGE_SAFE_MODE` | true | Strip potentially sensitive terms |
| `IDEMPOTENCY_WINDOW_HOURS` | 24 | Bind replay safety window |
| `CACHE_CONTROL_FOR_ERRORS` | `no-store` | Prevent caching of sensitive responses |

## Ownership
- Security Engineering defines allow-lists and redaction patterns
- Platform Foundation maintains gateway normalizers and headers
- Service teams implement the envelope and adhere to allow-lists
- SRE monitors for violations and blocks unsafe payloads

## Summary
Security for error surfaces is about reducing exposure while preserving actionable signals. With safe messages, strict headers, tenant isolation, idempotent write paths, and disciplined logging, the platform stays supportable and private by default.