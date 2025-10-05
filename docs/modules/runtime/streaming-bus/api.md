# Streaming Bus – API

## Overview
Public/admin interface for streaming bus operations.

**Base URL**  
`https://api.datajetty.com/api/v1/runtime/stream`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Topic
**Purpose:** Provision topic  
**Path:** `POST /topics`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "name":"orders","partitions":8,"retention_h":24 }
```

**Response**
```json
{ "topic":"orders","status":"active"}
```

**Notes**
- Validates naming, partitions, retention.

---

### List Consumer Groups
**Purpose:** Discover consumer groups  
**Path:** `GET /consumers?topic=orders`

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
{ "items":[{"group":"g_orders","lag":12}] }
```

**Notes**
- Supports pagination.

---

### Replay
**Purpose:** Replay messages from watermark  
**Path:** `POST /replay`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "topic":"orders","from":"2025-10-05T06:00:00Z"}
```

**Response**
```json
{ "status":"started"}
```

**Notes**
- Guarded by admin role; observe quotas.

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
