# API

## Scope
This page defines the API surface for Data Contract Registry. It covers endpoints, request and response schemas, error model, idempotency rules, rate limits, and examples.

## Conventions
- Base path is `/data-contract-registry/v1`
- Requests and responses use `application/json`
- Authentication and authorization are handled by Access Modules
- Resource identifiers use `uuid`
- Time fields use UTC ISO 8601
- Idempotency uses the `Idempotency-Key` header on unsafe operations
- Pagination uses `page` and `page_size` query parameters
- Layer is one of `extraction`, `raw`, `gold`, `activation`

## Related documents
See [Data Model](data-model.md) for entities and relationships.

## Roles
- Producer can register datasets and ingest schemas for a layer
- Consumer can subscribe to dataset layers and read contracts
- Operator can read all resources

## Endpoints

### At a glance
| Operation | Method and Path |
| --- | --- |
| [Create dataset](#create-dataset) | `POST /data-contract-registry/v1/datasets` |
| [List datasets](#list-datasets) | `GET /data-contract-registry/v1/datasets` |
| [Get dataset](#get-dataset) | `GET /data-contract-registry/v1/datasets/{dataset_id}` |
| [Ingest schema for a layer](#ingest-schema-for-a-layer) | `POST /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/schemas` |
| [List schema versions](#list-schema-versions) | `GET /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/versions` |
| [Get schema version](#get-schema-version) | `GET /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/versions/{version}` |
| [Diff versions](#diff-versions) | `GET /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/diff?from={v1}&to={v2}` |
| [Create subscription](#create-subscription) | `POST /data-contract-registry/v1/subscriptions` |
| [List subscriptions](#list-subscriptions) | `GET /data-contract-registry/v1/subscriptions` |
| [Compatibility check](#compatibility-check) | `POST /data-contract-registry/v1/compatibility/check` |

### Create dataset
`POST /data-contract-registry/v1/datasets`

Request
```json
{
  "namespace": "sap.mm",
  "name": "mara",
  "owner": "platform-admins",
  "steward": "stewards@example.com"
}
```

Response 201
```json
{
  "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
  "namespace": "sap.mm",
  "name": "mara",
  "owner": "platform-admins",
  "steward": "stewards@example.com",
  "status": "active",
  "created_at": "2025-02-12T10:00:00Z",
  "created_by": "svc-dcr@svc"
}
```

### List datasets
`GET /data-contract-registry/v1/datasets?namespace=sap.mm&name=&status=active&page=1&page_size=50`

Response 200
```json
{
  "items": [
    {
      "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
      "namespace": "sap.mm",
      "name": "mara",
      "owner": "platform-admins",
      "status": "active",
      "created_at": "2025-02-12T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 1
}
```

### Get dataset
`GET /data-contract-registry/v1/datasets/{dataset_id}`

Response 200
```json
{
  "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
  "namespace": "sap.mm",
  "name": "mara",
  "owner": "platform-admins",
  "steward": "stewards@example.com",
  "status": "active",
  "created_at": "2025-02-12T10:00:00Z"
}
```

### Ingest schema for a layer
`POST /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/schemas`

Request
```json
{
  "schema_json": {
    "type": "record",
    "name": "mara_extraction",
    "fields": [
      {"name": "matnr", "type": "string"},
      {"name": "maktx", "type": "string"}
    ]
  },
  "schema_registry_id": null,
  "set_current_if_compatible": true
}
```

Response 201
```json
{
  "version": 1,
  "is_current": true,
  "compatibility": "both",
  "schema_registry_id": null,
  "created_at": "2025-03-01T09:00:00Z"
}
```

### List schema versions
`GET /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/versions?page=1&page_size=50`

Response 200
```json
{
  "items": [
    {
      "version": 2,
      "is_current": true,
      "compatibility": "backward",
      "created_at": "2025-03-05T12:00:00Z"
    },
    {
      "version": 1,
      "is_current": false,
      "compatibility": "both",
      "created_at": "2025-03-01T09:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 2
}
```

### Get schema version
`GET /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/versions/{version}`

Response 200
```json
{
  "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
  "layer": "gold",
  "version": 2,
  "schema_json": { "...": "..." },
  "schema_registry_id": "srn:schema-registry:12345",
  "compatibility": "backward",
  "is_current": true,
  "created_at": "2025-03-05T12:00:00Z"
}
```

### Diff versions
`GET /data-contract-registry/v1/datasets/{dataset_id}/layers/{layer}/diff?from=1&to=2`

Response 200
```json
{
  "from": 1,
  "to": 2,
  "changes": [
    {"op": "add_field", "path": "/fields/-", "field": {"name": "currency", "type": "string", "optional": true}}
  ],
  "classification": "compatible"
}
```

### Create subscription
`POST /data-contract-registry/v1/subscriptions`

Request
```json
{
  "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
  "layer": "activation",
  "consumer": "svc-activation-api",
  "required_compatibility": "backward",
  "min_version": 1
}
```

Response 201
```json
{
  "subscription_id": "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
  "layer": "activation",
  "consumer": "svc-activation-api",
  "required_compatibility": "backward",
  "min_version": 1,
  "created_at": "2025-03-07T10:00:00Z"
}
```

### List subscriptions
`GET /data-contract-registry/v1/subscriptions?dataset_id=&layer=&consumer=&page=1&page_size=50`

Response 200
```json
{
  "items": [
    {
      "subscription_id": "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
      "layer": "activation",
      "consumer": "svc-activation-api",
      "required_compatibility": "backward",
      "min_version": 1,
      "created_at": "2025-03-07T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 1
}
```

### Compatibility check
`POST /data-contract-registry/v1/compatibility/check`

Request
```json
{
  "dataset_id": "2c5b8b7a-1df3-4e7a-a0b2-1b1f1ad7d9f1",
  "layer": "gold",
  "base_version": 2,
  "schema_json": { "... candidate schema ..." }
}
```

Response 200
```json
{
  "classification": "compatible",
  "changes": [
    {"op": "add_field", "path": "/fields/-", "field": {"name": "currency", "type": "string", "optional": true}}
  ]
}
```

## Error model
Errors use HTTP status codes and a common body.

```json
{
  "code": "invalid_request",
  "message": "layer must be one of extraction, raw, gold, activation",
  "details": { "field": "layer" },
  "correlation_id": "df2f4e85a5d64e7bb7a1b1a5a2f4c6d8"
}
```

Common codes
- invalid_request
- unauthorized
- forbidden
- not_found
- conflict
- rate_limited
- internal_error

## Idempotency
- Use `Idempotency-Key` for POST requests that create resources or produce side effects
- The server stores the first result for a given key for 24 hours and returns the same result for retries
- Keys must be unique per resource type and caller

## Rate limits
- Apply per service account and per endpoint
- Return `429` with `Retry-After` when limits are exceeded

## Examples

Ingest schema
```bash
curl -X POST "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/gold/schemas"   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -H "Idempotency-Key: $(uuidgen)"   -d '{"schema_json":{"type":"record","name":"key_materials","fields":[{"name":"material_id","type":"string"}]},"set_current_if_compatible":true}'
```

Diff versions
```bash
curl -s "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/gold/diff?from=1&to=2"   -H "Authorization: Bearer $TOKEN"
```
