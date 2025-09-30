# Metric Serving APIs

## Purpose
Provide consistent APIs for applications and BI tools.
Support pagination, filters, time windows, and security.

## Endpoints
- GET /metrics
- GET /metrics/{metric_id}
- GET /metrics/{metric_id}/series
- GET /catalog/search

## Pagination
Use limit and cursor for pagination.

## Filters
Support dimension filters and time windows.
Support currency and calendar options when relevant.

## Security
Enforce row level scoping where needed.
Use scoped tokens with least privilege.

## Legacy content
The following section is imported from legacy v1 API specifications.

# Kpi Api Specifications
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Specify APIs exposed by the KPI System and their contracts.  
- Scope: Includes endpoints, payloads, error semantics, and versioning. Excludes infra deployment.  
- Target Readers: Backend engineers, integrators.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI System - API Specifications

This document defines the external API surface of the KPI System.  
All endpoints are tenant-scoped, versioned, and policy-enforced.

## 0. Conventions

**Base URL (per environment)**  
- `https://api.cxofacts.com/{env}/kpi/v1` (e.g., `prod`, `stg`, `dev`)

**Auth & Tenant Context**  
- `Authorization: Bearer <OIDC/JWT>` (Cognito/OIDC)  
- `X-Tenant-Id: <tenant_id>` (required)  
- `X-Idempotency-Key: <uuid>` (for mutating ops; optional but recommended)

**Headers**  
- `Content-Type: application/json`  
- `Accept: application/json`

**Pagination**  
- Cursor-based: `?limit=50&cursor=<token>`  
- Response includes: `{ "items": [...], "next_cursor": "..." }`

**Errors**  
- RFC7807-ish:  
```json
{
  "error": "VALIDATION_FAIL_PRE",
  "message": "Pre-validation failed: source completeness < 98%",
  "detail": {
    "kpi_id": "CFO-AR-DSO",
    "run_id": "run_01HZZ...",
    "rule_id": "src_completeness_ge_98"
  },
  "trace_id": "req_01HAA..."
}
```
Common error codes: `UNAUTHENTICATED`, `UNAUTHORIZED`, `POLICY_DENY`, `VALIDATION_FAIL_PRE`, `VALIDATION_FAIL_POST`, `MISSING_GDP`, `SLA_BREACH`, `NOT_FOUND`, `CONFLICT`, `RATE_LIMIT`, `INTERNAL`.

**Versioning**  
- URI version (`/v1`) + KPI contract_version in responses.  
- Backward-compatible changes add fields; breaking changes bump `/vN`.

## 1. KPI Call API

### 1.1 Execute a KPI (stateless)
`POST /calls/execute`

**Request**
```json
{
  "kpi_id": "CFO-AR-DSO",
  "time": { "grain": "month", "range": { "start": "2024-01", "end": "2024-12" } },
  "filters": { "legal_entity": ["LE-APAC-01","LE-EMEA-02"], "product_line": ["Widgets"] },
  "extensions": {
    "time": ["YoY","MoM","rolling_3m"],
    "entity": ["currency=USD"],
    "benchmark": ["budget","forecast"],
    "scenario": [],
    "analytical": ["percentile_p50","zscore"]
  },
  "scd_view": "as_reported", 
  "options": { "include_lineage": true, "format": "json" }
}
```

**Response**
```json
{
  "kpi_id": "CFO-AR-DSO",
  "contract_version": "1.2.0",
  "policy_version": "2025-08-01",
  "run_id": "run_01J12...",
  "time": { "grain": "month", "range": { "start": "2024-01", "end": "2024-12" } },
  "data": [
    { "month":"2024-01", "entity":"LE-APAC-01", "value": 41.3, "YoY": -1.2, "MoM": 0.6 },
    { "month":"2024-02", "entity":"LE-APAC-01", "value": 42.1, "YoY": -0.8, "MoM": 0.8 }
  ],
  "applied_extensions": ["YoY","MoM","rolling_3m","currency=USD","budget","forecast","percentile_p50","zscore"],
  "applied_masking": ["suppress_small_segments"],
  "scd_view": "as_reported",
  "lineage": {
    "sources": [
      {"type":"gdp", "table":"gdp_ar_invoices", "version":"2025.08.01"},
      {"type":"kpi", "kpi_id":"CFO-AR-Revenue", "contract_version":"2.0.0"}
    ],
    "dag_url": "https://app.cxofacts.com/tenants/acme/lineage/run_01J12..."
  },
  "meta": {
    "sla_state": "pass",
    "generated_at": "2025-08-23T10:12:03Z",
    "trace_id": "req_01JA..."
  }
}
```

### 1.2 Preview SQL (debug)
`POST /calls/preview-sql`  
- Same payload as `/calls/execute`, returns generated SQL with redactions.  
- Useful for troubleshooting; requires `kpi:Inspect` permission.

## 2. Admin APIs (Control Plane)

### 2.1 List KPIs
`GET /admin/kpis?status=Active&pack=CFO&limit=50&cursor=...`

### 2.2 Create/Update KPI Definition (artifact)
`PUT /admin/kpis/{kpi_id}`  
Body = KPI contract artifact (YAML/JSON).

### 2.3 Publish a Version
`POST /admin/kpis/{kpi_id}/versions/{ver}/publish`

### 2.4 Pause / Resume
`POST /admin/kpis/{kpi_id}/versions/{ver}/pause`  
`POST /admin/kpis/{kpi_id}/versions/{ver}/resume`  
- Optional scope in body: `{ "entity": ["LE-APAC-01"], "time": {"start":"2025-01","end":"2025-03"} }`

### 2.5 Rollback
`POST /admin/kpis/{kpi_id}/versions/{ver}/rollback`

### 2.6 Schedule & SLA
`POST /admin/kpis/{kpi_id}/versions/{ver}/schedule`  
`POST /admin/kpis/{kpi_id}/versions/{ver}/sla`

### 2.7 Validation Rules
`POST /admin/kpis/{kpi_id}/versions/{ver}/validation/pre`  
`POST /admin/kpis/{kpi_id}/versions/{ver}/validation/post`

### 2.8 Change Requests
`POST   /admin/change-requests` (submit)  
`GET    /admin/change-requests?status=Pending` (list)  
`POST   /admin/change-requests/{cr_id}/decision` (approve/reject)

**Change Request Body (example)**
```json
{
  "kpi_id": "CFO-AR-DSO",
  "proposed_change": "update_sourcing",
  "diff": { "table": "gdp_ar_invoices_v2" },
  "criticality": "high",
  "justification": "new ERP rollout",
  "approvers": ["uid:tech_owner","uid:business_owner"]
}
```

## 3. Logging & Monitoring APIs

### 3.1 List Runs
`GET /logs/runs?kpi_id=CFO-AR-DSO&since=2025-07-01&limit=100`

**Response**
```json
{
  "items": [
    {"run_id":"run_01J10...", "kpi_id":"CFO-AR-DSO", "contract_version":"1.2.0", "started_at":"...", "ended_at":"...", "sla_state":"pass", "status":"success"},
    {"run_id":"run_01J11...", "kpi_id":"CFO-AR-DSO", "contract_version":"1.2.0", "started_at":"...", "ended_at":"...", "sla_state":"warn", "status":"success"}
  ],
  "next_cursor": "eyJwYWdlIjoyfQ=="
}
```

### 3.2 Get Run Detail
`GET /logs/runs/{run_id}` → inputs, outputs, validations, lineage refs, errors.

### 3.3 Monitoring Views (materialized)
`GET /monitoring/views/vw_kpi_run_overview?limit=100`  
`GET /monitoring/views/vw_kpi_validation_summary?limit=100`

## 4. Security & Policy APIs

### 4.1 Evaluate Policy (simulate)
`POST /policy/simulate`

**Request**
```json
{
  "user": { "id":"uid:123", "roles": ["Finance"], "region":"APAC" },
  "action": "kpi:Read",
  "resource": { "kpi_id": "CFO-AR-DSO", "sensitivity": "internal" },
  "slice": { "entity_region": ["APAC"], "grain": "month" }
}
```
**Response**
```json
{
  "decision": "Allow",
  "policy_sid": "AllowFinanceToReadInternalKPIs",
  "obligations": ["suppress_small_segments","grain_ge_month"],
  "policy_version": "2025-08-01",
  "trace_id": "req_01JB..."
}
```

### 4.2 Manage Tenant Policies
`GET  /policy` → current policy document  
`PUT  /policy` → replace policy (Change Request required if locked)  
Supports JSON (IAM-style), Cedar (Verified Permissions), or Rego (OPA).

## 5. Consumption APIs

### 5.1 Get KPI Metadata
`GET /metadata/kpis/{kpi_id}` → owners, sensitivity, contract_version, last_run, lineage refs.

### 5.2 Download KPI Results
`POST /results/export`
```json
{
  "kpi_id":"CFO-AR-DSO",
  "time":{"grain":"month","range":{"start":"2024-01","end":"2024-12"}},
  "filters":{},
  "format":"csv"
}
```
**Response**
```json
{ "export_id":"exp_01JC...", "status_url": "/results/exports/exp_01JC..." }
```

`GET /results/exports/{export_id}` → returns signed URL or inline file (subject to policy obligations).

## 6. Webhooks (optional, tenant-configured)

Events (via HTTPS POST; retries with exponential backoff):
- `kpi.run.completed`
- `kpi.run.failed`
- `kpi.sla.breach`
- `kpi.version.published`
- `kpi.paused`
- `kpi.change_request.pending`

**Delivery**  
- Signature header: `X-Cxofacts-Signature: sha256=<HMAC>`  
- Retries: 6 attempts over ~15 minutes.

## 7. Rate Limits

Default per tenant (configurable):
- Reads: 600 requests / minute  
- Writes: 120 requests / minute  
- Bursts: token bucket; `429` with `Retry-After` on exceed

## 8. Idempotency & Concurrency

- All mutating endpoints accept `X-Idempotency-Key`.  
- Concurrent updates on the same KPI/version shall return `409 CONFLICT` with a retry token.  
- Change Requests serialize via queue per `kpi_id`.

## 9. Security Notes

- All endpoints enforce tenant scoping + policy evaluation.  
- Responses include `policy_version` and any applied obligations (masking, grain limits).  
- Admin endpoints require elevated roles (dual approval for critical changes).

## 10. Examples (curl)

**Execute KPI**
```bash
curl -X POST "https://api.cxofacts.com/prod/kpi/v1/calls/execute" \  -H "Authorization: Bearer $TOKEN" \  -H "X-Tenant-Id: acme" \  -H "Content-Type: application/json" \  -d '{
    "kpi_id":"CFO-AR-DSO",
    "time":{"grain":"month","range":{"start":"2024-01","end":"2024-12"}},
    "filters":{"legal_entity":["LE-APAC-01"]},
    "extensions":{"time":["YoY","MoM"],"entity":["currency=USD"]},
    "scd_view":"as_reported"
  }'
```

**Publish Version**
```bash
curl -X POST "https://api.cxofacts.com/prod/kpi/v1/admin/kpis/CFO-AR-DSO/versions/1.2.0/publish" \  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: acme"
```

**Simulate Policy**
```bash
curl -X POST "https://api.cxofacts.com/prod/kpi/v1/policy/simulate" \  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: acme" \  -H "Content-Type: application/json" \  -d '{ "user":{"roles":["Finance"]}, "action":"kpi:Read", "resource":{"kpi_id":"CFO-AR-DSO","sensitivity":"internal"}, "slice":{"entity_region":["APAC"],"grain":"month"} }'
```

## 11. Changelog

- v1.0 - Initial surface covering Calls, Admin, Logs, Policy, Consumption, Webhooks.

## Diagrams

None

## Tables

None



## Glossary

None
