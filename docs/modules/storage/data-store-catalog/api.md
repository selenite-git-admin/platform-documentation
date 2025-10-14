# Data Store Catalog API

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Overview
Developer-facing reference for Catalog APIs. Catalog exposes dataset discovery and migration endpoints over standard HTTP. All datasets live inside governed PostgreSQL stores. There are no warehouse or external vendor dependencies.

## Auth
- All requests require JWT authentication.
- Scopes: `catalog.read`, `catalog.write` (internal only).
- Responses support `ETag` and `If-None-Match`.

## Errors
Common envelope
```json
{ "code":"invalid_request|not_found|forbidden|conflict|internal_error",
  "message":"detail",
  "correlation_id":"uuid-v7",
  "details":{"field":"reason"}
}
```

## Read Endpoints

### GET /storage/v1/catalog/datasets/{id}
Return a dataset descriptor.

**Response 200**
```json
{
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "layer": "kpi",
  "physical": [
    {"type": "postgres_table", "database": "platform_store", "schema": "kpi", "name": "cash_conversion_cycle_v2"}
  ],
  "schema_uri": "s3://schemas/kpi/cash_conversion_cycle_v2/1.4.0/json",
  "classification": "internal",
  "retention": {"policy": "90d_raw_365d_agg"},
  "owner": {"module": "kpi-service", "email": "kpi-owners@example.com"},
  "access_class": "read_internal",
  "tags": ["finance", "executive"],
  "compatibility": {"mode": "backward", "since": "1.3.0"}
}
```

**Codes** 200, 304, 403, 404

---

### GET /storage/v1/catalog/datasets
List datasets with filters and pagination.

**Query params**
| Name | Type | Notes |
|------|------|-------|
| `layer` | enum(raw,gdp,kpi,published) | optional |
| `tenant_id` | string | optional, RLS applies |
| `tag` | string | repeatable |
| `q` | string | full text search |
| `cursor` | string | pagination token |
| `limit` | int | default 50, max 500 |

**Response 200**
```json
{
  "items": [
    {"dataset_id":"gdp.sales_invoice_v3","layer":"gdp","tags":["finance"]}
  ],
  "count": 1,
  "cursor": "eyJvZmZzZXQiOjEwfQ=="
}
```

**Codes** 200, 304, 400, 403

---

### GET /storage/v1/catalog/datasets/{id}:describe
Return descriptor with optional DRR freshness in one call.

**Query params**
| Name | Type | Notes |
|------|------|-------|
| `include` | enum(freshness) | optional |

**Response 200**
```json
{
  "dataset": {
    "dataset_id": "kpi.cash_conversion_cycle_v2",
    "layer": "kpi",
    "physical": [{"type":"postgres_table","database":"platform_store","schema":"kpi","name":"cash_conversion_cycle_v2"}],
    "schema_uri": "s3://schemas/kpi/cash_conversion_cycle_v2/1.4.0/json"
  },
  "freshness": {
    "status":"fresh",
    "last_success_at":"2025-10-12T06:02:14Z",
    "freshness_lag_sec": 421,
    "freshness_slo_sec": 10800
  }
}
```

**Codes** 200, 304, 400, 403, 404

---

### GET /storage/v1/catalog/datasets/{id}/schema
Return schema definition reference and version.

**Response 200**
```json
{
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "schema_uri": "s3://schemas/kpi/cash_conversion_cycle_v2/1.4.0/json",
  "schema_type": "json",
  "version": "1.4.0"
}
```

**Codes** 200, 304, 403, 404

---

### GET /storage/v1/catalog/datasets/{id}/lineage
Return upstream and downstream relationships.

**Response 200**
```json
{
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "upstream": ["gdp.invoice_enriched_v7"],
  "downstream": ["published.executive_dashboard_v3"]
}
```

**Codes** 200, 304, 403, 404

## Write Endpoints (internal)

### POST /storage-internal/v1/catalog/datasets/{id}
Create or update a dataset descriptor. Requires owner role.

**Headers**
- Authorization: Bearer <m2m>
- Idempotency-Key: uuid-v7
- Content-Type: application/json

**Request**
```json
{
  "layer": "kpi",
  "physical": [{"type": "postgres_table", "database": "platform_store", "schema": "kpi", "name": "cash_conversion_cycle_v2"}],
  "schema_uri": "s3://schemas/kpi/cash_conversion_cycle_v2/1.4.0/json",
  "classification": "internal",
  "retention": {"policy":"90d_raw_365d_agg"},
  "owner": {"module":"kpi-service","email":"kpi-owners@example.com"},
  "access_class": "read_internal",
  "tags": ["finance","executive"],
  "compatibility": {"mode":"backward","since":"1.3.0"}
}
```

**Response 200**
```json
{ "updated": true, "dataset_id": "kpi.cash_conversion_cycle_v2", "version": "1.4.0" }
```

**Codes** 200, 400, 401, 403, 409, 422

---

### POST /storage-internal/v1/catalog/migrations
Submit migration steps to update physical coordinates or metadata.

**Request**
```json
{
  "dataset_id": "gdp.sales_invoice_v3",
  "steps": [
    {"op":"add_location","value":{"type":"postgres_table","database":"platform_store","schema":"gdp","name":"sales_invoice_v3"}},
    {"op":"set_schema","value":{"schema_uri":"s3://schemas/gdp/sales_invoice_v3/2.0.0/json","compatibility":{"mode":"backward","since":"1.5.0"}}}
  ],
  "change_reason": "data structure migration"
}
```

**Response 202**
```json
{ "accepted": true, "migration_id": "mig_01HC...", "dataset_id": "gdp.sales_invoice_v3" }
```

**Codes** 202, 400, 401, 403, 409, 422

---

### PATCH /storage-internal/v1/catalog/datasets/{id}/deprecate
Mark a dataset as deprecated. Readers receive a deprecation hint.

**Request**
```json
{ "replacement": "kpi.cash_conversion_cycle_v3", "reason": "schema break" }
```

**Response 200**
```json
{ "deprecated": true, "dataset_id": "kpi.cash_conversion_cycle_v2" }
```

**Codes** 200, 400, 401, 403, 404

## Pagination
- Use `cursor` for opaque pagination.
- Responses include `cursor` when more results exist.
- `limit` default 50, max 500.

## Caching
- `ETag` returned on all GETs.
- Use `If-None-Match` for cache validation.
- Recommended TTL 60 seconds for list endpoints.

## Rate Limits
- Read 2000 RPS per region default, burst 5000.
- Write 200 RPS per region default, burst 500.

## Contracts
- `dataset_id` is a stable logical identifier.
- Physical locations are immutable without a migration.
- Breaking schema changes require new major version.
- Only PostgreSQL stores are supported. No warehouse or vendor engines.