# Catalog – API

## Overview
Tenant-facing interface for catalog operations. Contract-stable and additive versioning.

**Base URL**  
`https://api.datajetty.com/api/v1/data-consumption/catalog`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens (Access → Authentication). `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### List Resources
**Purpose:** Search/browse catalog  
**Path:** `GET /resources?query=&tag=&owner=`

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
{ "items":[{"id":"kpi:revenue_mtd","title":"Revenue MTD","contract":"v1","freshness_sla":"P1D"}] }
```

**Notes**
- Search facets and pagination supported.

---

### Get Resource
**Purpose:** Full details  
**Path:** `GET /resources/{id}`

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
{ "id":"kpi:revenue_mtd","title":"Revenue MTD","owner":"fin-analytics","examples":[{"curl":"..."}] }
```

**Notes**
- Includes links to lineage evidence.

---

### List Collections
**Purpose:** Persona collections  
**Path:** `GET /collections`

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
{ "items":[{"collection_id":"cfo-insights","items":["kpi:revenue_mtd"]}] }
```

**Notes**
- Read-only.

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
