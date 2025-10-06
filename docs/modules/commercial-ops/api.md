# API

## Overview

This document describes the Commercial-Ops HTTP API used to provision tenants, manage plans, ingest and query usage, retrieve invoices, create payments, manage budgets and alerts, and access reconciliation status. The API is versioned and stateless. Canonical terms are tenant and plan. Currency defaults to USD.

The API follows REST conventions with JSON request and response bodies. Authentication uses OAuth 2.0 access tokens with the Bearer scheme or AWS SigV4 for service-to-service calls. Idempotency is enforced on unsafe operations using the `Idempotency-Key` header. All times are UTC ISO 8601 unless noted.

Base path:
```
/api/v1
```

## Authentication

### OAuth 2.0 bearer tokens
- Grant types: client_credentials for server-side integrations, authorization_code for user initiated flows.
- Scopes: `tenant:read`, `tenant:write`, `plan:read`, `billing:read`, `billing:write`, `usage:read`, `usage:write`, `recon:read`.

Example:
```
Authorization: Bearer <token>
```

### AWS SigV4 (optional)
- Allowed for operator automations running in AWS.
- Required headers as per AWS Signature Version 4.

## Idempotency

- Provide `Idempotency-Key` for POST operations that create resources or trigger jobs.
- The server stores request hash for 24 hours per key.
- Repeat calls with the same key return the original status and body.

Example:
```
Idempotency-Key: 2c4a6e1f-e2a7-49c5-9c3c-7c5b0e7ee9aa
```

## Pagination

- Cursor based pagination using `page_size` and `page_token` query parameters.
- Responses include `next_page_token` when more data is available.
- Maximum page size is 200 unless otherwise stated.

## Error Model

Errors use HTTP status codes with a structured body.

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "message": "plan_code is required",
    "details": [
      {"field": "plan_code", "reason": "missing"}
    ],
    "trace_id": "req-01J9R1W3W2AQS0"
  }
}
```

Common codes:
- `INVALID_ARGUMENT`
- `NOT_FOUND`
- `ALREADY_EXISTS`
- `FAILED_PRECONDITION`
- `PERMISSION_DENIED`
- `RATE_LIMITED`
- `INTERNAL`

## Resource Names

- Tenants: `TEN-<slug or uuid>`
- Plans: immutable `plan_code` value
- Invoices: `INV-<YYYYMM>-<tenant-id-suffix>`
- Payments: `PAY-<uuid>`

## Rate Limits

- Default 600 requests per minute per token.
- Burst limits apply; 429 includes retry-after seconds.

## Webhooks

Incoming webhooks allow notifications for invoice events and payment confirmations.

| Event | Description | Payload root |
|-------|-------------|--------------|
| `invoice.issued` | Invoice created and visible to tenant | `invoice` |
| `invoice.paid` | Payment reconciled to invoice | `invoice` |
| `budget.breached` | Budget threshold crossed | `budget` |
| `recon.failed` | Reconciliation run failed | `recon` |

Verification:
- Each webhook includes `X-Signature` HMAC SHA-256 using a shared secret.
- Replay protection via `X-Timestamp` and a five minute window.

## Versioning and Stability

- Breaking changes create a new major path `/api/v2`.
- Fields are only added, not removed, within a major version.
- Deprecated fields are marked in the schema for one cycle before removal in a new major version.

---

## Tenants

### Create tenant
`POST /api/v1/tenants`

Request:
```json
{
  "tenant_id": "TEN-00123",
  "tenant_name": "Acme Ltd",
  "billing_contact": {
    "name": "Jane Doe",
    "email": "jane@acme.example"
  },
  "plan_code": "ENT-Standard-v1",
  "seats": 10
}
```

Response `201`:
```json
{
  "tenant_id": "TEN-00123",
  "tenant_name": "Acme Ltd",
  "status": "active",
  "plan_binding": {
    "plan_code": "ENT-Standard-v1",
    "period_start": "2025-10-01",
    "period_end": "2025-10-31",
    "seats": 10
  }
}
```

Notes:
- Requires `tenant:write` scope.
- Fails with `ALREADY_EXISTS` if `tenant_id` is taken.

### Get tenant
`GET /api/v1/tenants/{tenant_id}`

Response `200`:
```json
{
  "tenant_id": "TEN-00123",
  "tenant_name": "Acme Ltd",
  "status": "active",
  "current_plan": "ENT-Standard-v1",
  "seats": 10,
  "created_at": "2025-09-10T11:02:03Z"
}
```

### Update tenant
`PATCH /api/v1/tenants/{tenant_id}`

Request:
```json
{
  "tenant_name": "Acme North America",
  "seats": 25
}
```

Response `200` includes updated fields only.

### List tenants
`GET /api/v1/tenants?page_size=50&page_token=...`

Response:
```json
{
  "tenants": [ { "tenant_id": "TEN-00123", "tenant_name": "Acme Ltd" } ],
  "next_page_token": "eyJvZmZzZXQiOjUw..."
}
```

---

## Plans

### Create or update plan
`PUT /api/v1/plans/{plan_code}`

Request:
```json
{
  "plan_family": "Enterprise",
  "version": "v1",
  "currency": "USD",
  "base_price_usd": 1999.00,
  "base_seats": 10,
  "entitlements": {
    "metrics_caps": {
      "storage_gb_peak": 5000,
      "egress_gb": 1000,
      "runner_hours": 300
    }
  },
  "effective_from": "2025-10-01"
}
```

Response `200` or `201` with plan body.

### Get plan
`GET /api/v1/plans/{plan_code}`

### List plans
`GET /api/v1/plans?active_only=true`

### Bind plan to tenant
`POST /api/v1/tenants/{tenant_id}/plan-bindings`

Request:
```json
{
  "plan_code": "ENT-Standard-v1",
  "effective_from": "2025-10-01",
  "seats": 10,
  "proration": true
}
```

Response includes computed period and proration factor.

---

## Usage

### Ingest usage snapshot
`POST /api/v1/usage/snapshots`

Request:
```json
{
  "tenant_id": "TEN-00123",
  "metric_code": "egress_gb",
  "metric_value": 12.34,
  "usage_date": "2025-10-06"
}
```

Response `202`:
```json
{"status": "accepted", "ingest_id": "ing-01J9R3..."}
```

### Query usage
`GET /api/v1/usage/snapshots?tenant_id=TEN-00123&metric_code=storage_gb_peak&from=2025-10-01&to=2025-10-31&page_size=100`

Response:
```json
{
  "items": [
    {"tenant_id":"TEN-00123","metric_code":"storage_gb_peak","metric_value": 312.9,"usage_date":"2025-10-05"}
  ],
  "next_page_token": null
}
```

Notes:
- `usage:read` scope required.
- Data is immutable after ingestion. Corrections are posted as new snapshots with the correct value and will supersede in downstream aggregations.

---

## Budgets and Alerts

### Create budget
`POST /api/v1/budgets`

Request:
```json
{
  "scope_type": "tenant",
  "scope_ref": "TEN-00123",
  "metric_type": "aws_cost",
  "period": "monthly",
  "target_usd": 1500.00,
  "thresholds": {"warning": 0.8, "critical": 0.95}
}
```

Response `201` includes `budget_id`.

### Get budget status
`GET /api/v1/budgets/{budget_id}`

### List alerts
`GET /api/v1/alerts?tenant_id=TEN-00123&state=open`

Response:
```json
{
  "alerts": [
    {
      "alert_id": "AL-9f1b6",
      "metric": "egress_gb",
      "level": "critical",
      "value": 980.2,
      "cap": 1000.0,
      "timestamp": "2025-10-06T02:15:00Z",
      "evidence": [{"type":"sql","ref":"aurora:qry-abc"}]
    }
  ]
}
```

---

## Invoices

### Generate invoice
`POST /api/v1/invoices:generate`

Request:
```json
{
  "tenant_id": "TEN-00123",
  "period_start": "2025-09-01",
  "period_end": "2025-09-30"
}
```

Response `202`:
```json
{"run_id":"invgen-01J9R4..."}
```

### Get invoice header
`GET /api/v1/invoices/{invoice_id}`

Response:
```json
{
  "invoice_id":"INV-202509-TEN00123",
  "tenant_id":"TEN-00123",
  "period_start":"2025-09-01",
  "period_end":"2025-09-30",
  "status":"issued",
  "subtotal_usd": 2245.00,
  "tax_usd": 0,
  "total_usd": 2245.00,
  "issued_at": "2025-10-02T08:05:00Z"
}
```

### Get invoice detail lines
`GET /api/v1/invoices/{invoice_id}/lines?page_size=200&page_token=...`

Line item:
```json
{
  "line_id": 101,
  "line_type": "allocation",
  "metric_code": "nat_gb_processed",
  "quantity": 450.0,
  "unit": "GB",
  "unit_price_usd": 0.0,
  "amount_usd": 112.45,
  "references": {"allocation_ids":[10111,10112]}
}
```

### List invoices by tenant
`GET /api/v1/invoices?tenant_id=TEN-00123&from=2025-07-01&to=2025-10-31`

---

## Payments

### Create payment
`POST /api/v1/payments`

Request:
```json
{
  "invoice_id": "INV-202509-TEN00123",
  "method": "bank_transfer",
  "amount_usd": 2245.00,
  "provider_ref": "NEFT-UTR-12345"
}
```

Response `201`:
```json
{
  "payment_id": "PAY-01J9R6...",
  "status": "confirmed"
}
```

### List payments for an invoice
`GET /api/v1/invoices/{invoice_id}/payments`

---

## Top-ups and Upgrades

### Purchase top-up
`POST /api/v1/topups`

Request:
```json
{
  "tenant_id": "TEN-00123",
  "sku_code": "TOPUP_EGRESS_200GB"
}
```

Response `201` includes applied cap adjustment for the current cycle.

### Upgrade plan
`POST /api/v1/tenants/{tenant_id}:upgrade-plan`

Request:
```json
{"plan_code":"ENT-Premium-v1","effective_from":"2025-10-10","proration":true}
```

Response shows new binding and proration factor.

---

## Reconciliation

### Get reconciliation summary
`GET /api/v1/reconciliation/summary?period=2025-09`

Response:
```json
{
  "period":"2025-09",
  "aws_total_usd": 23044.25,
  "allocated_total_usd": 22945.10,
  "invoiced_total_usd": 22945.10,
  "variance_usd": 99.15,
  "variance_pct": 0.43,
  "status": "ok"
}
```

### Get reconciliation exceptions
`GET /api/v1/reconciliation/exceptions?period=2025-09&state=open`

Response:
```json
{
  "exceptions": [
    {
      "exception_id":"RX-202509-0007",
      "tenant_id":"TEN-00456",
      "category":"Tagging",
      "description":"Missing user:tenant_id for NAT bytes",
      "variance_pct": 0.21,
      "status":"open"
    }
  ]
}
```

---

## Seats and Users

### Set seat count for tenant
`PUT /api/v1/tenants/{tenant_id}/seats`

Request:
```json
{"seats": 25}
```

Response includes effective date and plan validation.

### Get seat usage
`GET /api/v1/tenants/{tenant_id}/seats/usage?from=2025-10-01&to=2025-10-31`

Response:
```json
{"active_users": 18, "seats": 25, "utilization": 0.72}
```

---

## Health and Metadata

### Service health
`GET /api/v1/health`

Response `200`:
```json
{
  "status": "ok",
  "cur_freshness_days": 1,
  "db_read_replica_lag_ms": 24
}
```

### OpenAPI schema
`GET /api/v1/openapi.json`

---

## Security

- OAuth scopes restrict access by resource and operation.
- Every request is audit logged with tenant_id, action, and trace_id.
- Responses omit internal AWS resource identifiers.
- Sensitive content such as bank account numbers is redacted.

---

## Examples

### Create tenant and bind plan

```bash
curl -X POST https://api.example.com/api/v1/tenants  -H "Authorization: Bearer $TOKEN"  -H "Content-Type: application/json"  -H "Idempotency-Key: $(uuidgen)"  -d '{
  "tenant_id":"TEN-00123",
  "tenant_name":"Acme Ltd",
  "plan_code":"ENT-Standard-v1",
  "seats":10
 }'
```

### Query egress usage

```bash
curl -s "https://api.example.com/api/v1/usage/snapshots?tenant_id=TEN-00123&metric_code=egress_gb&from=2025-10-01&to=2025-10-31"  -H "Authorization: Bearer $TOKEN"
```

### Download invoice PDF

`GET /api/v1/invoices/{invoice_id}/export?format=pdf` returns a signed URL with 10 minute expiry.

---

## Response Conventions

- Amount fields end with `_usd` and use numeric types with scale 2 or 6.
- Date fields use `YYYY-MM-DD`.
- Timestamp fields use RFC 3339 with timezone `Z`.
- Enumerations appear as lowercase strings.
- Unknown fields are ignored by the server for forward compatibility.

---

## Change Log

- v1.0 initial release with tenants, plans, usage, budgets, invoices, payments, reconciliation, seats, and health.
