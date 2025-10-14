# Notifications Security

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Protect people and systems from information disclosure, spoofing, abuse, and replay risks across all notification channels. This guidance covers API, queue, workers, channel adapters, and providers such as SES, Slack, and webhooks.

## Threat model
- Leakage of PII through templates, variables, logs, or error surfaces
- Account or domain misuse through spoofed mail or weak sender policy
- Token leakage for Slack or other providers
- Replay of write requests or provider callbacks
- Cross tenant inference through status endpoints or delivery outcomes
- Phishing and link tampering in messages
- Partner webhooks that bypass signature checks
- Abuse through high rate submission or fan out

## Security principles
- Least information in client responses and UI
- Strict separation of secrets from content and metadata
- Tenant isolation everywhere
- Signed webhooks and idempotent writes
- Privacy by default with short retention for raw data

## Authentication and authorization
- OAuth2 or JWT bearer with scopes
  - `notify:send` create requests
  - `notify:preview` template rendering without sending
  - `notify:read` read status
  - `notify:admin` manage templates and destinations
- All write paths require `Idempotency-Key`
- Access checks enforce tenant boundary before reading template metadata or destinations

## Transport and headers
- HTTPS only for API and webhooks
- HSTS on public surfaces
- `X-Correlation-Id` required and echoed back
- `Cache-Control: no-store` for all error responses
- `Retry-After` on 429 and selected 503
- CORS restricted to allowed origins for in app flows

## Template governance
- Templates stored server side with versioning and locale
- Variables validated against JSON Schema at submit and preview
- Do not allow executable logic in templates
- Link rendering supports allow list for domains and adds `rel="noopener noreferrer"`
- Optional link wrapping for click tracking must sign redirect tokens and expire them

## PII and content hygiene
- Avoid putting sensitive personal data into variables
- Redact variables at rest and in logs
- Never log email subjects or bodies
- UI preview hides PII by default
- Suppression lists contain PII and are role gated

## Email channel hardening
- Use SES or equivalent with verified domains and DKIM keys
- SPF and DMARC records required before production
- From domain must be tenant validated or platform owned subdomain
- Bounce and complaint feedback loops update suppression lists in near real time
- Do not inline secrets or access tokens in links
- Provide a tenant scoped unsubscribe or manage preferences link where mandated

## Slack channel hardening
- Use bot tokens stored in the Secrets module only by handle reference
- Scope tokens to the minimum permissions
- Rotate tokens on join leave events or suspected leakage
- Validate workspace and channel id against tenant configuration
- Rate limit sends per tenant to avoid abuse

## Webhook channel hardening
- Require HTTPS with modern TLS
- Sign requests with HMAC SHA 256 using a per destination secret
- Include `X-Signature` and `X-Timestamp` headers and reject if older than five minutes
- Enforce idempotency with `Idempotency-Key` and deduplicate by provider id
- Maintain allow list of destination hosts and reject raw IPs
- Limit body size and content type to `application/json`

## Provider callbacks
- Verify provider signatures on SES style notifications and Slack events
- Treat callbacks as untrusted until signature and timestamp pass checks
- Apply idempotency on provider message id before updating state
- Store only minimal fields required for audit

## Rate limiting and abuse controls
- Per tenant token bucket on `POST /notifications`
- Per channel daily caps by tenant controlled by Subscription
- Back pressure to workers when provider limits are reached
- Auto suppression for repeated bounces and complaints with expiry

## Idempotency and replay protection
- Require `Idempotency-Key` on writes and persist for at least 24 hours
- Return original response for a replay with identical payload
- Return `409 conflict` for same key with different payload and log the attempt
- Include `Idempotency-Key` on downstream provider calls when supported

## Data model privacy
- `notification_request.variables` stored in redacted form only
- Email bodies and full webhook payloads are not stored
- Secrets are never stored in destination config, use handles to Secrets
- `notification_attempt.last_error_details` is allow listed and truncated

## Observability hygiene
- Structured logs contain only safe fields and hashed tenant identifiers when required
- Correlation id present in all logs for forensics
- Evidence Ledger records write attempts and outcomes without payload bodies

## Status API safety
- Do not reveal tenant or user specific details outside of tenant boundary
- For mixed outcomes return channel states without provider specifics
- Pagination and filters enforce caller tenant
- Avoid timing side channels by normalizing 404 vs 403 based on access policy

## Retention and deletion
- Requests and attempts retained 90 days by default
- Aggregates retained two years
- Suppressions retained until expiry or manual clear
- Follow Store Policies for region specific requirements
- Provide tenant self service export for audit without raw content

## Key management
- Secrets live in the Secrets module with automatic rotation options
- DKIM keys rotated yearly or on suspicion of compromise
- Webhook destination secrets rotated every 180 days
- Access to secrets audited and least privilege by role

## Configuration defaults
| Setting | Default | Purpose |
|---|---|---|
| `NOTIF_ALLOWED_LINK_HOSTS` | explicit allow list | Prevent phishing and data exfiltration |
| `NOTIF_MAX_VARIABLE_BYTES` | 4 KiB | Limit variable payloads |
| `NOTIF_WEBHOOK_MAX_BODY_BYTES` | 256 KiB | Protect workers from large payloads |
| `NOTIF_SIGNATURE_SKEW_SEC` | 300 | Prevent replay |
| `NOTIF_IDEMPOTENCY_WINDOW_HOURS` | 24 | Stable replay behavior |
| `NOTIF_SUPPRESSION_TTL_DAYS` | 365 | Auto cleanup |
| `NOTIF_RATE_LIMIT_RPS` | 50 | Default per tenant cap |

## Testing checklist
- Negative tests confirm no stack traces or SQL in API responses
- Schema validation fails with `validation_failed` and safe messages
- Webhook signature and timestamp verification rejects tampered requests
- Idempotent replay returns identical response
- SES domain verification and DKIM pass before can send
- Bounce and complaint loops update suppression tables
- Token scope tests for Slack and provider APIs
- Redaction tests for all logs and stored variables

## Incident workflow highlights
- For suspected leakage scrub recent logs and rotate keys
- Pause affected templates or channels through configuration
- Notify Governance for any incident with possible customer impact
- Post incident add detection rules and expand allow lists or schema hints

## Summary
Security in Notifications is about safe content, strict transport guarantees, tenant isolation, and disciplined handling of secrets and callbacks. With clear template governance, signed webhooks, idempotent writes, and privacy controls in the store and logs, the module stays safe for users and operators.