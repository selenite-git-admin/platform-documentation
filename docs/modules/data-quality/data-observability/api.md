# API

> All endpoints are versioned under `/api/v1/data-observability` and follow platform API Standards (cursor paging, idempotency, standard errors).

## Headers
- `Authorization: Bearer <jwt>`
- `X-Tenant-Id: <ulid>`
- `X-Request-Id: <ulid>`

## Endpoints

### List resources
`GET /api/v1/data-observability/resources?limit=50&cursor=...&query=...`  
**200**
```json
{
  "items": [{ "id":"res_01J...", "name":"...", "updated_at":"2025-10-05T00:00:00Z" }],
  "next_cursor": "..."
}
```

### Get by id
`GET /api/v1/data-observability/resources/{id}`

### Create / update (idempotent)
`POST /api/v1/data-observability/resources`  
```json
{ "name":"...", "spec":{} }
```
**201** returns created object + `evidence_id`.
Re‑sending with same `X-Request-Id` returns **200** with the original result.

### Delete
`DELETE /api/v1/data-observability/resources/{id}` → **204**

### Webhook replay
`POST /api/v1/data-observability/events/replay`

## Errors (canonical)
```json
{ "error":"invalid_request", "message":"...", "request_id":"req_01J..." }
```

    ### List signals
    `GET /api/v1/data-observability/signals?dataset=orders&from=...&to=...`

## List resources

GET /observability/events supports filters for dataset_id, layer, metric, outcome, and time range.

## Get by id

GET /observability/events/{event_id} returns a single event.

## Create event

POST /observability/events accepts idempotent writes keyed by event_id.

## Create snapshot

POST /observability/snapshots creates a snapshot for a run and dataset and returns snapshot_id and hash.

## Get snapshot

GET /observability/snapshots/{snapshot_id} returns the immutable snapshot used by a promotion.

## List alerts

GET /observability/alerts lists alerts with severity and status filters.

## Acknowledge alert

POST /observability/alerts/{id}/ack marks an alert as acknowledged.
