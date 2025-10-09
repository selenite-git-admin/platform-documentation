
# Tenancy Module - APIs

Audience: Platform engineers, service owners, integration developers  
Status: Draft v0.1  
Scope: REST endpoints, payload schemas, headers, versioning, idempotency, pagination, error model, webhooks, and event contracts. Includes internal and integration-facing APIs.

---

## 1. Principles

- Tenant context is explicit and required for all data plane calls.  
- All write operations are idempotent using a client supplied request identifier.  
- Versioning is path based and additive.  
- Responses are consistent across services. Errors use a common problem format.  
- Webhooks and event streams provide near real time notifications for lifecycle and policy changes.

---

## 2. Common Headers

```
X-Tenant-Id: t_7f3c2a
X-Env: prod          # dev | stage | prod
X-Request-Id: 3b1a2d...   # client generated UUID for idempotency
X-Client-Version: 1.12.0  # optional
Authorization: Bearer <access_token>
Content-Type: application/json
```

Notes  
- X-Tenant-Id and X-Env are required for tenant scoped calls.  
- Authorization tokens are issued by Access module and validated centrally.  
- X-Request-Id is required for POST, PUT, PATCH, DELETE.

---

## 3. Versioning

- Base path format: `/api/tenancy/v1/...`  
- Backward compatible fields may be added without a new version.  
- Breaking changes require a new version. Old versions are supported until end of life.

---

## 4. Resource Model

- Organization  
- Tenant  
- Environment  
- Workspace (optional)  
- Policy binding references

Identifiers are opaque strings. Clients must not infer meaning from identifier formats.

---

## 5. Registry APIs

### 5.1 Create Tenant

```
POST /api/tenancy/v1/tenants
Headers: X-Request-Id, Authorization
Body:
{
  "tenantId": "t_7f3c2a",
  "organizationId": "org_acme",
  "profile": "mt-standard",
  "environments": ["dev", "stage", "prod"],
  "quotas": { "storageGiB": 500, "concurrentJobs": 10 },
  "policies": { "dataResidency": "in-region-only", "encryption": "kms-per-tenant" },
  "billing": { "plan": "professional", "costCenter": "fin-ops" },
  "network": { "region": "ap-south-1", "privateEndpoint": true },
  "tags": { "owner": "team-analytics", "priority": "high" }
}
```

Response 201
```
{
  "id": "t_7f3c2a",
  "state": "Draft",
  "createdAt": "2025-10-08T16:30:00Z",
  "links": {
    "self": "/api/tenancy/v1/tenants/t_7f3c2a"
  }
}
```

Idempotency rules  
- If the same X-Request-Id and body are seen again, return 201 with the original response.  
- If the same X-Request-Id and a different body are seen, return 409 conflict with details.

### 5.2 Get Tenant

```
GET /api/tenancy/v1/tenants/{tenantId}
```

Query params  
- include=topology,policies,quotas,tags

### 5.3 List Tenants

```
GET /api/tenancy/v1/tenants?org={orgId}&state=Active&limit=50&cursor=eyJwYWdlIjoxfQ==
```

Pagination  
- Use `limit` and `cursor`.  
- Response includes `nextCursor` when more results exist.

### 5.4 Update Tenant

```
PUT /api/tenancy/v1/tenants/{tenantId}
Body: same shape as create. Partial update is not allowed for PUT.
```

### 5.5 Patch Tenant

```
PATCH /api/tenancy/v1/tenants/{tenantId}
Body:
{
  "profile": "st-dedicated",
  "quotas": { "storageGiB": 800 }
}
```

### 5.6 Delete Tenant

```
DELETE /api/tenancy/v1/tenants/{tenantId}
Query: force=false   # when true, skips archive and executes permanent delete if retention allows
```

Response 202 with lifecycle job reference. Deletion is asynchronous.

---

## 6. Environment APIs

### 6.1 Create Environment

```
POST /api/tenancy/v1/tenants/{tenantId}/environments
Body:
{
  "name": "stage",
  "region": "ap-south-1",
  "storageGiB": 300,
  "computeQuota": 10,
  "isolation": { "level": "strict" },
  "retentionDays": 90
}
```

### 6.2 Get Environment

```
GET /api/tenancy/v1/tenants/{tenantId}/environments/{name}
```

### 6.3 List Environments

```
GET /api/tenancy/v1/tenants/{tenantId}/environments
```

### 6.4 Update or Patch Environment

```
PUT /api/tenancy/v1/tenants/{tenantId}/environments/{name}
PATCH /api/tenancy/v1/tenants/{tenantId}/environments/{name}
```

### 6.5 Delete Environment

```
DELETE /api/tenancy/v1/tenants/{tenantId}/environments/{name}
```

---

## 7. Lifecycle APIs

Lifecycle actions are event driven and idempotent. All actions return a job resource that can be polled.

### 7.1 Activate Tenant

```
POST /api/tenancy/v1/tenants/{tenantId}:activate
```

### 7.2 Suspend Tenant

```
POST /api/tenancy/v1/tenants/{tenantId}:suspend
Body: { "reason": "billing" }
```

### 7.3 Resume Tenant

```
POST /api/tenancy/v1/tenants/{tenantId}:resume
```

### 7.4 Archive Tenant

```
POST /api/tenancy/v1/tenants/{tenantId}:archive
Body: { "retentionDays": 365 }
```

### 7.5 Delete Tenant

```
POST /api/tenancy/v1/tenants/{tenantId}:delete
Body: { "force": false }
```

### 7.6 Job Status

```
GET /api/tenancy/v1/jobs/{jobId}
```

Response
```
{
  "id": "job_19asf",
  "state": "Running",
  "progress": 0.42,
  "createdAt": "2025-10-08T16:31:00Z",
  "updatedAt": "2025-10-08T16:32:00Z",
  "logs": [ "... recent controller message ..." ]
}
```

---

## 8. Topology Discovery

Provides handles that other modules use to map storage, compute, secrets, and network resources.

```
GET /api/tenancy/v1/tenants/{tenantId}/topology?env=prod
```

Response
```
{
  "profile": "mt-standard",
  "db": { "type": "postgres", "database": "warehouse.shared", "schema": "t_7f3c2a" },
  "objectStore": { "bucket": "data.shared", "prefix": "tenants/t_7f3c2a/prod" },
  "runtime": { "queue": "jobs", "partitionKey": "t_7f3c2a" },
  "secrets": { "path": "secrets/t_7f3c2a/*" },
  "network": { "vpc": "vpc-main", "privateEndpoint": true }
}
```

For single tenant profile, values reflect dedicated resources.

---

## 9. Integration-facing APIs

### 9.1 Access Module

Resolve role bindings and validate scope.

```
POST /api/tenancy/v1/access/resolve
Body:
{
  "userId": "u_123",
  "tenantId": "t_7f3c2a",
  "env": "prod",
  "scopes": ["read:data", "write:jobs"]
}
```
Response
```
{
  "allowed": true,
  "roles": ["tenant-admin"],
  "expiresAt": "2025-10-08T17:30:00Z"
}
```

### 9.2 Commercial Ops

Report usage signals and request plan validation.

```
POST /api/tenancy/v1/billing/usage
Body:
{
  "tenantId": "t_7f3c2a",
  "env": "prod",
  "resource": "storageGiBHours",
  "amount": 120.5,
  "timestamp": "2025-10-08T16:40:00Z"
}
```

Plan validation
```
POST /api/tenancy/v1/billing/validate
Body: { "tenantId": "t_7f3c2a", "action": "provision_environment", "params": { "name": "stage" } }
```

### 9.3 Governance

Emit audit events and fetch policy bindings.

```
POST /api/tenancy/v1/governance/events
Body:
{
  "eventType": "TENANCY_SUSPENDED",
  "tenantId": "t_7f3c2a",
  "actor": "system",
  "metadata": { "reason": "billing" },
  "occurredAt": "2025-10-08T16:45:00Z"
}
```

Fetch current policy bindings
```
GET /api/tenancy/v1/governance/policies?tenantId=t_7f3c2a&env=prod
```

### 9.4 Runtime and Orchestrator

Obtain execution context for job submission.

```
POST /api/tenancy/v1/runtime/context
Body: { "tenantId": "t_7f3c2a", "env": "prod", "workload": "pipeline_ingest" }
```

Response
```
{
  "queue": "jobs",
  "partitionKey": "t_7f3c2a",
  "concurrencyLimit": 5,
  "rateLimitPerSecond": 20
}
```

### 9.5 Schema Registry

Associate migration sets with tenant context.

```
POST /api/tenancy/v1/schema/migrations
Body: {
  "tenantId": "t_7f3c2a",
  "env": "prod",
  "appVersion": "2.3.0",
  "migrationSetId": "ms_9821"
}
```

---

## 10. Webhooks

Tenancy can call back to your service when lifecycle transitions occur.

### 10.1 Configure Webhook

```
POST /api/tenancy/v1/webhooks
Body:
{
  "url": "https://ops.example.com/hooks/tenancy",
  "events": ["TENANCY_ACTIVATED", "TENANCY_SUSPENDED", "TENANCY_RESUMED", "TENANCY_ARCHIVED", "TENANCY_DELETED"],
  "secret": "whsec_...",
  "retryPolicy": { "maxRetries": 8, "backoffSeconds": 30 }
}
```

Webhook delivery payload
```
{
  "id": "evt_78a2",
  "type": "TENANCY_ACTIVATED",
  "tenantId": "t_7f3c2a",
  "env": "prod",
  "timestamp": "2025-10-08T16:50:00Z",
  "data": { "profile": "mt-standard" },
  "signatures": ["t=...,v1=..."]
}
```

Verification  
- Compute HMAC SHA256 over the raw body using the configured secret.  
- Compare the signature with the v1 value.

---

## 11. Event Stream Contracts

Topic name examples  
- tenancy.events.v1.lifecycle  
- tenancy.events.v1.policy  
- tenancy.events.v1.usage

Lifecycle event example
```
{
  "type": "TENANCY_SUSPENDED",
  "tenantId": "t_7f3c2a",
  "env": "prod",
  "reason": "billing",
  "actor": "system",
  "occurredAt": "2025-10-08T16:55:00Z",
  "correlationId": "3b1a2d..."
}
```

---

## 12. Error Model

Tenancy uses a Problem Details style payload.

```
HTTP 409
Content-Type: application/problem+json

{
  "type": "https://errors.example.com/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "Tenant already exists with different attributes for this request id",
  "instance": "/api/tenancy/v1/tenants/t_7f3c2a",
  "correlationId": "3b1a2d...",
  "errors": [
    { "field": "profile", "message": "cannot change profile during draft" }
  ]
}
```

Common error codes  
- 400 invalid input  
- 401 unauthorized  
- 403 forbidden  
- 404 not found  
- 409 conflict  
- 422 unprocessable entity  
- 429 too many requests  
- 500 internal error  
- 503 service unavailable

---

## 13. Pagination

List endpoints accept `limit` and `cursor`. The response includes `nextCursor` when there are more items.

```
GET /api/tenancy/v1/tenants?limit=100&cursor=eyJwYWdlIjoxfQ==
```

Response
```
{
  "items": [ ... ],
  "nextCursor": "eyJwYWdlIjoyfQ=="
}
```

---

## 14. Security Notes

- All APIs require TLS.  
- Access tokens are short lived and audience scoped.  
- Every call is logged with tenant id, environment, and request id.  
- Sensitive fields are redacted in logs.  
- Rate limits and quotas are enforced per tenant.

---

## 15. Examples

Create and activate a tenant

```
curl -X POST https://api.example.com/api/tenancy/v1/tenants   -H "Authorization: Bearer $TOKEN"   -H "X-Request-Id: $(uuidgen)"   -H "Content-Type: application/json"   -d '{
    "tenantId":"t_7f3c2a",
    "organizationId":"org_acme",
    "profile":"mt-standard",
    "environments":["prod"],
    "quotas":{"storageGiB":200,"concurrentJobs":5},
    "policies":{"dataResidency":"in-region-only","encryption":"kms-per-tenant"}
  }'
```

```
curl -X POST https://api.example.com/api/tenancy/v1/tenants/t_7f3c2a:activate   -H "Authorization: Bearer $TOKEN"   -H "X-Request-Id: $(uuidgen)"
```

Fetch topology
```
curl -s https://api.example.com/api/tenancy/v1/tenants/t_7f3c2a/topology?env=prod   -H "Authorization: Bearer $TOKEN"
```

---

Summary  
These APIs provide a clear and stable contract for creating, operating, and integrating with tenant scoped resources. Internal controllers and external services use the same identifiers and headers, which simplifies debugging and supports consistent governance and billing.
