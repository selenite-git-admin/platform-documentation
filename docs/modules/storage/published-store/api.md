# Published Store – API

## Overview
Public/admin interface for published store operations.

**Base URL**  
`https://api.datajetty.com/api/v1/storage/published`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Snapshot
**Purpose:** Create dataset snapshot for export  
**Path:** `POST /snapshots`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dataset":"orders","version":"v24","format":"parquet" }
```

**Response**
```json
{ "snapshot_id":"snap_9","status":"building" }
```

**Notes**
- Idempotent by (dataset,version,format).

---

### Export Snapshot
**Purpose:** Export snapshot to target  
**Path:** `POST /exports`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "snapshot_id":"snap_9","target":"s3://tenant/export/orders","notify_webhook":"https://..." }
```

**Response**
```json
{ "export_id":"ex_1","status":"queued" }
```

**Notes**
- Delivery retries with backoff; signed webhooks.

---

### List Datasets
**Purpose:** Discover published datasets  
**Path:** `GET /datasets`

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
{ "items":[{"dataset":"orders","contract":"v3"}] }
```

**Notes**
- Supports pagination and filtering.

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
