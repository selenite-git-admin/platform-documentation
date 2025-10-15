# Notifications Observability

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Observability for the Notifications module provides transparent insight into message lifecycle, delivery performance, failures, and provider health. It enables operators to detect delivery degradation, ensure idempotent behavior, and trace every request from API submission to channel-level outcome.

The goal is **zero-blind spots** across notification flows: API → Queue → Channel Adapter → Provider → Callback → Evidence Ledger.

## Design Principles
- **End-to-End Correlation:** Every notification request carries a `correlation_id` and `idempotency_key` visible in logs, traces, and metrics.
- **Channel Isolation:** Each channel (email, Slack, webhook, in-app) exposes metrics independently.
- **Delivery Accountability:** Each channel attempt must produce auditable outcomes (delivered, failed, retried, bounced).
- **Cost-Aware Observability:** Metrics and logs are compact, high signal-to-noise, optimized for 30-day retention in hot storage.
- **Tenant Partitioning:** Logs and dashboards are tenant-aware; no cross-tenant visibility.

---

## Metrics

All metrics are emitted via a standard library wrapper to the platform metric service (Prometheus or CloudWatch). Labels: `tenant_id`, `channel`, `template_id`, `region`.

| Metric | Type | Description |
|---|---|---|
| `notifications_submitted_total` | counter | Total notifications submitted by API |
| `notifications_attempts_total` | counter | Fan-out attempts (per channel) |
| `notifications_delivered_total` | counter | Successful deliveries per channel |
| `notifications_failed_total` | counter | Failed attempts per channel |
| `notifications_bounced_total` | counter | Provider bounces (email only) |
| `notifications_latency_seconds` | histogram | Time from enqueue → delivered |
| `notifications_retry_count` | histogram | Distribution of retry attempts |
| `notifications_queue_depth` | gauge | Messages pending in queue |
| `notifications_provider_latency_seconds` | histogram | Provider round-trip latency |
| `notifications_template_errors_total` | counter | Variable or schema validation failures |
| `notifications_suppression_hits_total` | counter | Suppressed sends due to opt-out or bounce |
| `notifications_rate_limited_total` | counter | Requests rejected due to rate limits |

### Example Prometheus snippets

```promql
# Delivery success ratio per channel
(sum(rate(notifications_delivered_total[5m])) / sum(rate(notifications_attempts_total[5m]))) * 100

# Email bounce rate by tenant
sum(rate(notifications_bounced_total[15m])) by (tenant_id) / sum(rate(notifications_delivered_total[15m])) by (tenant_id)

# P95 latency
histogram_quantile(0.95, sum(rate(notifications_latency_seconds_bucket[5m])) by (le, channel))
```

SLO Targets:
- P95 end-to-end latency < 5s for in-app, < 10s for email/webhook.
- 99.5% delivery success (excluding bounces) per channel over 24h.
- <0.5% validation or suppression rejections per day.

---

## Logging

Structured JSON logs emitted at key stages:
- `request.accepted` – API layer received and validated request
- `request.persisted` – request written to DB and queued
- `attempt.started` – per-channel delivery attempt
- `attempt.completed` – delivery outcome, latency, and provider id
- `callback.received` – webhook or provider event callback
- `suppression.applied` – when message blocked by suppression rule
- `validation.failed` – invalid variable or template

### Common Fields
| Field | Example | Description |
|---|---|---|
| `timestamp` | 2025-10-13T10:33:01Z | UTC |
| `level` | info / error / warn / debug | Log severity |
| `service` | notifications | Service name |
| `module` | email-adapter | Subcomponent |
| `tenant_id` | 1b2f... | Tenant context |
| `correlation_id` | 01JC2Q0YQ9S0Y0K7Q2YJX8G7QK | Trace key |
| `request_id` | 0f0cb2f4-62e0-7a3b-8a11-b9c1d2b3e4f5 | Notification request |
| `channel` | email/slack/inapp/webhook | Channel |
| `event` | attempt.completed | Lifecycle event |
| `status` | delivered/failed | Outcome |
| `latency_ms` | 4213 | Duration |
| `error_code` | bounce / timeout | Canonical code |

### Log Routing
- Default: CloudWatch Logs or OpenSearch sink (retention 30d).
- Long-term evidence: subset forwarded to Evidence Ledger.
- Sensitive payloads redacted (`variables`, `to`, etc.).

---

## Tracing

OpenTelemetry spans capture the complete lifecycle per request.

**Root span:** `notifications.api.request`  
**Child spans:**
- `notifications.db.persist`
- `notifications.queue.enqueue`
- `notifications.delivery.<channel>`
- `notifications.provider.<adapter>`
- `notifications.callback.receive`

### Trace attributes
| Attribute | Example |
|---|---|
| `correlation_id` | 01JC2Q0YQ9S0Y0K7Q2YJX8G7QK |
| `tenant_id` | 1b2f... |
| `template_id` | password-reset |
| `channel` | email |
| `attempt_id` | 8a2b-... |
| `provider` | ses |
| `retry_count` | 1 |
| `status` | delivered |
| `latency_ms` | 4213 |

### Trace Sampling
- Default 10% per tenant; always sample errors and retries.
- Adaptive sampling raises rate during partial delivery or high latency.

---

## Dashboards

**Notification Overview (Ops):**
- Submissions per minute (by tenant, channel)
- Delivery success vs failure
- Queue depth trend
- Bounce and suppression trends
- P95 latency
- Rate-limited tenants

**Provider Health (Eng):**
- Provider latency by region
- Error rate by provider (SES, Slack, etc.)
- Retries and dead-letter queues
- Top templates by volume and error ratio

**Tenant Health (CSM):**
- Delivery success per tenant
- Daily active templates
- SLA compliance (delivery latency, success)

---

## Alerts

| Alert | Condition | Severity | Action |
|---|---|---|---|
| High failure rate | `>5% failures over 5m` | High | Auto‑page oncall |
| Provider latency spike | `P95 latency > 15s` | Medium | Notify #eng-notifications |
| Queue backlog | `queue_depth > 5000` | High | Scale runners or throttle ingestion |
| Bounce surge | `bounce rate > 3%` | Medium | Trigger suppression review |
| Rate limiting burst | `rate_limited_total > 1000` in 10m | Low | Audit abusive tenants |
| Missing callbacks | No callback within 2× expected latency | High | Provider outage or callback blocked |

All alerts fire via Notification API (self‑dogfooding) to on‑call Slack and email.

---

## Audit and Evidence Integration
- Every `attempt.completed` log creates an entry in Evidence Ledger.
- Provider callbacks (`bounce`, `delivery`, `complaint`) append immutable proofs.
- Key fields (`tenant_id`, `channel`, `template_id`, `status`) stored as GDP fields.

---

## Example Queries

**Recent failures for tenant**
```sql
select correlation_id, channel, status, last_error_code
from notification_attempt a
join notification_request r on r.id = a.request_id
where r.tenant_id = $1 and a.state = 'failed'
order by a.last_attempt_at desc
limit 20;
```

**Find long latency deliveries**
```sql
select a.channel, extract(epoch from a.delivered_at - a.first_attempt_at) as latency
from notification_attempt a
where a.delivered_at is not null
and a.delivered_at - a.first_attempt_at > interval '10 seconds'
order by latency desc limit 20;
```

---

## Integration with Platform Observability
- Unified Correlation: `X-Correlation-Id` propagates through API Gateway → Lambda → Queue → Channel Adapter.
- Shared Error Taxonomy: reuses canonical codes from Error Handling module.
- DRR Interaction: delivery completion triggers dataset freshness check updates (optional for KPI alerts).

---

## Retention and Storage
- Metrics: 30d in hot store, 6m in cold.
- Logs: 30d retention; Evidence subset archived to Ledger.
- Traces: 7d retention (error traces kept 30d).

---

## Summary
Notifications Observability delivers full visibility from submission to provider outcome. Each request is traceable, measurable, and accountable, with unified metrics, structured logs, and distributed tracing. It ensures delivery reliability, SLA compliance, and transparent operations across all channels.