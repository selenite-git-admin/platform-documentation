# Ticketing API

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Provide a compact HTTP contract to create, search, update, and observe tickets. The API is **platform‑scoped** with RBAC‑enforced visibility. Tenant users operate within their tenant scope; platform operators have global access.

## Base path
Service local root. Endpoints are versioned under `/v1`.

## Authentication and authorization
- Service‑to‑service: IAM or signed service tokens
- Tenant users: OAuth2 bearer tokens
- Platform operators: elevated role with global read/write
- All writes must include `Idempotency-Key`

**Visibility rules**
- Tenant callers can only read or mutate tickets where `tenant_id` is in their scope and `visibility != platform_only`
- Platform callers may access platform‑only tickets (`tenant_id = null`) and tenant tickets

## Common headers
| Header | Direction | Purpose |
|---|---|---|
| `Authorization: Bearer <token>` | in | caller identity |
| `Idempotency-Key` | in | deduplicate unsafe writes |
| `X-Correlation-Id` | in/out | trace continuity |
| `Content-Type` | in/out | `application/json` for JSON |
| `Retry-After` | out | backoff hint on 429 |

## Errors
Standard envelope
```json
{"code":"validation_failed","message":"missing title","correlation_id":"01JC...","details":{"field":"title"}}
```

## Create ticket
`POST /v1/tickets`

- `tenant_id` is optional. Omit or set null for **platform incidents**.  
- `visibility` defaults to `tenant`. Use `platform_only` for platform incidents not visible to tenants.

Request
```json
{
  "category": "incident",
  "subcategory": "health_readiness",
  "severity": "p1",
  "title": "Readiness failing for notifications in ap-south-1",
  "summary": "readyz 503 due to database timeout",
  "tenant_id": null,
  "visibility": "platform_only",
  "requester_user_id": "u_123",
  "source": "health",
  "source_ref": "01JC2Q0...",
  "environment": "prod",
  "region": "ap-south-1",
  "links": [
    {"target_type":"service","target_ref":"notifications","relation":"relates_to"}
  ],
  "tags": ["oncall"]
}
```

Headers
- `Idempotency-Key: health-01JC2Q0-01`

Response 201
```json
{
  "id": "018f4a88-...",
  "key": "TCK-2025-00123",
  "state": "new",
  "sla": {"ack_due_at":"2025-10-13T08:00:00Z"},
  "correlation_id": "01JC2Q0..."
}
```

Idempotency
- Repeating the request with the same idempotency key returns 201 or 200 with the same resource

## Get ticket
`GET /v1/tickets/{id}` or `GET /v1/tickets/key/{key}`

Query params
- `include=timeline,links,attachments` optional expansions

Visibility
- Tenant callers receive 404 for tickets outside scope or with `visibility=platform_only`

## Search tickets
`GET /v1/tickets`

Query params
- `q` free text over key, title, summary
- `category`, `subcategory`, `state`, `severity`
- `tenant_id` optional filter; ignored for tenant callers (their scope is implicit)
- `assignee_user_id`, `assignee_team_id`
- `environment`, `region`
- `created_from`, `created_to` ISO 8601
- `page`, `page_size` default 50
- `sort` defaults to `updated_at desc`

Response
```json
{
  "items":[{"id":"018f4a88-...","key":"TCK-2025-00123","title":"...", "state":"ack"}],
  "page":1,
  "page_size":50,
  "total":1234
}
```

## Update ticket
`PATCH /v1/tickets/{id}`

Allowed fields
- `state`, `severity`, `priority`
- `assignee_user_id`, `assignee_team_id`
- `title`, `summary`, `visibility`

## Comments and attachments
`POST /v1/tickets/{id}/comments` includes optional `visibility` for platform‑only notes.  
`POST /v1/tickets/{id}/attachments` returns a signed `upload_url` to S3 (tenant‑prefixed key when applicable).

## Links
`POST /v1/tickets/{id}/links` relates tickets to datasets, connectors, jobs, incidents, evidence, and services.

## Bulk create
`POST /v1/tickets/bulk/create` accepts an array of create payloads; returns 207 with per‑item results.

## Inbound and outbound hooks
Inbound: `POST /v1/hooks/inbound/email`, `POST /v1/hooks/inbound/web` (scoped to tenant or platform).  
Outbound: `POST /v1/webhooks/subscriptions` with HMAC signatures and retries.

## OpenAPI excerpt
```yaml
openapi: 3.0.3
info:
  title: Ticketing API
  version: "2025-10-13"
components:
  schemas:
    TicketCreate:
      type: object
      required: [category, subcategory, severity, title, summary, requester_user_id]
      properties:
        tenant_id: { type: string, nullable: true }
        visibility: { type: string, enum: [platform_only, tenant, mixed], default: tenant }
        # ... other properties as defined above
```

## Security notes
- Enforce RBAC at the query layer; tenant callers cannot request other tenants
- Validate idempotency and reject key reuse with conflicting payloads
- Redact PII on ingest; comments default to `tenant` visibility
- Sign outbound webhooks and verify inbound
- Rate limit per caller and per tenant where applicable

## Summary
A platform‑scoped API with precise visibility controls keeps operations centralized while protecting tenant privacy.