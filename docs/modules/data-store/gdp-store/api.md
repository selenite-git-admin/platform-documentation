# GDP Store – API

## Overview
Public/admin interface for gdp store operations.

**Base URL**  
`https://api.datajetty.com/api/v1/storage/gdp`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Dataset Version
**Purpose:** Create a new GDP version  
**Path:** `POST /datasets/{id}/versions`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "version":"v24","schema_id":"sch_gdp_24","inputs":[{"object_id":"obj_1"}] }
```

**Response**
```json
{ "dataset_id":"ds_sales","version":"v24","status":"building" }
```

**Notes**
- Idempotent by (dataset_id,version).

---

### Publish Dataset
**Purpose:** Promote version to current  
**Path:** `POST /datasets/{id}/publish`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "version":"v24" }
```

**Response**
```json
{ "dataset_id":"ds_sales","current":"v24","prev":"v23" }
```

**Notes**
- Requires all DQ gates green.

---

### Get Lineage
**Purpose:** Fetch lineage graph  
**Path:** `GET /lineage?dataset=ds_sales&version=v24`

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
{ "nodes":[...], "edges":[...] }
```

**Notes**
- Returns graph in JSON.

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
