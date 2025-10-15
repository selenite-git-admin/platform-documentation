# GDP Calendar – API

## Overview
Public/admin interface for gdp calendar operations.

**Base URL**  
`https://api.datajetty.com/api/v1/storage/calendar`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Set Schedule
**Purpose:** Create/update dataset schedule  
**Path:** `POST /schedules`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dataset":"ds_sales","cron":"0 2 * * *","timezone":"Asia/Kolkata" }
```

**Response**
```json
{ "schedule_id":"sch_9","status":"active" }
```

**Notes**
- Uses tenant timezone for SLAs.

---

### List Runs
**Purpose:** List historical runs  
**Path:** `GET /runs?dataset=ds_sales&limit=20`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{}
```

**Response**
```json
{ "items":[{"run_id":"run_1","status":"success","ended_at":"2025-10-05T02:33:00+05:30"}] }
```

**Notes**
- Supports pagination and filtering by status.

---

### Subscribe Webhook
**Purpose:** Receive notifications  
**Path:** `POST /subscriptions`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dataset":"ds_sales","url":"https://example.com/hook","events":["run.success","run.failed"] }
```

**Response**
```json
{ "subscription_id":"sub_77","status":"active" }
```

**Notes**
- Webhooks are signed; retries with backoff.

---

## Error Model
| HTTP | Title | Example |
|------|-------|---------|
| 400 | Bad Request | {"error":"invalid_request"} |
| 401 | Unauthorized | {"error":"unauthorized"} |
| 403 | Forbidden | {"error":"forbidden"} |
| 404 | Not Found | {"error":"not_found"} |
| 409 | Conflict | {"error":"version_conflict"} |
| 429 | Too Many Requests | {"error":"rate_limited"} |
| 500 | Internal Error | {"error":"internal_error"} |
| 503 | Service Unavailable | {"error":"dependency_down"} |

## Rate Limits
Documented per endpoint; defaults: 10 rps per tenant.

## References
- [Data Model](data-model.md) · [Runbook](runbook.md) · [Security](security.md)
