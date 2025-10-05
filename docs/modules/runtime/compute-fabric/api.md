# Compute Fabric – API

## Overview
Public/admin interface for compute fabric operations.

**Base URL**  
`https://api.datajetty.com/api/v1/runtime/compute`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Submit Job
**Purpose:** Submit container/function job  
**Path:** `POST /jobs`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "image":"repo/transform:24","cmd":["/app/run"],"cpu":2,"mem_gib":4,"env":{"TZ":"Asia/Kolkata"} }
```

**Response**
```json
{ "job_id":"job_7","state":"queued"}
```

**Notes**
- Validates image signature and quota.

---

### Get Logs
**Purpose:** Stream job logs  
**Path:** `GET /jobs/{id}/logs`

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
{ "lines":["..."] }
```

**Notes**
- Server‑sent events or websockets supported.

---

### Stop Job
**Purpose:** Terminate job  
**Path:** `POST /jobs/{id}/stop`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "reason":"operator_request" }
```

**Response**
```json
{ "job_id":"job_7","state":"stopping"}
```

**Notes**
- Graceful with timeout; then SIGKILL.

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
