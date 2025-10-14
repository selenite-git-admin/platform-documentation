# Dataset Refresh Registry (DRR) API

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Purpose  
The DRR API provides a stable, read-optimized interface for querying and updating dataset freshness state. It isolates read availability from runtime orchestration load.  
All external consumers use **public read APIs**; only Runtime uses **internal write APIs**.  

## API Overview  

| Type | Method | Path | Auth | Description |
|------|---------|------|------|-------------|
| Read | GET | `/storage/v1/datasets/{id}/freshness` | user or m2m | Returns current freshness state for a dataset |
| Read | GET | `/storage/v1/datasets?layer=&tenant_id=&status=` | user or m2m | Lists datasets filtered by layer or status |
| Read | GET | `/storage/v1/datasets/{id}/runs?limit=` | user or m2m | Returns recent run history |
| Read | GET | `/storage/v1/datasets/{id}:describe?include=freshness` | user or m2m | Joins freshness with catalog metadata |
| Write | POST | `/storage-internal/v1/datasets/{id}/refresh-state` | internal m2m | Updates freshness after job completion |

## Public Read APIs  

### GET /storage/v1/datasets/{id}/freshness
Returns the most recent refresh state for a single dataset.  

**Response – 200 OK**
```json
{
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "layer": "kpi",
  "tenant_scope": "multi",
  "last_success_at": "2025-10-12T06:02:14Z",
  "next_scheduled_at": "2025-10-12T08:00:00Z",
  "freshness_slo_sec": 10800,
  "freshness_lag_sec": 421,
  "status": "fresh",
  "source": {"runtime_run_id": "run_01HBV0K5S3"}
}
```

**Response – 404 Not Found**
```json
{ "code": "not_found", "message": "Dataset not registered in DRR", "correlation_id": "uuid-v7" }
```

### GET /storage/v1/datasets?layer=&tenant_id=&status=
Retrieves a filtered list of datasets with their freshness summary.

**Example**
```
GET /storage/v1/datasets?tenant_id=tnt_123&status=late
```

**Response – 200 OK**
```json
{
  "items": [
    {
      "dataset_id": "sales.pipeline_summary",
      "layer": "gdp",
      "status": "late",
      "freshness_lag_sec": 14300,
      "last_success_at": "2025-10-12T00:00:00Z"
    }
  ],
  "count": 1
}
```

### GET /storage/v1/datasets/{id}/runs
Lists recent run history for a dataset. Limited to 100 entries per call.

**Response – 200 OK**
```json
{
  "dataset_id": "sales.pipeline_summary",
  "runs": [
    {
      "run_id": "run_01HBV0K5S3",
      "status": "success",
      "started_at": "2025-10-12T06:02:14Z",
      "finished_at": "2025-10-12T06:04:01Z",
      "rows_out": 123450
    }
  ]
}
```

## Internal Write API  

### POST /storage-internal/v1/datasets/{id}/refresh-state
Runtime posts a dataset’s new state when a run completes.  

**Headers**
| Key | Required | Description |
|------|-----------|-------------|
| Authorization | Yes | Bearer token (internal m2m) |
| Idempotency-Key | Yes | Prevents duplicate updates |
| Content-Type | Yes | application/json |

**Request Example**
```json
{
  "layer": "gdp",
  "schedule": {"cron":"0 */2 * * *","timezone":"UTC"},
  "run_id": "run_01HBV0K5S3",
  "status": "success",
  "started_at": "2025-10-12T06:02:14Z",
  "finished_at": "2025-10-12T06:04:01Z",
  "rows_in": 123456,
  "rows_out": 123450,
  "freshness_slo_sec": 10800
}
```

**Response – 200 OK**
```json
{ "updated": true, "dataset_id": "kpi.cash_conversion_cycle_v2", "status": "fresh" }
```

**Response – 409 Conflict**
```json
{ "code": "stale_update", "message": "Update older than current record", "correlation_id": "uuid-v7" }
```

## Error Envelope  
All responses follow a common error envelope.  
```json
{
  "code": "invalid_request|not_found|forbidden|stale_update|internal_error",
  "message": "Human-readable detail",
  "correlation_id": "uuid-v7",
  "details": {"field": "reason"}
}
```

## Events  

| Event Name | Description | Key Fields |
|-------------|--------------|-------------|
| storage.dataset.refresh.completed | Successful refresh recorded | dataset_id, status, runtime_run_id, lag_seconds |
| storage.dataset.refresh.failed | Failed refresh reported | dataset_id, status, runtime_run_id, error_code |
| storage.dataset.freshness.slo_breached | Freshness lag exceeded SLO | dataset_id, lag_seconds, tenant_id |

Events are emitted asynchronously after each state change. Delivery is at-least-once; consumers must de-duplicate using runtime_run_id.  

## Performance and Limits  

| Parameter | Value | Notes |
|------------|--------|-------|
| Read latency (P99) | ≤ 100 ms | at 2 k RPS per region |
| Write propagation lag | ≤ 10 s | Runtime → DRR visibility |
| Max payload size | 64 KB | per update |
| Max list response | 500 items | paginated via cursor |
| Idempotency key retention | 24 h | deduplication window |

## Audit and Traceability  
Every API call logs the correlation_id and runtime_run_id to the Evidence Ledger through an asynchronous link.  
Write operations are fully auditable; all decisions use deterministic timestamps.  

## Availability Targets  
- Read APIs: 99.99% regional availability  
- Write API: 99.9% regional availability  
- Propagation consistency: 10 s or less between Runtime post and visible freshness state  

## Security Summary  
- Authentication via JWT with scoped service roles (storage.read.refresh, storage.write.refresh).  
- All responses include an ETag for caching and integrity checks.  
- Tenancy is enforced by tenant_id filters at query level and via RLS at database level.