# Subscription Enforcement – Data Model

## Scope
Defines conceptual entities, fields, keys, and relationships used by Subscription Enforcement to evaluate entitlements, apply limits, and emit evidence. This is a logical model; physical schemas may vary by deployment.

## Entities

### Plan
Represents a versioned plan definition with features, limits, grace, and overage policy.

| Field | Type | Req | Constraints | Notes |
|------|------|-----|-------------|------|
| plan_id | string | ✓ | PK; immutable | `plan_<edition>_<yyyymm>` |
| edition | string | ✓ | enum: free, pro, enterprise | |
| version | string | ✓ | semver or date tag | Governs compatibility |
| features | array\<string> | ✓ | | Feature keys |
| limits | array\<Limit> | ✓ | | Per-feature quotas |
| grace_policy | object |  | | `{window, behavior}` |
| overage_policy | object |  | | pricing, caps |
| valid_from | datetime | ✓ | | |
| valid_to | datetime |  | | null = open-ended |

**Limit (inline object)**  
`{ "feature": "csv_export", "unit": "calls/day", "soft": 1000, "hard": 1200 }`

---

### Entitlement
Effective feature access for a tenant (plan + overrides).

| Field | Type | Req | Constraints | Notes |
|------|------|-----|-------------|------|
| tenant_id | string | ✓ | PK1 | |
| feature | string | ✓ | PK2 | |
| enabled | boolean | ✓ | | |
| constraints | object |  | | region/time/data‑class |
| plan_ref | string | ✓ | FK → Plan.plan_id | |
| source | string | ✓ | enum: plan, override, promo | Provenance |
| updated_at | datetime | ✓ | | |

---

### Override
Time‑boxed changes to entitlements or limits.

| Field | Type | Req | Constraints | Notes |
|------|------|-----|-------------|------|
| override_id | string | ✓ | PK | |
| tenant_id | string | ✓ | | |
| scope | string | ✓ | enum: feature, edition | |
| feature | string |  | required if scope=feature | |
| patch | object | ✓ | | JSON‑patch style |
| status | string | ✓ | enum: draft, active, expired, revoked | |
| starts_at | datetime |  | | |
| ends_at | datetime |  | | |
| approver | string |  | | user id |
| reason | string |  | | audit text |

_State transitions_: draft → active → expired | revoked

---

### UsageAggregate
Rolling counters for enforcement windows.

| Field | Type | Req | Constraints | Notes |
|------|------|-----|-------------|------|
| tenant_id | string | ✓ | PK1 | |
| feature | string | ✓ | PK2 | |
| window_start | datetime | ✓ | PK3 | Aligned to window |
| window_end | datetime | ✓ | | |
| used_units | integer | ✓ | `>=0` | |
| last_updated | datetime | ✓ | | |

_Index_: `(tenant_id, feature, window_start)`

---

### EnforcementEvent
Evidence of a decision for audit and support.

| Field | Type | Req | Constraints | Notes |
|------|------|-----|-------------|------|
| evidence_id | string | ✓ | PK | Hash chain capable |
| timestamp | datetime | ✓ | | UTC |
| tenant_id | string | ✓ | | |
| feature | string | ✓ | | |
| decision | string | ✓ | enum: permit, throttle, deny, grace | |
| reason | string | ✓ | | machine‑readable |
| quota_snapshot | object |  | | `{limit, used, window}` |
| policy_ids | array\<string> |  | | plan, promo, override ids |
| request_hash | string |  | | idempotency key |

_Retention_: 90 days (immutable in Evidence Ledger).

---

## Relationships
- Plan 1—* Entitlement (via `plan_ref`).  
- Tenant 1—* Entitlement / Override / UsageAggregate / EnforcementEvent.  
- Feature is a controlled vocabulary across Plan, Entitlement, UsageAggregate, EnforcementEvent.

## Keys and Indexes
- Entitlement PK `(tenant_id, feature)`; read‑heavy.  
- UsageAggregate PK `(tenant_id, feature, window_start)`; write‑heavy with upserts.  
- EnforcementEvent PK `evidence_id` with time‑based partition.

## Data Quality Rules
- `used_units` cannot decrease within a window except during reconciliation.  
- `plan_ref` must be valid for `timestamp` range.  
- Override with `status=active` must have `starts_at <= now < ends_at`.

## Retention
- Decision caches: < 24 h.  
- EnforcementEvent: 90 days (Ledger).  
- UsageAggregate: window duration + 30 days for reconciliation.

## Notes
- No raw PII is stored in these entities.  
- Region and residency are inherited from the tenant profile.
