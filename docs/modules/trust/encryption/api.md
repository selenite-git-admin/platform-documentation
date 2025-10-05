# Encryption – API

## Overview
Public interface for encryption operations.

**Base URL**  
`https://api.datajetty.com/api/v1/trust/encryption`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens issued by Access. Include: `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Encrypt
**Purpose:** Encrypt small payloads with envelope scheme  
**Path:** `POST /encrypt`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "plaintext_b64":"...", "aad":"tenant:t_123", "key_alias":"alias/app-default" }
```

**Response**
```json
{ "ciphertext_b64":"...", "key_ref":"kr_123", "alg":"AES-GCM", "iv_b64":"..." }
```

**Notes**
- For large objects, use storage‑level encryption and store key_ref as metadata.

---

### Decrypt
**Purpose:** Decrypt ciphertext using key_ref  
**Path:** `POST /decrypt`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "ciphertext_b64":"...", "key_ref":"kr_123", "aad":"tenant:t_123" }
```

**Response**
```json
{ "plaintext_b64":"..." }
```

**Notes**
- AAD must match original; otherwise decryption fails.

---

### Sign
**Purpose:** Generate detached signature  
**Path:** `POST /sign`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "message_b64":"...", "key_alias":"alias/signing-2025", "alg":"RSASSA-PSS" }
```

**Response**
```json
{ "signature_b64":"...", "kid":"kid_2025_10" }
```

**Notes**
- Use Verify to check signatures; kid selects public key.

---

### Verify
**Purpose:** Verify signature  
**Path:** `POST /verify`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "message_b64":"...", "signature_b64":"...", "kid":"kid_2025_10" }
```

**Response**
```json
{ "valid": true }
```

**Notes**
- Returns valid=false if signature mismatch or kid unknown.

---

### Rotate Key
**Purpose:** Rotate key behind alias  
**Path:** `POST /admin/rotate`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "key_alias":"alias/app-default", "strategy":"new-version" }
```

**Response**
```json
{ "key_alias":"alias/app-default", "active_kid":"kid_2025_11" }
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
