
# Tenancy Module - Examples

Audience: Developers, QA, platform engineers  
Status: Draft v0.1  
Purpose: Demonstrates practical examples for common tenancy operations, configuration patterns, and integration use cases. Each example is self-contained and executable with minimal dependencies.

---

## 1. Creating a Tenant

### Example Request
```
POST /api/tenancy/v1/tenants
Body:
{
  "tenantId": "t_5001",
  "organizationId": "org_acme",
  "profile": "mt-standard",
  "environments": ["dev", "prod"],
  "quotas": { "storageGiB": 200, "concurrentJobs": 10 },
  "policies": { "dataResidency": "in-region-only", "encryption": "kms-per-tenant" },
  "billing": { "plan": "starter" }
}
```

### Example Response
```
HTTP 201 Created
{
  "id": "t_5001",
  "state": "Draft",
  "createdAt": "2025-10-08T14:32:00Z"
}
```

---

## 2. Activating a Tenant

### Example Request
```
POST /api/tenancy/v1/tenants/t_5001:activate
Headers: Authorization, X-Request-Id
```

### Example Response
```
HTTP 202 Accepted
{
  "jobId": "job_7001",
  "state": "Running",
  "links": { "self": "/api/tenancy/v1/jobs/job_7001" }
}
```

Polling the job status:
```
GET /api/tenancy/v1/jobs/job_7001
```

---

## 3. Listing Tenants

### Example Request
```
GET /api/tenancy/v1/tenants?org=org_acme&state=Active
```

### Example Response
```
{
  "items": [
    {
      "tenantId": "t_5001",
      "organizationId": "org_acme",
      "profile": "mt-standard",
      "state": "Active",
      "region": "ap-south-1"
    }
  ],
  "nextCursor": null
}
```

---

## 4. Fetching Topology Details

```
GET /api/tenancy/v1/tenants/t_5001/topology?env=prod
```

Example Response
```
{
  "profile": "mt-standard",
  "db": { "type": "postgres", "database": "warehouse.shared", "schema": "t_5001" },
  "objectStore": { "bucket": "data.shared", "prefix": "tenants/t_5001/prod" },
  "runtime": { "queue": "jobs", "partitionKey": "t_5001" }
}
```

---

## 5. Updating Tenant Profile

```
PATCH /api/tenancy/v1/tenants/t_5001
Body:
{
  "profile": "st-dedicated",
  "quotas": { "storageGiB": 500 }
}
```

Response
```
HTTP 200 OK
{
  "tenantId": "t_5001",
  "profile": "st-dedicated",
  "state": "Active"
}
```

---

## 6. Listing Environments

```
GET /api/tenancy/v1/tenants/t_5001/environments
```

Example Response
```
{
  "items": [
    {
      "name": "dev",
      "region": "ap-south-1",
      "quota": { "storageGiB": 50 }
    },
    {
      "name": "prod",
      "region": "ap-south-1",
      "quota": { "storageGiB": 150 }
    }
  ]
}
```

---

## 7. Setting Up a Webhook

```
POST /api/tenancy/v1/webhooks
Body:
{
  "url": "https://ops.example.com/hooks/tenancy",
  "events": ["TENANCY_ACTIVATED", "TENANCY_SUSPENDED"],
  "secret": "whsec_demo"
}
```

Webhook delivery sample
```
{
  "id": "evt_101",
  "type": "TENANCY_ACTIVATED",
  "tenantId": "t_5001",
  "timestamp": "2025-10-08T15:01:00Z",
  "data": { "profile": "mt-standard" }
}
```

---

## 8. Policy Binding Example

```
GET /api/tenancy/v1/governance/policies?tenantId=t_5001&env=prod
```

Response
```
{
  "policies": [
    {
      "name": "DataResidency",
      "rule": "in-region-only",
      "enforced": true
    },
    {
      "name": "Encryption",
      "rule": "kms-per-tenant",
      "enforced": true
    }
  ]
}
```

---

## 9. Usage Reporting Example

```
POST /api/tenancy/v1/billing/usage
Body:
{
  "tenantId": "t_5001",
  "env": "prod",
  "resource": "storageGiBHours",
  "amount": 100.2,
  "timestamp": "2025-10-08T15:20:00Z"
}
```

Response
```
HTTP 202 Accepted
{
  "accepted": true,
  "recordId": "usage_902"
}
```

---

## 10. Tenant Suspension Example

```
POST /api/tenancy/v1/tenants/t_5001:suspend
Body: { "reason": "billing" }
```

Response
```
{
  "jobId": "job_910",
  "state": "Running"
}
```

---

## 11. Event Stream Subscription Example

Lifecycle events are pushed to Kafka-compatible topics.

Sample message
```
{
  "type": "TENANCY_SUSPENDED",
  "tenantId": "t_5001",
  "reason": "billing",
  "timestamp": "2025-10-08T15:40:00Z"
}
```

Consumer code (Python)
```python
for msg in consumer:
    event = json.loads(msg.value)
    if event["type"] == "TENANCY_SUSPENDED":
        handle_suspend(event["tenantId"])
```

---

## 12. Tenant Deletion Example

```
DELETE /api/tenancy/v1/tenants/t_5001?force=false
```

Response
```
HTTP 202 Accepted
{
  "jobId": "job_1200",
  "state": "Queued"
}
```

---

## 13. MT to ST Migration Example

```
PATCH /api/tenancy/v1/tenants/t_5001
Body:
{
  "profile": "st-dedicated"
}
```

Response
```
{
  "jobId": "job_1801",
  "state": "Running",
  "message": "Migration in progress"
}
```

---

## 14. Fetching Job Status

```
GET /api/tenancy/v1/jobs/job_1801
```

Response
```
{
  "id": "job_1801",
  "state": "Completed",
  "progress": 1.0,
  "updatedAt": "2025-10-08T16:30:00Z"
}
```

---

Summary  
These examples represent operational patterns for the Tenancy module across creation, lifecycle management, policy enforcement, billing integration, and event handling. Developers can directly reuse these examples for testing or SDK generation.
