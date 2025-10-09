# API

> All endpoints are versioned under `/api/v1/migration-service` and follow platform API Standards (cursor paging, idempotency, standard errors).

## Headers
- `Authorization: Bearer <jwt>`
- `X-Tenant-Id: <ulid>`
- `X-Request-Id: <ulid>`

## Endpoints

### List resources
`GET /api/v1/migration-service/resources?limit=50&cursor=...&query=...`  
**200**
```json
{
  "items": [{ "id":"res_01J...", "name":"...", "updated_at":"2025-10-05T00:00:00Z" }],
  "next_cursor": "..."
}
```

### Get by id
`GET /api/v1/migration-service/resources/{id}`

### Create / update (idempotent)
`POST /api/v1/migration-service/resources`  
```json
{ "name":"...", "spec":{} }
```
**201** returns created object + `evidence_id`.
Re‑sending with same `X-Request-Id` returns **200** with the original result.

### Delete
`DELETE /api/v1/migration-service/resources/{id}` → **204**

### Webhook replay
`POST /api/v1/migration-service/events/replay`

## Errors (canonical)
```json
{ "error":"invalid_request", "message":"...", "request_id":"req_01J..." }
```

    ### Create migration plan
    `POST /api/v1/migration-service/plans`
    ```json
    { "subject":"dataset:orders", "steps":[{"op":"add_column","path":"customer_segment","default":null}], "dry_run":true }
    ```
    **201** `{ "plan_id":"plan_01J...", "status":"planned" }`

    ### Execute
    `POST /api/v1/migration-service/plans/{plan_id}:execute`
