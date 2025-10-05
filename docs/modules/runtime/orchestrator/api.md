# Orchestrator – API

## Overview
Public/admin interface for orchestrator operations.

**Base URL**  
`https://api.datajetty.com/api/v1/runtime/orchestrator`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Submit DAG
**Purpose:** Create or update a DAG  
**Path:** `POST /dags`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dag_id":"sales_gdp","schedule":"0 2 * * *","owner":"team-data"}
```

**Response**
```json
{ "dag_id":"sales_gdp","status":"active"}
```

**Notes**
- Validates acyclic graph and schedule.

---

### Trigger Run
**Purpose:** Trigger a manual or backfill run  
**Path:** `POST /runs`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "dag_id":"sales_gdp","run_type":"backfill","from":"2025-10-01","to":"2025-10-04"}
```

**Response**
```json
{ "run_id":"run_9","state":"queued"}
```

**Notes**
- Idempotent by (dag_id, window).

---

### Get Run
**Purpose:** Fetch run status  
**Path:** `GET /runs/{id}`

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
{ "run_id":"run_9","state":"running","tasks":{"extract":"done","transform":"running"}}
```

**Notes**
- Includes SLA deadline and attempts.

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
