# Action Catalog – API

## Overview
Public interface for action catalog operations (tenant/admin-scoped as indicated).

**Base URL**  
`https://api.datajetty.com/api/v1/action/catalog`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Create Template
**Purpose:** Create a draft template  
**Path:** `POST /templates`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "name":"incident_pager","kind":"notification","body":"...", "schema_id":"sch_123" }
```

**Response**
```json
{ "template_id":"tpl_abc","version":1,"status":"draft" }
```

**Notes**
- Drafts are mutable; publishing freezes content.

---

### Publish Template
**Purpose:** Publish a template version  
**Path:** `POST /templates/{id}/publish`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "version":1, "approver":"user:ops1" }
```

**Response**
```json
{ "template_id":"tpl_abc","version":1,"status":"published","signature":"sig_..." }
```

**Notes**
- Requires approval; emits evidence with approver and signature.

---

### Search Templates
**Purpose:** Find templates by fields  
**Path:** `GET /templates?query=incident`

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
{ "items":[{"template_id":"tpl_abc","name":"incident_pager","version":1}] }
```

**Notes**
- Supports pagination and sorting.

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
