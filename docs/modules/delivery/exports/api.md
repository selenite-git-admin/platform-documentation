# Exports – API

## Overview
Tenant-facing interface for exports operations. Contract-stable and additive versioning.

**Base URL**  
`https://api.datajetty.com/api/v1/data-consumption/exports`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens (Access → Authentication). `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Export
**Purpose:** Create/export snapshot  
**Path:** `POST /jobs`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dataset":"orders","version":"v24","format":"parquet","target":"s3://tenant/exports/orders"}
```

**Response**
```json
{ "export_id":"ex_1","status":"queued","snapshot_ref":"snap_9"}
```

**Notes**
- Idempotent by (dataset,version,format,target).

---

### Get Export
**Purpose:** Fetch export status  
**Path:** `GET /jobs/{id}`

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
{ "export_id":"ex_1","status":"done","artifacts":[{"uri":"s3://.../orders_v24.parquet"}]}
```

**Notes**
- Includes artifacts and receipts.

---

### List Exports
**Purpose:** List tenant exports  
**Path:** `GET /jobs`

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
{ "items":[{"export_id":"ex_1","status":"done"}]}
```

**Notes**
- Pagination & filtering supported.

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
