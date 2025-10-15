# API

## Scope
Endpoints to ingest lineage events, author obligations, query the lineage graph, and read evaluation results.

## Conventions
- Base path is `/lineage/v1`
- Requests and responses use `application/json`
- Authentication and authorization handled by Access Modules
- Idempotency uses `Idempotency-Key` on POST
- Time uses UTC ISO 8601

## Endpoints

### At a glance
| Operation | Method and Path |
| --- | --- |
| [Ingest lineage event](#ingest-lineage-event) | `POST /lineage/v1/events` |
| [Batch ingest](#batch-ingest) | `POST /lineage/v1/events:batch` |
| [Get asset](#get-asset) | `GET /lineage/v1/assets/{asset_id}` |
| [Search assets](#search-assets) | `GET /lineage/v1/assets?q=&layer=&tag=` |
| [Traverse graph](#traverse-graph) | `GET /lineage/v1/graph?asset_id=&depth=&direction=` |
| [List runs](#list-runs) | `GET /lineage/v1/processes/{process_id}/runs` |
| [List obligations](#list-obligations) | `GET /lineage/v1/obligations` |
| [Create obligation](#create-obligation) | `POST /lineage/v1/obligations` |
| [Update obligation](#update-obligation) | `PUT /lineage/v1/obligations/{obligation_id}` |
| [List evaluations](#list-evaluations) | `GET /lineage/v1/evaluations?status=&obligation_id=&since=` |
| [Evaluate now](#evaluate-now) | `POST /lineage/v1/obligations/{obligation_id}:evaluate` |

### Ingest lineage event
`POST /lineage/v1/events`

Request
```json
{
  "tenant_id":"...",
  "run": {"process_id":"...","started_at":"2025-10-03T12:00:00Z","status":"running","correlation_id":"..."},
  "edges": [
    {"src_asset_id":"...","dest_asset_id":"...","op":"read","columns":null,"stats":{"rows":1000}},
    {"src_asset_id":"...","dest_asset_id":"...","op":"write","columns":null,"stats":{"rows":980}}
  ]
}
```

Response 202
```json
{"accepted":true}
```

### Batch ingest
`POST /lineage/v1/events:batch`

Request
```json
{"items":[{"tenant_id":"...","run":{...},"edges":[...]}]}
```

Response 202
```json
{"accepted":1,"failed":0}
```

### Get asset
`GET /lineage/v1/assets/{asset_id}`

Response 200
```json
{"asset_id":"...","qualified_name":"raw.sap.mm.mara","layer":"raw","tags":{"domain":"sap"}}
```

### Search assets
`GET /lineage/v1/assets?q=&layer=&tag=`

Response 200
```json
{"items":[{"asset_id":"...","qualified_name":"gold.kpi.materials","layer":"gold"}]}
```

### Traverse graph
`GET /lineage/v1/graph?asset_id=&depth=2&direction=both`

Response 200
```json
{"nodes":[{"id":"...","label":"gold.kpi.materials"}],"edges":[{"src":"...","dest":"...","op":"transform"}]}
```

### List runs
`GET /lineage/v1/processes/{process_id}/runs`

Response 200
```json
{"items":[{"run_id":"...","status":"success","started_at":"2025-10-03T12:00:00Z"}]}
```

### List obligations
`GET /lineage/v1/obligations`

Response 200
```json
{"items":[{"obligation_id":"...","name":"Gold requires contract","enabled":true}]}
```

### Create obligation
`POST /lineage/v1/obligations`

Request
```json
{"name":"Gold requires contract","check_type":"required_tag","params":{"tag_key":"contract"},"scope":{"layer":["gold"]}}
```

Response 201
```json
{"obligation_id":"..."}
```

### Update obligation
`PUT /lineage/v1/obligations/{obligation_id}`

Request
```json
{"enabled":false}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

### List evaluations
`GET /lineage/v1/evaluations?status=fail&since=2025-09-01T00:00:00Z`

Response 200
```json
{"items":[{"obligation_id":"...","status":"fail","evaluated_at":"2025-10-03T12:05:00Z","details":{"asset_id":"..."}}]}
```

### Evaluate now
`POST /lineage/v1/obligations/{obligation_id}:evaluate`

Request
```json
{"target":{"asset_id":"..."}} 
```

Response 200
```json
{"status":"pass","evaluated_at":"2025-10-03T12:06:00Z"}
```

## Error model
```json
{"code":"invalid_request","message":"unknown asset_id","correlation_id":"..."}
```

## Idempotency and caching
- Use `Idempotency-Key` on ingest and obligation updates
- Return `ETag` on obligation reads and accept `If-None-Match`
