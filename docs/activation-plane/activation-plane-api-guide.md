# Activation Plane — API Guide

## Purpose
The APIs expose the capabilities of the Activation Plane in a consistent, governed, and auditable way.

## Categories

1. **Data APIs**  
   - Read governed KPI/GDP datasets.  
   - Enforce row-level security, column masking, quotas.  
   - Example:  
     ```
     GET /api/v1/data/kpi/ar_overdue?filter=days_overdue>90
     ```

2. **Action APIs**  
   - Trigger governed actions (notify, create_task, export, webhook).  
   - Require role-based scopes (`action.trigger`).  
   - Example:  
     ```
     POST /api/v1/action/create_task
     {
       "reason": "AR >90d",
       "targets": [{ "system": "salesforce", "object": "Task" }]
     }
     ```

3. **AI Activation APIs**  
   - Invoke approved, tenant-enabled models for forecasting, anomaly detection, recommendations.  
   - Example:  
     ```
     POST /api/v1/ai/liquidity_forecast:predict
     {
       "inputs": [{ "cash_on_hand": 1500000, "payables": 780000 }]
     }
     ```

## Authentication & Authorization
- OAuth2 (JWT) with tenant-scoped tokens.  
- Scopes: `data.read`, `action.trigger`, `ai.invoke`.  
- Service principals supported for M2M integrations.  
- Policies enforce least privilege by default.

## Governance Controls
- **Rate limits** and **quotas** per tenant and endpoint.  
- **Egress allow-lists**: actions only to approved systems.  
- **Idempotency**: required header `Idempotency-Key` for all action POSTs.  
- **Audit trail**: correlation id + KPI reference logged with every call.  

## Versioning & Deprecation
- Semantic versioning via base path (`/api/v1`).  
- Additive changes allowed in minor releases.  
- Breaking changes → `/api/v2` with 180-day deprecation window.  

## Error Model
Uniform envelope:  
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Tenant limit exceeded for action.trigger",
    "correlation_id": "b6f1f1a8-...",
    "details": { "limit": "100/day", "reset_at": "2025-09-19T00:00:00Z" }
  }
}
```

## Webhooks & Events
- **KPI Breach** (`kpi.breach`)  
- **DQ Failure** (`dq.failed`)  
- **Action Result** (`action.succeeded|failed`)  
- **Quota/Rate** (`quota.near_limit`, `rate.limit_exceeded`)  

Delivery: retries with backoff, signatures for verification, dead-letter replay.

## Examples

**Trigger overdue AR escalation**  
```
POST /api/v1/action/create_task
Authorization: Bearer <token>
Idempotency-Key: 7c1a...
{
  "reason": "AR >90d spike",
  "targets": [{ "system": "salesforce", "object": "Task" }]
}
```

**Run liquidity forecast**  
```
POST /api/v1/ai/liquidity_forecast:predict
Authorization: Bearer <token>
{
  "inputs": [{ "cash_on_hand": 1500000, "receivables": 950000, "payables": 780000 }]
}
```
