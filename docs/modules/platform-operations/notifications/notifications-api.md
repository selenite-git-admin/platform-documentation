# Notifications API

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
A channel-agnostic HTTP API for generating notifications to users and systems. Producers submit a single request with a `template_id` and variables. The platform handles rendering, routing, retry, and provider abstraction. All errors use the platform's canonical error envelope.

## Design Principles
- Uniform contract for email, Slack, in-app, and webhooks
- Idempotent writes, at-least-once delivery per channel
- Safe templates with schema validation and localization
- Observability by correlation id, template, channel, tenant
- Zero engineering at the edges: simple API, no channel code in producers

## Authentication
- OAuth2/JWT bearer, scopes:
  - `notify:send` to create requests
  - `notify:preview` to render previews
  - `notify:read` to fetch status
  - `notify:admin` to manage templates and destinations

## Headers
| Header | Direction | Purpose |
|--------|-----------|---------|
| `Authorization: Bearer <token>` | in | auth |
| `X-Correlation-Id` | in/out | end-to-end tracing (UUIDv7) |
| `Idempotency-Key` | in | deduplicate writes for 24h |
| `Retry-After` | out | present on `429` and select `503` |
| `Cache-Control` | out | `no-store` on 4xx/5xx |

## Core Resources
- `/notifications` – submit, schedule, fan-out
- `/notifications/{id}` – status and outcomes
- `/notifications/preview` – render without sending
- `/templates` – list metadata (admin)
- `/templates/{templateId}/versions/{version}` – fetch version metadata (admin)
- `/destinations` – tenant-level channel config (admin read-only from this API)

---

## Create Notification
`POST /notifications`

Submit a request to send a notification to one or more channels and recipients.

### Request
```json
{
  "template_id": "password-reset",
  "version": "latest",
  "channel": ["email","inapp"],
  "to": [
    {"type":"user","id":"a2de6d2c-5a1d-4d3e-9b7c-0c2b0f4f3a4b"}
  ],
  "variables": {
    "name": "Riya",
    "reset_url": "https://app.example.com/reset?token=..."
  },
  "priority": "normal",
  "schedule_at": "2025-10-13T09:30:00Z"
}
```

Field notes
- `version` may be `latest` or a specific version id. If omitted, `latest` is implied.
- `to` supports `{ "type":"user","id":UUID }` or `{ "type":"system","url":"https://..." }` for webhooks.
- `channel` is a list; each channel executes independently with at-least-once guarantees.
- `schedule_at` optional; must be within 7 days in the future; otherwise rejected.

### Response
```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "id": "0f0cb2f4-62e0-7a3b-8a11-b9c1d2b3e4f5",
  "correlation_id": "01JC2Q0YQ9S0Y0K7Q2YJX8G7QK",
  "status": "queued"
}
```

### Errors
- `400 invalid_request` for schema violations
- `401 unauthenticated` / `403 forbidden` for scope issues
- `404 not_found` if template not visible to tenant
- `409 conflict` for duplicate `Idempotency-Key` with different payload
- `429 rate_limited` when tenant/channel limits exceeded
- `503 dependency_unavailable` for provider outage

---

## Get Notification Status
`GET /notifications/{id}`

### Response
```json
{
  "id": "0f0cb2f4-62e0-7a3b-8a11-b9c1d2b3e4f5",
  "template_id": "password-reset",
  "version": "2025.10.01-1",
  "to": [{"type":"user","id":"a2de6d2c-5a1d-4d3e-9b7c-0c2b0f4f3a4b"}],
  "submitted_at": "2025-10-13T09:30:00Z",
  "status": "partially_delivered",
  "channels": [
    {
      "name": "email",
      "state": "delivered",
      "attempts": 1,
      "provider_id": "AQEAMh7...",
      "delivered_at": "2025-10-13T09:30:09Z"
    },
    {
      "name": "inapp",
      "state": "pending",
      "attempts": 0
    }
  ]
}
```

States: `queued`, `pending`, `delivered`, `failed`, `dead_lettered`, `partially_delivered`.

---

## Preview Template
`POST /notifications/preview`

Render a template with variables without sending.

### Request
```json
{
  "template_id": "password-reset",
  "version": "latest",
  "channel": "email",
  "variables": {
    "name": "Riya",
    "reset_url": "https://app.example.com/reset?token=..."
  },
  "locale": "en-IN"
}
```

### Response
```json
{
  "subject": "Reset your password",
  "body_text": "Hi Riya, use this link to reset your password...",
  "body_html": "<p>Hi Riya,</p><p>Use this link...</p>"
}
```

Errors include `validation_failed` when required variables are missing or wrong type.

---

## Template Metadata
`GET /templates`

List visible templates for the caller's tenant.
```json
{
  "items": [
    {"id":"password-reset","name":"Password Reset","locales":["en-US","en-IN"],"active_version":"2025.10.01-1"},
    {"id":"kpi-alert","name":"KPI Alert","locales":["en-US"],"active_version":"2025.09.12-2"}
  ]
}
```

`GET /templates/{templateId}/versions/{version}` returns variables schema and policy flags.

---

## Destinations (read)
`GET /destinations`

Return configured per-tenant channel settings (masked).
```json
{
  "email": {"from":"no-reply@example.com","domain_status":"verified"},
  "slack": {"bot":"enabled"},
  "webhook": {"endpoints":[{"name":"ERP","url":"https://...","verified":true}]},
  "inapp": {"enabled":true}
}
```

Destination writes are managed via Admin surfaces, not this API.

---

## Webhooks
Provider callbacks use a signed POST to `/webhooks/notification`. Payload shape:
```json
{
  "provider": "ses",
  "event": "bounce",
  "message_id": "AQEAMh7...",
  "reason": "mailbox_full",
  "timestamp": "2025-10-13T09:31:00Z",
  "signature": "base64(hmac_sha256(body))"
}
```
- Non-2xx responses are retried by the provider; we enforce idempotency by `message_id`.

---

## Errors
All errors conform to the standard envelope:
```json
{ "code":"rate_limited","message":"Too many requests","correlation_id":"01JC2Q0...","details":{"retryable":true,"limit":2000,"window_sec":60} }
```

Common codes:
- `invalid_request`, `validation_failed`, `unsupported_media_type`
- `unauthenticated`, `forbidden`, `scope_insufficient`
- `not_found`, `conflict`, `already_exists`
- `rate_limited`
- `timeout`, `dependency_unavailable`, `internal_error`

---

## Idempotency
- Supply `Idempotency-Key` for all POSTs.
- Replays within 24 hours return the original response body and status.
- A different payload with the same key returns `409 conflict`.

---

## Rate Limits
- Default: 50 RPS per tenant on `POST /notifications` with token bucket bursts to 100.
- Channel-specific daily caps configurable via Subscription module.
- On `429`, clients must honor `Retry-After`.

---

## OpenAPI (excerpt)
```yaml
openapi: 3.0.3
info:
  title: Notifications API
  version: "2025-10-13"
paths:
  /notifications:
    post:
      operationId: createNotification
      security: [{ bearerAuth: [] }]
      parameters:
        - in: header
          name: Idempotency-Key
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateNotificationRequest'
      responses:
        '202':
          description: Queued
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateNotificationResponse'
        '4XX':
          description: Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
  schemas:
    ErrorEnvelope:
      type: object
      properties:
        code: { type: string }
        message: { type: string }
        correlation_id: { type: string }
        details: { type: object, additionalProperties: true }
```

---

## Testing Checklist
- Idempotent replay returns identical body and status
- Preview fails when variables are missing or wrong type
- 429 includes `Retry-After` and SDK backoff honors it
- Webhook signature verified and duplicates ignored
- Partial delivery is reflected in channel states and audit entries

## Summary
A simple, durable API for all notification channels. Producers call one endpoint; the platform handles the rest with strong guarantees around idempotency, retries, observability, and security.