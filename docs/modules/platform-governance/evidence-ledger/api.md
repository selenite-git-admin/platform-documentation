# Evidence Ledger – API

## Overview
Public interface for evidence ledger operations.

**Base URL**  
`https://api.datajetty.com/api/v1/trust/evidence`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Append Evidence
**Purpose:** Record immutable decision/event  
**Path:** `POST /append`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "tenant_id":"t_123","kind":"decision","payload":{"decision":"permit","reason":"within_limit"} }
```

**Response**
```json
{ "evidence_id":"ev_7f2a","hash":"abc123","timestamp":"2025-10-05T10:00:00Z" }
```

**Notes**
- Payload is hashed and chained; returns identifiers for correlation.

---

### Verify Chain
**Purpose:** Verify integrity of a range  
**Path:** `POST /verify`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "from":"2025-10-01T00:00:00Z","to":"2025-10-05T00:00:00Z" }
```

**Response**
```json
{ "valid": true, "proof":{"root":"..."} }
```

**Notes**
- Returns valid=false on any mismatch.

---

### Export Range
**Purpose:** Export evidence for auditors  
**Path:** `POST /export`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "from":"2025-10-01","to":"2025-10-05","format":"ndjson" }
```

**Response**
```json
{ "export_id":"ex_123","location":"s3://audit/exports/ex_123" }
```

**Notes**
- Long‑running; poll export status if needed.

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
