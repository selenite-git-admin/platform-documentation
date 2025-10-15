# Metering – API

## Overview
Public/admin interface for metering operations.

**Base URL**  
`https://api.datajetty.com/api/v1/runtime/metering`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Ingest Delta
**Purpose:** Record usage delta  
**Path:** `POST /deltas`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "tenant_id":"t_123","feature":"csv_export","units":1,"timestamp":"2025-10-05T10:00:00Z"}
```

**Response**
```json
{ "status":"accepted"}
```

**Notes**
- Idempotent by event id if provided.

---

### Get Counter
**Purpose:** Fetch window counter  
**Path:** `GET /counters?tenant=t_123&feature=csv_export&window=day&as_of=2025-10-05`

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
{ "tenant_id":"t_123","feature":"csv_export","window":"day","used":999,"limit":1000 }
```

**Notes**
- Aligns with tenant calendar.

---

### Reconcile
**Purpose:** Run reconciliation job  
**Path:** `POST /reconcile`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "from":"2025-10-04","to":"2025-10-05"}
```

**Response**
```json
{ "job_id":"rec_7","status":"running"}
```

**Notes**
- Produces drift report.

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
