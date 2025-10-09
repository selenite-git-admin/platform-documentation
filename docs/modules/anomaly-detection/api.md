
# Anomaly Detection Module — API

Audience: Platform integrators, tenant application developers, DevOps  
Status: Version 1.0  
Purpose: Define the tenant scoped, integration facing APIs for rule management, evaluation control, anomaly retrieval, notifications, and system administration. All endpoints are stable, idempotent where indicated, and designed for programmatic automation.

---

## Conventions

Base path  
`/api/v1/anomaly`

Authentication and scope  
- JWT or service token issued by Access module  
- Required headers:  
  - `Authorization: Bearer <token>`  
  - `X-Tenant-Id: <tenant_id>`  
  - `X-Env: <env>` such as dev, staging, prod  
  - `X-Request-Id: <uuid>` for idempotency and tracing

Content types  
- `application/json` for requests and responses  
- `application/yaml` accepted for rule and configuration manifests

Pagination  
- `page`, `pageSize` query parameters  
- `nextPageToken` supported for high volume listings

Filtering  
- Standard filter syntax `?filter=field1==value1;field2~substr`  
- Time windows use `from` and `to` in ISO 8601

Rate limits  
- Default per tenant limits apply to write endpoints  
- 429 is returned when limits are exceeded along with a retry header

Idempotency  
- POST operations accept `X-Request-Id` and deduplicate retries within 24 hours

Error model  
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "baseline window must be between 3 and 12",
    "traceId": "c-8a9e"
  }
}
```

---

## Rules

### Create or update a rule

`PUT /api/v1/anomaly/rules/{ruleId}`

Idempotent upsert of a rule specification. The server validates schema, dependencies, and constraints.

Request
```json
{
  "metadata": {
    "ruleId": "revenue_dip_daily"
  },
  "spec": {
    "target": "kpi_sales",
    "metric": "daily_revenue",
    "baseline": "mean(trailing=7)",
    "predicate": "(baseline - current) / baseline > 0.15",
    "severity": "medium",
    "actions": [
      {"type": "alert", "channel": "email", "recipients": ["finance-team@tenant.com"]},
      {"type": "workflow", "workflowId": "wf_revenue_check"}
    ]
  }
}
```

Response
```json
{
  "ruleId": "revenue_dip_daily",
  "status": "validated",
  "version": "2.1.0",
  "updatedAt": "2025-10-09T10:12:00Z"
}
```

### Get a rule

`GET /api/v1/anomaly/rules/{ruleId}`

### List rules

`GET /api/v1/anomaly/rules?pack=finance-defaults&status=active&page=1&pageSize=50`

### Change rule status

`PATCH /api/v1/anomaly/rules/{ruleId}/status`

Request
```json
{"status": "active"}
```

Response
```json
{"ruleId": "revenue_dip_daily", "status": "active"}
```

### Delete or archive a rule

`DELETE /api/v1/anomaly/rules/{ruleId}?mode=archive`

Soft delete by default. Use `mode=hard` only for test environments.

---

## Rule packs

### Attach or detach a rule pack

`POST /api/v1/anomaly/rule-packs/{packName}:attach`  
`POST /api/v1/anomaly/rule-packs/{packName}:detach`

### List available rule packs

`GET /api/v1/anomaly/rule-packs`

Returns names, versions, and descriptions. Packs are namespaced to avoid collisions.

---

## Evaluation control

### Trigger evaluation for a window

`POST /api/v1/anomaly/evaluate`

Runs rules for a specific time window or triggers an immediate evaluation of the latest refresh. This endpoint is idempotent with respect to `X-Request-Id` and the requested window.

Request
```json
{
  "rules": ["revenue_dip_daily", "gross_margin_drift"],
  "window": {"from": "2025-09-01", "to": "2025-09-30"},
  "replay": false
}
```

Response
```json
{
  "jobId": "job-7b12",
  "accepted": true,
  "estimated": {"rules": 2, "slices": 30}
}
```

### Get evaluation job status

`GET /api/v1/anomaly/evaluate/jobs/{jobId}`

Response
```json
{
  "jobId": "job-7b12",
  "state": "completed",
  "startedAt": "2025-10-09T10:15:00Z",
  "completedAt": "2025-10-09T10:15:18Z",
  "counters": {"evaluated": 60, "matches": 3, "errors": 0}
}
```

### List evaluation jobs

`GET /api/v1/anomaly/evaluate/jobs?state=completed&from=2025-09-01&to=2025-10-01&page=1`

---

## Anomaly retrieval

### Query anomalies

`GET /api/v1/anomaly/events?metric=daily_revenue&severity=high&from=2025-09-01&to=2025-10-01&page=1&pageSize=100`

Response
```json
{
  "items": [
    {
      "eventId": "ae-9c31",
      "ruleId": "revenue_dip_daily",
      "metric": "daily_revenue",
      "period": "2025-09-15",
      "baseline": {"fn": "mean", "window": 7, "value": 152430.50},
      "current": 120010.00,
      "deviationPct": -0.2123,
      "severity": "high",
      "sourceTable": "kpi_sales_daily",
      "createdAt": "2025-09-15T23:59:59Z",
      "status": "open"
    }
  ],
  "nextPageToken": null
}
```

### Get a specific anomaly

`GET /api/v1/anomaly/events/{eventId}`

### Update anomaly status

`PATCH /api/v1/anomaly/events/{eventId}/status`

Request
```json
{"status": "resolved", "note": "Confirmed drop due to planned price experiment"}
```

Response
```json
{"eventId": "ae-9c31", "status": "resolved", "updatedAt": "2025-10-09T11:00:12Z"}
```

### Export anomalies

`POST /api/v1/anomaly/events:export`

Request
```json
{"format": "csv", "from": "2025-09-01", "to": "2025-10-01", "filters": {"severity": ["high","critical"]}}
```

Response returns a signed URL with limited lifetime.

---

## Notifications and webhooks

### Configure routes

`PUT /api/v1/anomaly/notifications`

Request
```json
{
  "routes": [
    {"severity": "high", "channel": "webhook", "endpoint": "https://ops.tenant.com/hooks/anomaly"},
    {"severity": "medium", "channel": "email", "recipients": ["analytics@tenant.com"]}
  ]
}
```

### Webhook delivery format

```json
{
  "schema": "anomaly.webhook.v1",
  "tenantId": "t_23fd",
  "eventId": "ae-9c31",
  "ruleId": "revenue_dip_daily",
  "metric": "daily_revenue",
  "severity": "high",
  "payload": { "current": 120010.0, "baseline": 152430.5, "deviationPct": -0.2123 },
  "createdAt": "2025-09-15T23:59:59Z",
  "signature": "v1=hex"
}
```

Webhook security  
- HTTPS only  
- HMAC signatures with shared secret  
- Retries with exponential backoff and dead letter queue

---

## Configuration APIs

For full configuration details see configuration.md. Primary endpoints relevant to integrations are listed here.

- `GET /api/v1/anomaly/config` read current tenant configuration  
- `PUT /api/v1/anomaly/config` replace configuration manifest  
- `GET /api/v1/anomaly/system` read global controls for platform admins

---

## Admin and system APIs

These endpoints require platform admin roles and are not available to tenant users by default.

- `GET /api/v1/anomaly/system/quotas` read platform quotas  
- `PUT /api/v1/anomaly/system/quotas` update quotas  
- `GET /api/v1/anomaly/system/scheduler` read scheduler defaults  
- `PUT /api/v1/anomaly/system/scheduler` update scheduler defaults  
- `POST /api/v1/anomaly/system/jobs:requeue` requeue failed jobs across tenants with filters

Requests must include admin JWT scopes and will be audited.

---

## SDK considerations

- Generated clients should wrap idempotent `X-Request-Id` handling  
- Paging helpers should surface `nextPageToken`  
- Retries should be safe for idempotent endpoints only  
- Strong typing for `baseline` and `predicate` expressions is recommended

---

## Examples

### Example 1. Create a threshold rule and activate it

1. Upsert rule  
`PUT /api/v1/anomaly/rules/revenue_dip_daily`  
2. Activate rule  
`PATCH /api/v1/anomaly/rules/revenue_dip_daily/status` with `{"status":"active"}`  
3. Evaluate window for September  
`POST /api/v1/anomaly/evaluate` with body `{"rules":["revenue_dip_daily"],"window":{"from":"2025-09-01","to":"2025-09-30"}}`

### Example 2. Query and resolve anomalies

1. Query events  
`GET /api/v1/anomaly/events?metric=daily_revenue&severity=high&from=2025-09-01&to=2025-10-01`  
2. Resolve one event  
`PATCH /api/v1/anomaly/events/ae-9c31/status` with `{"status":"resolved","note":"explained by promotion timing"}`

---

## Compatibility and versioning

- The API follows semantic versioning at the path level.  
- Non breaking additions include new fields and resources.  
- Breaking changes require a new major version path.

---

## Security summary

- All endpoints require authentication and tenant scoping.  
- Least privilege is enforced through Access roles.  
- Events and exports are signed and time bound.  
- All operations are audited with actor, action, request id, and timestamp.
