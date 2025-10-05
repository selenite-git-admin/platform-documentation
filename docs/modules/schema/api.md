# API

Base path: `/api/v1/schema-registry`

## List subjects
`GET /subjects?kind=gdp|raw|kpi&owner=finance&limit=50&cursor=...`

## Get latest version
`GET /subjects/{subject}/versions/latest`

## Get specific version
`GET /subjects/{subject}/versions/{version}`

## Create version (idempotent)
`POST /subjects/{subject}/versions`
```json
{
  "schema": { "$schema":"https://json-schema.org/draft/2020-12/schema", "type":"object", "properties":{ "id":{"type":"string"}, "amount":{"type":"number"} }, "required":["id"] },
  "compatibility": "additive",
  "aliases": ["id","order_id"],
  "note": "Add amount; required stays compatible (new required is not allowed)."
}
```
**201**
```json
{ "version": 24, "evidence_id": "ev_01J...", "checksum":"sha256:..." }
```

## Validate (no write)
`POST /validate`
```json
{ "kind":"kpi", "schema": { "type":"object", "properties":{ "kpi":{"type":"string"} } }, "ruleset": "additive" }
```
**200** `{ "valid": true, "problems": [] }`

## Deprecation proposal
`POST /subjects/{subject}/deprecations`
```json
{ "field":"legacy_code", "sunset_after_days": 180, "note":"Replace with product_code" }
```

## Search subjects
`GET /subjects/search?q=gdp.orders owner:finance tag:core`
