
# Anomaly Detection Module — Examples

Audience: Platform integrators, tenant admins, analysts  
Status: Version 1.0  
Purpose: Provide copy ready examples that demonstrate rule definition, activation, evaluation, retrieval, notification routing, tuning, and replay. Each example is self contained and references the APIs and data models defined in this module.

---

## Example 1. Create and activate a daily revenue dip rule

### Rule manifest

```yaml
apiVersion: anomaly.v1
kind: Rule
metadata:
  ruleId: revenue_dip_daily
  tenantId: t_23fd
spec:
  target: kpi_sales
  metric: daily_revenue
  baseline: mean(trailing=7)
  predicate: (baseline - current) / baseline > 0.15
  severity: high
  actions:
    - type: alert
      channel: email
      recipients: [finance-team@tenant.com]
```

### Upsert rule

```bash
curl -X PUT https://api.example.com/api/v1/anomaly/rules/revenue_dip_daily   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "X-Request-Id: $REQ"   -H "Content-Type: application/json"   -d '{
    "metadata":{"ruleId":"revenue_dip_daily"},
    "spec":{
      "target":"kpi_sales",
      "metric":"daily_revenue",
      "baseline":"mean(trailing=7)",
      "predicate":"(baseline - current) / baseline > 0.15",
      "severity":"high",
      "actions":[{"type":"alert","channel":"email","recipients":["finance-team@tenant.com"]}]
    }
  }'
```

### Activate rule

```bash
curl -X PATCH https://api.example.com/api/v1/anomaly/rules/revenue_dip_daily/status   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{"status":"active"}'
```

---

## Example 2. Event driven evaluation after KPI refresh

The pipeline publishes a refresh event for the table `kpi_sales_daily`. The control plane converts the event into a per tenant evaluation job.

### Trigger context

```json
{
  "table": "kpi_sales_daily",
  "tenantId": "t_23fd",
  "window": {"from": "2025-09-01", "to": "2025-09-30"},
  "correlationId": "c-9d21"
}
```

### Job acceptance response

```json
{
  "jobId": "job-7b12",
  "accepted": true,
  "estimated": {"rules": 1, "slices": 30}
}
```

### Retrieve job status

```bash
curl -s https://api.example.com/api/v1/anomaly/evaluate/jobs/job-7b12   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod"
```

Possible response

```json
{
  "jobId": "job-7b12",
  "state": "completed",
  "startedAt": "2025-10-09T10:15:00Z",
  "completedAt": "2025-10-09T10:15:18Z",
  "counters": {"evaluated": 30, "matches": 2, "errors": 0}
}
```

---

## Example 3. Query anomalies for a metric and resolve one

### List anomalies

```bash
curl -s "https://api.example.com/api/v1/anomaly/events?metric=daily_revenue&severity=high&from=2025-09-01&to=2025-10-01&page=1&pageSize=50"   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod"
```

Sample response

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

### Resolve an event

```bash
curl -X PATCH https://api.example.com/api/v1/anomaly/events/ae-9c31/status   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{"status":"resolved","note":"Explained by regional promotion timing"}'
```

---

## Example 4. Configure notification routes and test delivery

### Configure

```bash
curl -X PUT https://api.example.com/api/v1/anomaly/notifications   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{
    "routes":[
      {"severity":"high","channel":"webhook","endpoint":"https://ops.tenant.com/hooks/anomaly"},
      {"severity":"medium","channel":"email","recipients":["analytics@tenant.com"]}
    ]
  }'
```

### Webhook payload example

```json
{
  "schema": "anomaly.webhook.v1",
  "tenantId": "t_23fd",
  "eventId": "ae-9c31",
  "ruleId": "revenue_dip_daily",
  "metric": "daily_revenue",
  "severity": "high",
  "payload": {"current": 120010.0, "baseline": 152430.5, "deviationPct": -0.2123},
  "createdAt": "2025-09-15T23:59:59Z",
  "signature": "v1=hex"
}
```

---

## Example 5. Tune a noisy rule

A tenant observes frequent false positives for a seasonal metric. The fix increases the baseline window and adds a minimum volume guard.

### Updated rule manifest

```yaml
apiVersion: anomaly.v1
kind: Rule
metadata:
  ruleId: seasonal_revenue_stability
  tenantId: t_23fd
spec:
  target: kpi_sales
  metric: daily_revenue
  baseline: median(trailing=30)
  predicate: (abs(current - baseline) / max(0.0001, baseline) > 0.2) and (volume >= 1000)
  severity: medium
  actions:
    - type: alert
      channel: webhook
      endpoint: https://ops.tenant.com/hooks/anomaly
```

### Upsert and activate

```bash
curl -X PUT https://api.example.com/api/v1/anomaly/rules/seasonal_revenue_stability   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{"metadata":{"ruleId":"seasonal_revenue_stability"},"spec":{"target":"kpi_sales","metric":"daily_revenue","baseline":"median(trailing=30)","predicate":"(abs(current - baseline) / max(0.0001, baseline) > 0.2) and (volume >= 1000)","severity":"medium","actions":[{"type":"alert","channel":"webhook","endpoint":"https://ops.tenant.com/hooks/anomaly"}]}}'

curl -X PATCH https://api.example.com/api/v1/anomaly/rules/seasonal_revenue_stability/status   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{"status":"active"}'
```

---

## Example 6. Manual replay for a window

Used after a pipeline correction or backfill. Replays are idempotent when using the same request id and window keys.

```bash
curl -X POST https://api.example.com/api/v1/anomaly/evaluate   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "X-Request-Id: $REQ"   -H "Content-Type: application/json"   -d '{"rules":["revenue_dip_daily","seasonal_revenue_stability"],"window":{"from":"2025-09-01","to":"2025-09-30"},"replay":true}'
```

Monitor job as in Example 2, then query anomalies for the window.

---

## Example 7. Export anomalies for audit

```bash
curl -X POST https://api.example.com/api/v1/anomaly/events:export   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{"format":"csv","from":"2025-09-01","to":"2025-10-01","filters":{"severity":["high","critical"]}}'
```

Response returns a signed URL. Download within the expiry window.

---

## Example 8. Correlation rule for margin pressure

A rule that flags days when revenue rises while gross margin falls, which may indicate discount leakage or cost shocks.

```yaml
apiVersion: anomaly.v1
kind: Rule
metadata:
  ruleId: margin_pressure_daily
  tenantId: t_23fd
spec:
  target: kpi_financials
  metric: gross_margin_percent
  baseline: median(trailing=14)
  predicate: (revenue_delta > 0) and (gross_margin_percent_delta < 0) and (abs(gross_margin_percent_delta) > 0.03)
  severity: high
  actions:
    - type: alert
      channel: email
      recipients: ["cfo-office@tenant.com"]
```

Activate as shown earlier and verify anomalies appear with both revenue and margin context captured in event attributes.

---

## Example 9. Completeness rule for missing reconciliations

Detect missing daily payment reconciliations.

```yaml
apiVersion: anomaly.v1
kind: Rule
metadata:
  ruleId: missing_payment_recon
  tenantId: t_23fd
spec:
  target: kpi_finance_ops
  metric: payment_reconciliation_count
  baseline: previous_period
  predicate: current == 0
  severity: critical
  actions:
    - type: workflow
      workflowId: wf_open_incident_finance_ops
```

After activation, a day with no reconciliation produces a critical anomaly that opens a workflow ticket.

---

## Example 10. Webhook verification and replay

### Verify destination

```bash
curl -si https://ops.tenant.com/health
```

### Rotate secret and test

```bash
curl -X PUT https://api.example.com/api/v1/anomaly/notifications   -H "Authorization: Bearer $TOKEN"   -H "X-Tenant-Id: t_23fd" -H "X-Env: prod" -H "Content-Type: application/json"   -d '{"routes":[{"severity":"high","channel":"webhook","endpoint":"https://ops.tenant.com/hooks/anomaly"}]}'
```

Requeue deliveries through the admin endpoint if needed.

---

## Summary

These examples show rule lifecycle, evaluation, retrieval, routing, tuning, and replay. Use them as templates for tenant onboarding and automation. All examples assume authenticated calls with tenant scoped headers and follow idempotent patterns for safe retries.
