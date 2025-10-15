# Action Delivery – API

## Overview
Public interface for action delivery operations (tenant/admin-scoped as indicated).

**Base URL**  
`https://api.datajetty.com/api/v1/action/delivery`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Endpoint Health
**Purpose:** Check status of a delivery endpoint  
**Path:** `GET /endpoints/{id}/health`

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
{ "endpoint_id":"e_7","status":"healthy","latency_ms":120 }
```

**Notes**
- Admin only; aggregates recent delivery metrics.

---

### DLQ Inspect
**Purpose:** List DLQ entries  
**Path:** `GET /dlq?tenant=t_123`

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
{ "items":[{"job_id":"j_7","reason":"429 from receiver"}] }
```

**Notes**
- Supports pagination.

---

### Replay
**Purpose:** Replay DLQ message  
**Path:** `POST /dlq/{job_id}/replay`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "force": true }
```

**Response**
```json
{ "job_id":"j_7","state":"queued" }
```

**Notes**
- Requires admin role and endpoint revalidation.

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
