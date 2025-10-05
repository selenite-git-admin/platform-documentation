# Action Engine – API

## Overview
Public interface for action engine operations (tenant/admin-scoped as indicated).

**Base URL**  
`https://api.datajetty.com/api/v1/action/engine`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Rule
**Purpose:** Create or update rule  
**Path:** `POST /rules`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "name":"HighDefectRate","when":"kpi.defect_rate > 2% for 5m","template_id":"tpl_abc" }
```

**Response**
```json
{ "rule_id":"r_123","status":"active" }
```

**Notes**
- Validates references to templates and KPIs.

---

### Test Evaluate
**Purpose:** Dry‑run rules against a sample event  
**Path:** `POST /evaluate`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "event":{"kpi":"defect_rate","value":0.03},"rule_id":"r_123" }
```

**Response**
```json
{ "would_trigger": true, "resolved_template":"tpl_abc" }
```

**Notes**
- Does not create jobs.

---

### Job Status
**Purpose:** Check job progress  
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
{ "job_id":"j_7","state":"completed","attempts":1 }
```

**Notes**
- Includes retry/backoff history.

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
