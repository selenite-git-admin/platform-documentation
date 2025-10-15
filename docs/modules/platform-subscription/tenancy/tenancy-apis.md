# Tenancy Module APIs

**Audience:** Backend engineers, integration developers, platform SREs  
**Status:** Working draft  
**Purpose:** Provide a complete, self contained specification of the Tenancy HTTP APIs. This document defines resource models, endpoints, required headers, idempotency, versioning, pagination, search, lifecycle operations, residency and plan surfaces, webhook contracts, rate limits, and error semantics. Content merges the Tenancy baseline with the Tenant Management API conventions so integrators can build once and operate safely at scale.

## Principles

**Consistency first:** The same resource model and error semantics are used across read and write APIs.  
**Predictable behavior:** Every mutating call is idempotent. Every response is cache aware.  
**Security by default:** Authentication and authorization are required for all endpoints. Least privilege roles are enforced.  
**Observability built in:** Correlation identifiers and audit fields are present in every response.  
**Backwards compatibility:** Versioning rules ensure non breaking evolution.

## Base Path And Media Types

**Base path:** `/tenant-management/v1`  
**Media types:** `application/json` for requests and responses.  
**Character encoding:** UTF-8.  
**Time format:** RFC 3339 with timezone designator.

## Common Headers

**Request headers**
- `Authorization: Bearer <token>`
- `Idempotency-Key: <uuid>` for POST and state changing PUT operations
- `If-None-Match: <etag>` for conditional reads
- `X-Request-Id: <uuid>` for client side correlation

**Response headers**
- `ETag: <hash>` for caching
- `X-Request-Id: <uuid>` echoed back for tracing
- `X-Correlation-Id: <uuid>` for cross service tracing
- `Retry-After: <seconds>` on 429 responses

## Versioning

**URI versioning** is used through the base path. Minor, non breaking changes are additive. Removing or changing fields in incompatible ways requires a new version. Version deprecation follows a communicated schedule and dual run period.

## Authentication And Authorization

**Auth model:** OAuth 2.0 bearer tokens issued by the Access module.  
**Scopes:** read tenancy, write tenancy, manage webhooks, admin override.  
**Least privilege:** tokens are scoped to tenant or environment where possible. Mutating endpoints require write tenancy or admin override scope.

## Resource Model

**Tenant resource**
```json
{
  "tenantId": "t_123456",
  "displayName": "Example Corp",
  "state": "Active",
  "profile": "singleTenant",
  "planCode": "ENTERPRISE_PLUS",
  "residency": {
    "allowedRegions": ["ap-south-1","eu-central-1"],
    "preferredRegion": "ap-south-1",
    "dataSovereigntyRequired": true
  },
  "isolation": {
    "strategy": "dedicatedDatabase",
    "networkMode": "dedicatedVpc"
  },
  "quotas": {
    "storageGb": 5000,
    "eventsPerMinute": 3000,
    "connections": 200
  },
  "contacts": {
    "technical": "tech.ops@example.com",
    "billing": "ar@example.com",
    "incident": "oncall@example.com"
  },
  "externalIds": {
    "billing": "BILL-00988",
    "crm": "SFDC-ACCT-44A"
  },
  "tags": ["enterprise","finance"],
  "createdAt": "2025-10-08T10:00:00Z",
  "updatedAt": "2025-10-08T10:05:00Z",
  "etag": "W/"c5598-abc""
}
```

## Pagination And Search

**Query parameters**
- `page` default 1
- `pageSize` default 50, maximum 500
- `q` prefix search on display name and tags
- `filter` state equals Active, planCode equals ENTERPRISE_PLUS, region equals ap-south-1

**Response envelope**
```json
{
  "items": [ /* array of resources */ ],
  "page": 1,
  "pageSize": 50,
  "total": 1240
}
```

## Registry APIs

### Create Tenant
`POST /tenant-management/v1/tenants`

Request uses `Idempotency-Key`. A repeated POST with the same key must be treated as the same operation.

```json
{
  "displayName": "Example Corp",
  "profile": "singleTenant",
  "planCode": "ENTERPRISE_PLUS",
  "residency": {
    "allowedRegions": ["ap-south-1"],
    "preferredRegion": "ap-south-1"
  },
  "isolation": {
    "strategy": "dedicatedDatabase",
    "networkMode": "dedicatedVpc"
  },
  "contacts": {
    "technical": "tech.ops@example.com",
    "billing": "ar@example.com",
    "incident": "oncall@example.com"
  },
  "externalIds": {
    "billing": "BILL-00988",
    "crm": "SFDC-ACCT-44A"
  },
  "tags": ["enterprise"]
}
```

Response 201
```json
{
  "tenantId": "t_123456",
  "state": "Draft",
  "etag": "W/"a1b2c3""
}
```

### Get Tenant
`GET /tenant-management/v1/tenants/{tenantId}`

Supports `If-None-Match`. Returns 304 when unchanged.

### List Tenants
`GET /tenant-management/v1/tenants`

Supports pagination, filtering, and prefix search. Returns a response envelope.

### Update Tenant
`PUT /tenant-management/v1/tenants/{tenantId}`

Requires `Idempotency-Key`. Entire resource is replaced except for immutable fields. Returns new `etag`.

### Patch Tenant
`PATCH /tenant-management/v1/tenants/{tenantId}`

Supports JSON Merge Patch for selective field updates. Immutable fields cannot be changed.

### Delete Tenant
`DELETE /tenant-management/v1/tenants/{tenantId}`

Deletion is allowed for test tenants or when policy permits. Requires admin scope and audit.

## Lifecycle APIs

### Activate
`POST /tenant-management/v1/tenants/{tenantId}:activate`

Transitions from Draft to Active. Policy checks validate residency, quotas, and plan eligibility. Orchestrator begins provisioning and returns a job reference when asynchronous.

Response 202
```json
{"jobId":"job_7002","state":"running"}
```

### Suspend
`POST /tenant-management/v1/tenants/{tenantId}:suspend`

Requires justification in the request body for audit. Access is restricted according to policy.

### Resume
`POST /tenant-management/v1/tenants/{tenantId}:resume`

Resumes from Suspended to Active after validation passes.

### Archive
`POST /tenant-management/v1/tenants/{tenantId}:archive`

Moves tenant to Archived. Retention policy applies to data handling.

## Residency And Regions APIs

### Get Regions
`GET /tenant-management/v1/tenants/{tenantId}/regions`

Returns allowed and preferred regions. Useful for UI prompts and validations.

### Put Regions
`PUT /tenant-management/v1/tenants/{tenantId}/regions`

Updates allowed and preferred regions. Policy service validates residency before persisting.

### Get Residency
`GET /tenant-management/v1/tenants/{tenantId}/residency`

Returns resolved residency status and flags such as data sovereignty required.

### Put Residency
`PUT /tenant-management/v1/tenants/{tenantId}/residency`

Updates residency policy references for the tenant.

## Plan And Quotas APIs

### Get Plan
`GET /tenant-management/v1/tenants/{tenantId}/plan`

Returns current plan code and derived features.

### Put Plan
`PUT /tenant-management/v1/tenants/{tenantId}/plan`

Updates plan code. Quotas and features are recalculated and stored. Returns change summary for audit.

### Get Quotas
`GET /tenant-management/v1/tenants/{tenantId}/quotas`

Returns effective quotas including policy overrides.

### Put Quotas
`PUT /tenant-management/v1/tenants/{tenantId}/quotas`

Administrative override with ttl and reason required. Writes an audit entry.

## Contacts, External Ids, And Tags APIs

### Get Contacts
`GET /tenant-management/v1/tenants/{tenantId}/contacts`

### Put Contacts
`PUT /tenant-management/v1/tenants/{tenantId}/contacts`

### Get External Ids
`GET /tenant-management/v1/tenants/{tenantId}/external-ids`

### Put External Ids
`PUT /tenant-management/v1/tenants/{tenantId}/external-ids`

### Get Tags
`GET /tenant-management/v1/tenants/{tenantId}/tags`

### Put Tags
`PUT /tenant-management/v1/tenants/{tenantId}/tags`

Tags follow the platform taxonomy. Validation provides actionable error messages for unknown tags.

## Search APIs

`GET /tenant-management/v1/tenants:search?q=<query>&filter=<expr>&page=1&pageSize=50`

Filter examples
- `state eq Active`
- `planCode eq ENTERPRISE_PLUS`
- `region eq ap-south-1`

Search supports prefix queries on display name and tags. Complex queries must be served by the registry’s indexes configured in the data model.

## Webhook Management APIs

### List Webhooks
`GET /tenant-management/v1/tenants/{tenantId}/webhooks`

### Create Webhook
`POST /tenant-management/v1/tenants/{tenantId}/webhooks`

Body
```json
{
  "name":"billing-sync",
  "url":"https://billing.example.com/hooks/tenancy",
  "events":["TENANCY_ACTIVATED","TENANCY_SUSPENDED"],
  "signingKeyRef":"secret://tenancy/webhooks/signing",
  "retry":{"maxRetries":12,"backoffSeconds":30,"jitter":true}
}
```

### Delete Webhook
`DELETE /tenant-management/v1/tenants/{tenantId}/webhooks/{webhookId}`

### Requeue Dead Letters
`POST /tenant-management/v1/tenants/{tenantId}/webhooks:requeue`

Body
```json
{"sequenceFrom":1800,"sequenceTo":1900}
```

## Idempotency And Caching

**Idempotency**
- Provide `Idempotency-Key` on POST and state changing PUT. The server stores request hash and result for a dedupe window. Replays return the original response and status.
- Lifecycle transitions implement idempotent handlers so repeated calls do not create duplicate operations.

**Caching**
- `ETag` is returned on all GET responses. Clients use `If-None-Match` to avoid transfer when unchanged.
- Cache control headers may be set to limit staleness for directory style endpoints.

## Rate Limits

**Global limits**
- Read per tenant per minute and write per tenant per minute are enforced by the API gateway.
- Burst multiplier allows short spikes with token bucket semantics.

**Error signaling**
- 429 is returned when limits are exceeded. `Retry-After` communicates backoff guidance. Clients must implement exponential backoff.

## Error Model

**Structure**
```json
{
  "error": {
    "code": "RESIDENCY_OUT_OF_POLICY",
    "message": "Preferred region eu-west-1 is not allowed by residency policy",
    "requestId": "req_9f3a",
    "correlationId": "corr_1c77",
    "details": {
      "allowedRegions": ["ap-south-1","eu-central-1"]
    }
  }
}
```

**Common codes**
- `VALIDATION_FAILED`
- `RESIDENCY_OUT_OF_POLICY`
- `PLAN_NOT_FOUND`
- `QUOTA_EXCEEDED`
- `RATE_LIMITED`
- `NOT_FOUND`
- `CONFLICT`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `INTERNAL_ERROR`

Every error is logged with request id and correlation id. Sensitive information is not included in error strings.

## Observability

**Metrics**
- Request latency and error rate per endpoint
- Webhook delivery latency and failure counts
- Policy evaluation latency for mutating calls

**Logging**
- Structured JSON logs include tenant id, endpoint, method, status code, request id, correlation id, and user agent.

**Tracing**
- Correlation ids are propagated to downstream services for end to end tracing.

## CLI And Tooling

**CLI wrappers** provide convenience for creating, listing, and transitioning tenants. The CLI uses the same API contract and headers. Admin commands require explicit confirmation and write audit records.

## Backwards Compatibility And Deprecation

**Policy**
- Additive changes only in a given API version.
- Field removals or behavior changes require a new version path.
- Deprecations are announced with timelines, migration notes, and parallel availability of both versions for a defined period.

## Examples

**Create and activate flow**
1. Create tenant with POST. State is Draft.
2. Update residency or plan if necessary.
3. Activate with lifecycle endpoint. Response returns job id.
4. Poll job id or subscribe to webhooks for completion.
5. Read tenant to confirm state Active and placement metadata.

**Search and filter**
1. List tenants filtered by plan code and region.
2. Page through results using page and pageSize.
3. Use ETag caching to avoid repeated payloads on unchanged reads.

## Security Notes

**Least privilege and audit**
- Tokens are scoped to necessary actions only.
- All mutating calls require audit and policy checks before execution.
- Sensitive fields are redacted from logs and error messages.
