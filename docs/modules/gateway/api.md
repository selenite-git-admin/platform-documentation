# Gateway – API

## Overview
Public/admin interface for gateway operations.

**Base URL**  
`https://api.datajetty.com/api/v1/security/gateway`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### List Routes
**Purpose:** List configured upstream routes  
**Path:** `GET /routes`

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
{ "items":[{"path":"/api/v1/enforcement/*","upstream":"enforcement-svc"}] }
```

**Notes**
- Admin only; supports pagination.

---

### Update Route
**Purpose:** Create or modify a route  
**Path:** `POST /routes`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "path":"/api/v1/enforcement/*","upstream":"enforcement-svc","retries":2 }
```

**Response**
```json
{ "path":"/api/v1/enforcement/*","status":"active" }
```

**Notes**
- Validates upstream health before activation.

---

### Set WAF Policy
**Purpose:** Attach a WAF ruleset  
**Path:** `POST /waf/policies`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "name":"baseline-2025","mode":"block","rules":["sql_injection","xss"] }
```

**Response**
```json
{ "policy_id":"waf_2025_10","status":"active" }
```

**Notes**
- Supports shadow mode for testing.

---

### Rate Limit
**Purpose:** Configure per‑tenant limits  
**Path:** `POST /ratelimits`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "tenant_id":"t_123","limit_rps":10,"burst":20 }
```

**Response**
```json
{ "tenant_id":"t_123","status":"active" }
```

**Notes**
- Overrides expire automatically unless renewed.

---

### Rotate Certificate
**Purpose:** Rotate TLS certificate  
**Path:** `POST /certs/rotate`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "domain":"api.datajetty.com","strategy":"bluegreen" }
```

**Response**
```json
{ "status":"rotating","new_cert_id":"crt_2025_10" }
```

**Notes**
- Blue/green with automatic rollback on failures.

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
