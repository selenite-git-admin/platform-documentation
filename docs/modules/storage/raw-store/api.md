# Raw Store – API

## Overview
Public/admin interface for raw store operations.

**Base URL**  
`https://api.datajetty.com/api/v1/storage/raw`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Register Object
**Purpose:** Register new raw object with metadata  
**Path:** `POST /objects`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "source":"s3://vendor/file.csv","checksum":"sha256:...","bytes":12345,"tags":{"vendor":"acme"} }
```

**Response**
```json
{ "object_id":"obj_1","partition":"dt=2025-10-05","receipt_id":"rcp_9" }
```

**Notes**
- Object becomes immutable; updates create new objects.

---

### List Objects
**Purpose:** List objects by tag/time  
**Path:** `GET /objects?tag=vendor:acme&from=2025-10-01`

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
{ "items":[{"object_id":"obj_1","bytes":12345}] }
```

**Notes**
- Supports pagination and ETag caching.

---

### Ingest Event
**Purpose:** Append streaming event  
**Path:** `POST /events`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "topic":"sales","event":{"order_id":"...","amount":123.45} }
```

**Response**
```json
{ "offset":987654 }
```

**Notes**
- Idempotent by event key if provided.

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
