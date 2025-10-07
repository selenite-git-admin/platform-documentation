# API

## Scope
This page defines the API surface for Policy Registry. It includes endpoints, request and response schemas, error model, idempotency rules, and examples.

## Conventions
- Base path is `/policy-registry/v1`
- All requests and responses use `application/json`
- Authentication and authorization are handled by Access Modules
- Resource identifiers are `uuid`
- Time fields use UTC ISO 8601
- Idempotency uses the `Idempotency-Key` header on unsafe operations
- Pagination uses `page` and `page_size` query parameters

## Related documents
See [Data Model](data-model.md) for table structures and relationships.

## Roles
- Policy Administrator can create and update policies and bindings
- Operator can read policies, bindings, and evaluations
- Service account can call evaluate

## Endpoints

### At a glance
| Operation | Method and Path |
| --- | --- |
| [Create policy](#create-policy) | `POST /policy-registry/v1/policies` |
| [List policies](#list-policies) | `GET /policy-registry/v1/policies` |
| [Get policy](#get-policy) | `GET /policy-registry/v1/policies/{policy_id}` |
| [Create policy version](#create-policy-version) | `POST /policy-registry/v1/policies/{policy_id}/versions` |
| [List policy versions](#list-policy-versions) | `GET /policy-registry/v1/policies/{policy_id}/versions` |
| [Set current version](#set-current-version) | `POST /policy-registry/v1/policies/{policy_id}/versions/{version}/current` |
| [Create binding](#create-binding) | `POST /policy-registry/v1/bindings` |
| [List bindings](#list-bindings) | `GET /policy-registry/v1/bindings` |
| [Evaluate](#evaluate) | `POST /policy-registry/v1/evaluate` |
| [Get evaluation](#get-evaluation) | `GET /policy-registry/v1/evaluations/{eval_id}` |



### Create policy
`POST /policy-registry/v1/policies`

Request
```json
{
  "name": "Export Requires Approval",
  "category": "export",
  "status": "active"
}
```

Response 201
```json
{
  "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
  "name": "Export Requires Approval",
  "category": "export",
  "status": "active",
  "created_at": "2025-01-15T10:30:00Z",
  "created_by": "admin@example.com"
}
```

### List policies
`GET /policy-registry/v1/policies?status=active&category=export&page=1&page_size=50`

Response 200
```json
{
  "items": [
    {
      "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
      "name": "Export Requires Approval",
      "category": "export",
      "status": "active",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 1
}
```

### Get policy
`GET /policy-registry/v1/policies/{policy_id}`

Response 200
```json
{
  "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
  "name": "Export Requires Approval",
  "category": "export",
  "status": "active",
  "created_at": "2025-01-15T10:30:00Z",
  "created_by": "admin@example.com"
}
```

### Create policy version
`POST /policy-registry/v1/policies/{policy_id}/versions`

Request
```json
{
  "definition": {
    "rule": "require_approval",
    "applies_to": "export"
  },
  "set_current": true
}
```

Response 201
```json
{
  "version_id": "2d1b5bfc-6f40-4b56-9f4c-1f9b2c64cb7c",
  "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
  "version": 2,
  "is_current": true,
  "created_at": "2025-01-20T09:00:00Z"
}
```

### List policy versions
`GET /policy-registry/v1/policies/{policy_id}/versions`

Response 200
```json
{
  "items": [
    {
      "version_id": "2d1b5bfc-6f40-4b56-9f4c-1f9b2c64cb7c",
      "version": 2,
      "is_current": true,
      "created_at": "2025-01-20T09:00:00Z"
    },
    {
      "version_id": "d7f74b5f-4dea-4c63-9c7a-9c1e16b67d7a",
      "version": 1,
      "is_current": false,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Set current version
`POST /policy-registry/v1/policies/{policy_id}/versions/{version}/current`

Response 204

### Create binding
`POST /policy-registry/v1/bindings`

Request
```json
{
  "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
  "version_id": "2d1b5bfc-6f40-4b56-9f4c-1f9b2c64cb7c",
  "scope_type": "tenant",
  "scope_ref": "tenant-acme",
  "status": "active"
}
```

Response 201
```json
{
  "binding_id": "3f0c1a5a-3d35-4f78-8f3e-7b4a49f25d85",
  "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
  "version_id": "2d1b5bfc-6f40-4b56-9f4c-1f9b2c64cb7c",
  "scope_type": "tenant",
  "scope_ref": "tenant-acme",
  "status": "active",
  "created_at": "2025-01-20T09:05:00Z"
}
```

### List bindings
`GET /policy-registry/v1/bindings?scope_type=tenant&scope_ref=tenant-acme&page=1&page_size=50`

Response 200
```json
{
  "items": [
    {
      "binding_id": "3f0c1a5a-3d35-4f78-8f3e-7b4a49f25d85",
      "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
      "version_id": "2d1b5bfc-6f40-4b56-9f4c-1f9b2c64cb7c",
      "scope_type": "tenant",
      "scope_ref": "tenant-acme",
      "status": "active",
      "created_at": "2025-01-20T09:05:00Z"
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 1
}
```

### Evaluate
`POST /policy-registry/v1/evaluate`

Request
```json
{
  "scope_type": "tenant",
  "scope_ref": "tenant-acme",
  "subject_type": "schema_change",
  "subject_ref": "kpi:finance:monthly_revenue:v2",
  "context": {
    "fields_present": ["period_start", "period_end", "currency"],
    "actor": "svc-schema-registry-checker@svc",
    "requested_at": "2025-02-01T08:00:00Z"
  }
}
```

Response 200
```json
{
  "decision": "require_approval",
  "reason_code": "export_requires_approval",
  "policy_id": "8e2b6a17-2a0a-4a3e-8f1c-4a0f2b0a9a10",
  "policy_version": 2,
  "eval_id": "0b0dfd58-1a21-43a9-8d84-2f0dc6c4872c",
  "evaluated_at": "2025-02-01T08:00:01Z"
}
```

### Get evaluation
`GET /policy-registry/v1/evaluations/{eval_id}`

Response 200
```json
{
  "eval_id": "0b0dfd58-1a21-43a9-8d84-2f0dc6c4872c",
  "binding_id": "3f0c1a5a-3d35-4f78-8f3e-7b4a49f25d85",
  "subject_type": "schema_change",
  "subject_ref": "kpi:finance:monthly_revenue:v2",
  "decision": "require_approval",
  "reason_code": "export_requires_approval",
  "evaluator_version": "pr-1.2.0",
  "evaluated_at": "2025-02-01T08:00:01Z"
}
```

## Error model
Errors use HTTP status codes and a common body.

```json
{
  "code": "invalid_request",
  "message": "scope_type must be one of tenant, schema-registry, workflow",
  "details": {
    "field": "scope_type"
  },
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

Create policy
```bash
curl -X POST "$BASE/policy-registry/v1/policies"   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -H "Idempotency-Key: 5b2a3d2e-1e9d-4b8b-8f5d-9f2e3a4b5c6d"   -d '{"name":"Export Requires Approval","category":"export","status":"active"}'
```

Evaluate
```bash
curl -X POST "$BASE/policy-registry/v1/evaluate"   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -d '{"scope_type":"tenant","scope_ref":"tenant-acme","subject_type":"schema_change","subject_ref":"kpi:finance:monthly_revenue:v2","context":{"actor":"svc-schema-checker@svc"}}'
```
