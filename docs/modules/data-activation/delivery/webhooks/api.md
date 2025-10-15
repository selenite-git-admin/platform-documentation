# Webhooks – API

## Overview
Tenant-facing interface for webhooks operations. Contract-stable and additive versioning.

**Base URL**  
`https://api.datajetty.com/api/v1/data-consumption/webhooks`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens (Access → Authentication). `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Register Endpoint
**Purpose:** Create/update endpoint  
**Path:** `POST /endpoints`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "url":"https://app/hook","events":["export.done"],"secret":"***"}
```

**Response**
```json
{ "endpoint_id":"ep_7","status":"active"}
```

**Notes**
- Validates ownership via challenge handshake.

---

### List Endpoints
**Purpose:** List tenant endpoints  
**Path:** `GET /endpoints`

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
{ "items":[{"endpoint_id":"ep_7","status":"active"}]}
```

**Notes**
- Pagination supported.

---

### Replay
**Purpose:** Replay from watermark  
**Path:** `POST /replay`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "endpoint_id":"ep_7","from":"2025-10-05T06:00:00Z"}
```

**Response**
```json
{ "status":"started"}
```

**Notes**
- Rate-limited; deliveries signed.

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
