# Data Model

## Entities

### `subject`
| field | type | notes |
|---|---|---|
| id | ulid | primary key |
| tenant_id | ulid | isolation |
| name | string | e.g., `gdp.orders` |
| kind | enum | `raw`,`gdp`,`kpi` |
| owner | string | team |
| tags | json | strings |
| created_at | timestamp | |
| updated_at | timestamp | |

### `schema_version`
| field | type | notes |
|---|---|---|
| id | ulid | |
| tenant_id | ulid | |
| subject_id | ulid | fk to subject |
| version | int | monotonic |
| schema | json | canonical JSON Schema |
| compatibility | enum | `additive`,`backward` |
| aliases | json | e.g., `["customer_id","cust_id"]` |
| checksum | string | sha256 |
| created_at | timestamp | |

### `deprecation`
| field | type | notes |
|---|---|---|
| id | ulid | |
| subject_id | ulid | |
| field | string | JSONPath |
| sunset_after_days | int | default 180 |
| note | string | |
| created_at | timestamp | |

### `receipt`
| field | type | notes |
|---|---|---|
| evidence_id | ulid | |
| subject | string | |
| version | int | nullable for non-version ops |
| actor | string | service/user |
| action | enum | `create_version`,`deprecate`,`alias_update` |
| diff | json | structural diff |
| adr | uri | design record |
| created_at | timestamp | |


# Compatibility & Field Operations

## Field-level operations
| Operation | Raw | GDP | KPI | Notes |
|---|---|---|---|---|
| Add optional field | ✅ additive | ✅ additive | ✅ additive | default allowed |
| Add required field | ⚠️ blocked | ❌ breaking | ❌ breaking | use deprecation + major subject |
| Rename field (alias) | ✅ via alias | ✅ via alias | ✅ via alias | keep alias ≥ 180 days |
| Type widen (int→number) | ✅ additive | ✅ additive | ✅ additive | narrowing is breaking |
| Type narrow (number→int) | ❌ breaking | ❌ breaking | ❌ breaking | requires new subject |
| Remove field | ❌ breaking | ❌ breaking | ❌ breaking | deprecate + sunset then remove |
| Enum add value | ✅ additive | ✅ additive | ✅ additive | |
| Enum remove value | ❌ breaking | ❌ breaking | ❌ breaking | |

## Subject-level
- Breaking proposals require **new subject** (e.g., `gdp.orders.v2`) with migration plan and parallel publish window.
- Minimum parallel window: **90 days**; KPIs recommended **2 full cycles**.


# Validation Pipeline

1. **Schema shape check** — JSON Schema draft 2020-12 canonicalization.
2. **Ruleset check** — additive/backward constraints.
3. **Alias map validation** — ensures lookups for renamed fields.
4. **PII annotations** — surface masking obligations to Governance.
5. **Impact analysis** — compute downstream consumers (Delivery endpoints, dashboards, actions).
6. **Receipt & notify** — emit evidence, webhook to Catalog and Delivery for cache invalidation.

**Webhook event (create_version)**
```json
{
  "event":"schema.create_version",
  "subject":"gdp.orders",
  "version":24,
  "evidence_id":"ev_01J...",
  "produced_at":"2025-10-05T00:00:00Z"
}
```
