# Config & Flags – API

## Overview
Public/admin interface for config & flags operations.

**Base URL**  
`https://api.datajetty.com/api/v1/runtime/flags`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Flag
**Purpose:** Create or update a flag  
**Path:** `POST /flags`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "key":"plan-simulator-enabled","rules":[{"if":"region==\"IN\"","pct":10}] }
```

**Response**
```json
{ "flag_id":"flg_7","status":"active"}
```

**Notes**
- Validates rule expressions.

---

### Evaluate
**Purpose:** Evaluate flags for a subject  
**Path:** `POST /evaluate`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "subject":"user:42","attrs":{"region":"IN"},"keys":["plan-simulator-enabled"] }
```

**Response**
```json
{ "decisions":{"plan-simulator-enabled": true},"meta":{"variant":"A"}}
```

**Notes**
- Edge‑cached; returns decisions and variants.

---

### Create Segment
**Purpose:** Define reusable targeting segment  
**Path:** `POST /segments`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "name":"IN-tenants","expr":"tenant.region==\"IN\"" }
```

**Response**
```json
{ "segment_id":"seg_9","status":"active"}
```

**Notes**
- Used by flag rules.

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
