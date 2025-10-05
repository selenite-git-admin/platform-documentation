# Subscription Enforcement – API

## Overview
The Subscription Enforcement API provides tenant‑facing endpoints for entitlement validation, plan retrieval, and simulation of plan upgrades or usage scenarios.  
It is the public contract for tenants and admins to evaluate actions and ensure compliance with plan limits in real time.

**Base URL**  
`https://api.datajetty.com/api/v1/enforcement`

**Content Type**  
`application/json`

**Authentication**  
All endpoints require a valid bearer token issued by the Access domain.  
Include the following header in each request:
```
Authorization: Bearer <access_token>
```

**Versioning**  
Versioned via URI path (`/api/v1/`) and changelog managed through `/api/v1/meta/versions`.  
Backward‑compatible changes only; new fields are additive.

---

## Endpoints

### 1. Evaluate

**Purpose:** Validate whether a tenant action is allowed under its active plan and entitlements.  
**Path:** `POST /evaluate`

**Headers**
| Key | Required | Description |
|-----|-----------|-------------|
| Authorization | Yes | Bearer token |
| Content‑Type | Yes | application/json |
| X‑Request‑Id | Optional | Idempotency key (auto‑generated if omitted) |

**Request Parameters**
| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| tenant_id | string | Yes | Unique tenant identifier |
| subject | string | Yes | User or service identifier |
| action | string | Yes | Action to evaluate (e.g., `exports.create`) |
| feature | string | Yes | Feature key associated with the action |
| usage_hint | object | No | Estimated units and window |
| context | object | No | Region, plan version, or tags |

**Request Example**
```json
{
  "tenant_id": "t_123",
  "subject": "user:42",
  "action": "exports.create",
  "feature": "csv_export",
  "usage_hint": {"units": 1, "window": "day"},
  "context": {"region": "IN", "plan_version": "2025-09-01"}
}
```

**Response Example**
```json
{
  "decision": "permit",
  "reason": "within_limit",
  "quota": {"limit": 1000, "used": 999, "window": "day"},
  "grace": false,
  "evidence_id": "ev_ae91a",
  "policy_ids": ["plan:pro@2025-09-01"],
  "timestamp": "2025-10-05T10:00:00Z"
}
```

**Response Fields**
| Field | Type | Description |
|--------|------|-------------|
| decision | string | permit, throttle, deny, or grace |
| reason | string | Text reason code for decision |
| quota | object | Snapshot of current limit and usage |
| grace | boolean | True if grace policy applied |
| evidence_id | string | Reference to Evidence Ledger record |
| policy_ids | array | Active plan and promotion identifiers |
| timestamp | datetime | UTC timestamp of decision |

---

### 2. Get Plan

**Purpose:** Retrieve the effective plan definition and limits for the tenant.  
**Path:** `GET /plan`

**Query Parameters**
| Name | Type | Required | Description |
|-------|------|-----------|-------------|
| edition | string | No | Specific plan edition (defaults to active) |
| as_of | string | No | ISO date to retrieve plan snapshot |

**Example Response**
```json
{
  "plan_id": "plan_pro_2025",
  "edition": "pro",
  "features": ["csv_export", "dashboard"],
  "limits": [
    {"feature": "csv_export", "unit": "calls/day", "soft": 1000, "hard": 1200}
  ],
  "grace_policy": {"window": "3d", "behavior": "allow"},
  "overage_policy": {"pricing": "₹2 per extra call", "limit": 2000}
}
```

**Notes**
- Supports ETag caching to minimize load.  
- Plan versions include validity ranges for audit and rollback.  
- Optional pagination if the plan has >100 features.

---

### 3. Simulate

**Purpose:** Evaluate a hypothetical plan or usage level without committing changes.  
**Path:** `POST /simulate`

**Request**
```json
{
  "tenant_id": "t_123",
  "target_plan": "enterprise",
  "feature": "exports.csv",
  "hypothetical_usage": {"units": 1100, "window": "day"}
}
```

**Response**
```json
{
  "decision": "permit",
  "plan_diff": {"old_limit": 1000, "new_limit": 2000},
  "notes": "Upgrade removes throttling risk.",
  "effective_date": "2025-10-06"
}
```

**Behavior**
- Simulation never updates usage or evidence.  
- Admins may run batch simulations via bulk endpoints.  
- Supports comparison across multiple editions.  

---

## Shared Objects

### Decision Object
```json
{
  "decision": "permit",
  "reason": "within_limit",
  "quota": {"limit": 1000, "used": 500, "window": "day"},
  "grace": false,
  "evidence_id": "ev_7f2a",
  "policy_ids": ["plan:pro"],
  "timestamp": "2025-10-05T09:40:00Z"
}
```

### Quota Object
| Field  | Type    | Description                           |
|--------|---------|---------------------------------------|
| limit  | integer | Maximum allowed units for the window  |
| used   | integer | Current usage count                   |
| window | string  | Measurement period (day, month, etc.) |

### Evidence Object
| Field       | Type     | Description                |
|-------------|----------|----------------------------|
| evidence_id | string   | Identifier for audit trail |
| tenant_id   | string   | Tenant reference           |
| feature     | string   | Evaluated feature          |
| decision    | string   | Outcome                    |
| timestamp   | datetime | UTC time of record         |

---

## Error Model

| HTTP Code | Title               | Description                     | Example                                                         |
|-----------|---------------------|---------------------------------|-----------------------------------------------------------------|
| 200       | OK                  | Valid decision response         | —                                                               |
| 400       | Bad Request         | Invalid or missing field        | `{ "error": "invalid_request", "detail": "missing tenant_id" }` |
| 401       | Unauthorized        | Invalid or missing token        | `{ "error": "unauthorized" }`                                   |
| 403       | Forbidden           | Limit or entitlement violation  | `{ "error": "denied", "reason": "hard_limit_exceeded" }`        |
| 429       | Too Many Requests   | Soft limit exceeded             | `{ "error": "throttled", "retry_after_ms": 2000 }`              |
| 500       | Internal Error      | Unexpected evaluation error     | `{ "error": "internal_error" }`                                 |
| 503       | Service Unavailable | Dependency or cache unavailable | `{ "error": "dependency_down" }`                                |

---

## Rate Limits
- Evaluate: 10 requests / sec per tenant.  
- Get Plan: 1 request / sec per tenant.  
- Simulate: 2 requests / sec per tenant.  
Bursting within 1 second window is tolerated up to 2×.

---

## Versioning and Stability
- Current version: `v1` (stable).  
- Changes tracked in `/meta/changelog`.  
- Deprecation warnings returned via `X‑API‑Warning` header 60 days before removal.

---

## References
- [Data Model](data-model.md)  
- [Observability](observability.md)  
- [Runbook](runbook.md)  
- [Security](security.md)
