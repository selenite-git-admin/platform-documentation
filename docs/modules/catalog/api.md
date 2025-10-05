# API

Base path: `/api/v1/catalog`

## Search
`GET /search?query=orders tag:finance fresh:<24h&limit=50&cursor=...`

## Get item
`GET /items/{slug}`

## Upsert item (idempotent)
`POST /items`
```json
{ "type":"dataset","slug":"gdp.orders","name":"Orders","owner":"data-finance","tags":["finance","orders"], "links": { "storage":"...", "delivery":"..." } }
```

## Signals ingest
`POST /signals`
```json
{ "slug":"gdp.orders", "freshness_ms": 5400000, "quality_score": 92, "usage_7d": 124 }
```

## Link relations
`POST /items/{slug}/relations`
```json
{ "related":[ {"type":"kpi","slug":"kpi.gm%"} ] }
```
