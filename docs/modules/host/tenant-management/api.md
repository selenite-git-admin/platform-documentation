# API

## Scope
Endpoints for creating tenants, managing lifecycle, and editing metadata such as regions, residency, plan binding, contacts, tags, and external identifiers.

## Conventions
- Base path is `/tenant-management/v1`
- Requests and responses use `application/json`
- Authentication and authorization handled by Access Modules
- Idempotency uses `Idempotency-Key` on POST and state changing PUTs
- Time uses UTC ISO 8601

## Endpoints

### At a glance
| Operation | Method and Path |
| --- | --- |
| [Search tenants](#search-tenants) | `GET /tenant-management/v1/tenants?q=&status=&region=&tag=` |
| [Get tenant](#get-tenant) | `GET /tenant-management/v1/tenants/{tenant_id}` |
| [Create tenant](#create-tenant) | `POST /tenant-management/v1/tenants` |
| [Update tenant](#update-tenant) | `PUT /tenant-management/v1/tenants/{tenant_id}` |
| [Activate](#activate) | `POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/activate` |
| [Suspend](#suspend) | `POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/suspend` |
| [Resume](#resume) | `POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/resume` |
| [Archive](#archive) | `POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/archive` |
| [Get regions](#get-regions) | `GET /tenant-management/v1/tenants/{tenant_id}/regions` |
| [Put regions](#put-regions) | `PUT /tenant-management/v1/tenants/{tenant_id}/regions` |
| [Get residency](#get-residency) | `GET /tenant-management/v1/tenants/{tenant_id}/residency` |
| [Put residency](#put-residency) | `PUT /tenant-management/v1/tenants/{tenant_id}/residency` |
| [Get plan](#get-plan) | `GET /tenant-management/v1/tenants/{tenant_id}/plan` |
| [Put plan](#put-plan) | `PUT /tenant-management/v1/tenants/{tenant_id}/plan` |
| [Get contacts](#get-contacts) | `GET /tenant-management/v1/tenants/{tenant_id}/contacts` |
| [Put contacts](#put-contacts) | `PUT /tenant-management/v1/tenants/{tenant_id}/contacts` |
| [Get external ids](#get-external-ids) | `GET /tenant-management/v1/tenants/{tenant_id}/external-ids` |
| [Put external ids](#put-external-ids) | `PUT /tenant-management/v1/tenants/{tenant_id}/external-ids` |
| [Get tags](#get-tags) | `GET /tenant-management/v1/tenants/{tenant_id}/tags` |
| [Put tags](#put-tags) | `PUT /tenant-management/v1/tenants/{tenant_id}/tags` |

### Search tenants
`GET /tenant-management/v1/tenants?q=&status=&region=&tag=`

Response 200
```json
{"items":[{"tenant_id":"...","slug":"acme","legal_name":"Acme Inc","status":"active"}]}
```

### Get tenant
`GET /tenant-management/v1/tenants/{tenant_id}`

Response 200
```json
{"tenant_id":"...","slug":"acme","legal_name":"Acme Inc","status":"active"}
```

### Create tenant
`POST /tenant-management/v1/tenants`

Request
```json
{"slug":"acme","legal_name":"Acme Inc"}
```

Response 201
```json
{"tenant_id":"...","slug":"acme"}
```

### Update tenant
`PUT /tenant-management/v1/tenants/{tenant_id}`

Request
```json
{"legal_name":"Acme Incorporated"}
```

Response 200
```json
{"tenant_id":"...","updated_at":"2025-10-03T12:00:00Z"}
```

### Activate
`POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/activate`

Response 200
```json
{"tenant_id":"...","status":"active"}
```

### Suspend
`POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/suspend`

Response 200
```json
{"tenant_id":"...","status":"suspended"}
```

### Resume
`POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/resume`

Response 200
```json
{"tenant_id":"...","status":"active"}
```

### Archive
`POST /tenant-management/v1/tenants/{tenant_id}/lifecycle/archive`

Response 200
```json
{"tenant_id":"...","status":"archived"}
```

### Get regions
`GET /tenant-management/v1/tenants/{tenant_id}/regions`

Response 200
```json
{"items":["ap-south-1","eu-central-1"]}
```

### Put regions
`PUT /tenant-management/v1/tenants/{tenant_id}/regions`

Request
```json
{"items":["ap-south-1","eu-central-1"]}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

### Get residency
`GET /tenant-management/v1/tenants/{tenant_id}/residency`

Response 200
```json
{"policy":{"policy_id":"...","effective_from":"2025-10-01"}}
```

### Put residency
`PUT /tenant-management/v1/tenants/{tenant_id}/residency`

Request
```json
{"policy_id":"...","effective_from":"2025-10-01"}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

### Get plan
`GET /tenant-management/v1/tenants/{tenant_id}/plan`

Response 200
```json
{"plan_code":"pro","effective_from":"2025-10-01"}
```

### Put plan
`PUT /tenant-management/v1/tenants/{tenant_id}/plan`

Request
```json
{"plan_code":"pro","effective_from":"2025-10-01"}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

### Get contacts
`GET /tenant-management/v1/tenants/{tenant_id}/contacts`

Response 200
```json
{"items":[{"role":"owner","name":"Jane Doe","email":"owner@example.com"}]}
```

### Put contacts
`PUT /tenant-management/v1/tenants/{tenant_id}/contacts`

Request
```json
{"items":[{"role":"owner","name":"Jane Doe","email":"owner@example.com"}]}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

### Get external ids
`GET /tenant-management/v1/tenants/{tenant_id}/external-ids`

Response 200
```json
{"items":[{"system_key":"billing","id_value":"BILL-123"}]}
```

### Put external ids
`PUT /tenant-management/v1/tenants/{tenant_id}/external-ids`

Request
```json
{"items":[{"system_key":"billing","id_value":"BILL-123"}]}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

### Get tags
`GET /tenant-management/v1/tenants/{tenant_id}/tags`

Response 200
```json
{"items":[{"tag_key":"sector","tag_value":"manufacturing"}]}
```

### Put tags
`PUT /tenant-management/v1/tenants/{tenant_id}/tags`

Request
```json
{"items":[{"tag_key":"sector","tag_value":"manufacturing"}]}
```

Response 200
```json
{"updated_at":"2025-10-03T12:00:00Z"}
```

## Error model
```json
{"code":"invalid_request","message":"unknown region_code: ap-nowhere-1","correlation_id":"..."}
```

## Idempotency and caching
- Use `Idempotency-Key` for POST and lifecycle transitions
- Return `ETag` on tenant reads and accept `If-None-Match`
