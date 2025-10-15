# Secrets – API

## Overview
Public interface for secrets operations.

**Base URL**  
`https://api.datajetty.com/api/v1/trust/secrets`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Write Secret
**Purpose:** Create or update a secret version  
**Path:** `POST /secrets/{path}`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "value_b64":"...", "metadata":{"owner":"svc-data","rotation":"90d"} }
```

**Response**
```json
{ "version": 7, "created_at": "2025-10-05T10:00:00Z" }
```

**Notes**
- Value is envelope‑encrypted; metadata stored in index.

---

### Read Secret
**Purpose:** Read latest or specific version  
**Path:** `GET /secrets/{path}?version=n`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ }
```

**Response**
```json
{ "value_b64":"...", "version": 7, "lease_ttl_s": 3600 }
```

**Notes**
- Requires read scope for the path; may return leased credentials.

---

### Issue Lease
**Purpose:** Generate short‑lived credentials  
**Path:** `POST /leases`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "role":"etl-reader", "ttl_s":3600 }
```

**Response**
```json
{ "access_key":"...", "secret_key":"...", "expires_at":"2025-10-05T11:00:00Z" }
```

**Notes**
- Backed by provider‑specific plugins (e.g., cloud IAM).

---

### Rotate Secret
**Purpose:** Trigger rotation hook  
**Path:** `POST /admin/rotate/{path}`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "strategy":"immediate" }
```

**Response**
```json
{ "path":"db/password", "new_version": 8 }
```

**Notes**
- Admin only; emits evidence with actor and reason.

---

## Error Model
| HTTP | Title | Example |
|------|-------|---------|
| 400 | Bad Request | {"error":"invalid_request"} |
| 401 | Unauthorized | {"error":"unauthorized"} |
| 403 | Forbidden | {"error":"forbidden"} |
| 404 | Not Found | {"error":"not_found"} |
| 429 | Too Many Requests | {"error":"rate_limited"} |
| 500 | Internal Error | {"error":"internal_error"} |
| 503 | Service Unavailable | {"error":"dependency_down"} |

## Rate Limits
Documented per endpoint; defaults: 10 rps per tenant.

## References
- [Data Model](data-model.md) · [Runbook](runbook.md) · [Security](security.md)
