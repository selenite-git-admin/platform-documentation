# Activation APIs – API

## Overview
Tenant-facing interface for activation apis operations. Contract-stable and additive versioning.

**Base URL**  
`https://api.datajetty.com/api/v1/data-consumption/activation`

**Content Type**  
`application/json`

**Authentication**  
Bearer tokens (Access → Authentication). `Authorization: Bearer <token>`

**Versioning**  
URI‑versioned (`/api/v1/`). Additive changes only.

---

## Endpoints

### Query
**Purpose:** Run query over KPIs/datasets  
**Path:** `POST /query`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "resource":"kpi:revenue_mtd","filters":{"region":["IN"]},"select":["value","confidence"],"limit":100,"cursor":null }
```

**Response**
```json
{ "items":[{"ts":"2025-10-05","value":12345,"confidence":0.98}], "cursor":"eyJwYWdlIjoyfQ==" }
```

**Notes**
- Returns a signed cursor for next page.

---

### GraphQL
**Purpose:** GraphQL endpoint  
**Path:** `POST /graphql`

**Headers**
| Key | Required | Description |
|-----|----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key |

**Request**
```json
{ "query":"query($k:String!){ kpi(key:$k){ points{ ts value } }}", "variables":{"k":"revenue_mtd"} }
```

**Response**
```json
{ "data": { "kpi": { "points":[{"ts":"2025-10-05","value":12345}] } } }
```

**Notes**
- Auth scopes enforced in resolvers.

---

### Discover
**Purpose:** List resources & contracts  
**Path:** `GET /resources`

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
{ "items":[{"id":"kpi:revenue_mtd","contract":"v1"}] }
```

**Notes**
- Search & tags supported.

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
