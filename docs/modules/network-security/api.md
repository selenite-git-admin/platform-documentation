# Network Security – API

## Overview
Public/admin interface for network security operations.

**Base URL**  
`https://api.datajetty.com/api/v1/security/network`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Provision Segment
**Purpose:** Create or update network segment  
**Path:** `POST /segments`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "tenant_id":"t_123","cidr":"10.10.0.0/24","labels":["prod"] }
```

**Response**
```json
{ "segment_id":"seg_7","status":"active" }
```

**Notes**
- Idempotent by (tenant_id,cidr).

---

### Create Private Link
**Purpose:** Establish private connectivity to external service  
**Path:** `POST /private-links`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "tenant_id":"t_123","service":"s3","region":"ap-south-1" }
```

**Response**
```json
{ "link_id":"pl_55","status":"provisioning" }
```

**Notes**
- Asynchronous operation; poll for completion.

---

### Set Egress Policy
**Purpose:** Define egress allow‑list  
**Path:** `POST /egress-policies`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "tenant_id":"t_123","domains":["api.partner.com"],"ports":[443] }
```

**Response**
```json
{ "policy_id":"eg_9","status":"active" }
```

**Notes**
- Policies are enforced at gateways and SGs.

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
