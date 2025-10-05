# Dashboards – API

## Overview
Tenant-facing interface for dashboards operations. Contract-stable and additive versioning.

**Base URL**  
`https://api.datajetty.com/api/v1/data-consumption/dashboards`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens (Access → Authentication). `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Render
**Purpose:** Render dashboard  
**Path:** `POST /render`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dashboard_id":"ops_overview","filters":{"region":"IN"} }
```

**Response**
```json
{ "html":"<div>...</div>","ttl_s":300 }
```

**Notes**
- Server-rendered HTML with hydration data.

---

### Share
**Purpose:** Create expiring share link  
**Path:** `POST /share`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dashboard_id":"ops_overview","expires_in_s":3600 }
```

**Response**
```json
{ "url":"https://.../s/abc","expires_at":"2025-10-05T12:00:00Z" }
```

**Notes**
- Links are signed and scoped.

---

### Save Definition
**Purpose:** Create/update dashboard  
**Path:** `POST /definitions`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dashboard_id":"ops_overview","layout":{...},"datasources":[...]}
```

**Response**
```json
{ "dashboard_id":"ops_overview","status":"active"}
```

**Notes**
- Definitions are versioned; publishing freezes content.

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
