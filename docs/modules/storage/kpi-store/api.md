# KPI Store – API

## Overview
Public/admin interface for kpi store operations.

**Base URL**  
`https://api.datajetty.com/api/v1/storage/kpi`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Query KPI
**Purpose:** Query KPI series/aggregates  
**Path:** `POST /query`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "kpi":"revenue_mtd","filters":{"region":["IN"]},"window":{"from":"2025-10-01","to":"2025-10-05"} }
```

**Response**
```json
{ "kpi":"revenue_mtd","points":[{"ts":"2025-10-01","value":12345.0}] }
```

**Notes**
- Supports downsampling and confidence intervals.

---

### List KPIs
**Purpose:** Discover available KPIs  
**Path:** `GET /kpis`

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
{ "items":[{"kpi":"revenue_mtd","contract":"v1"}] }
```

**Notes**
- Contracts are versioned.

---

### Get Dimensions
**Purpose:** Fetch dimension values  
**Path:** `GET /dimensions?name=region`

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
{ "items":["IN","US","EU"] }
```

**Notes**
- Supports paging for large dimensions.

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
