# API (REST)

Base: `/api/v1/schema-registry`

## Headers
- `Authorization: Bearer <jwt>`
- `X-Tenant-Id: <ulid>`
- `X-Request-Id: <ulid>`

## Endpoints

### List subjects
`GET /subjects?kind=gdp&owner=finance&limit=50&cursor=...`

### Get subject
`GET /subjects/{subject}`

### Latest version
`GET /subjects/{subject}/versions/latest`

### Specific version
`GET /subjects/{subject}/versions/{version}`

### Create version (idempotent)
`POST /subjects/{subject}/versions`
```json
{ "schema": {...}, "compatibility":"additive", "aliases":["order_id","id"] }
```

### Validate only
`POST /validate`
```json
{ "kind":"kpi", "schema": {...}, "ruleset":"additive" }
```

### Propose deprecation
`POST /subjects/{subject}/deprecations`
```json
{ "field":"legacy_code", "sunset_after_days":180, "note":"replace with product_code" }
```

### Search
`GET /subjects/search?q=gdp.order tag:finance`

### Webhook replay
`POST /events/replay?since=...`
