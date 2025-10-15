# Ticketing Observability

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Provide visibility into request rates, write success, deduplication, routing, SLA timers, and webhook delivery for the Ticketing service. Covers metrics, logs, traces, dashboards, alerts, and retention for Lambda plus API Gateway deployments. **Platform‑scoped** with optional tenant‑level slices where safe.

## Design principles
- Every write and state transition is observable
- Idempotency, routing, and SLA behavior are first‑class signals
- Tenant slices are optional and capped to avoid metric cardinality blowups
- Lightweight payloads that align with the API and data model

## Metrics
Default labels: `service_name=ticketing`, `environment`, `region`. Avoid high‑cardinality labels; expose `tenant_bucket` only for top N tenants and aggregate the rest under `other`.

| Metric | Type | Description |
|---|---|---|
| `ticket_create_requests_total` | counter | HTTP create attempts |
| `ticket_create_success_total` | counter | Created or idempotent ok |
| `ticket_create_dedup_total` | counter | Requests matched by idempotency key |
| `ticket_update_requests_total` | counter | HTTP patch attempts |
| `ticket_update_success_total` | counter | Successful updates |
| `ticket_search_requests_total` | counter | Searches performed |
| `ticket_write_latency_ms` | histogram | End‑to‑end write latency |
| `ticket_search_latency_ms` | histogram | Search latency |
| `ticket_open_gauge` | gauge | Open tickets by state and category |
| `ticket_sla_due_gauge` | gauge | Tickets due within time buckets |
| `ticket_sla_breach_total` | counter | SLA breaches by kind |
| `ticket_assignment_changes_total` | counter | Owner or team changes |
| `ticket_comment_added_total` | counter | Comments added |
| `ticket_webhook_out_total` | counter | Outbound webhook deliveries |
| `ticket_webhook_out_fail_total` | counter | Failed webhook attempts |
| `ticket_webhook_latency_ms` | histogram | Webhook delivery latency |
| `ticket_inbound_hook_total` | counter | Inbound email or webhook events |
| `ticket_inbound_hook_fail_total` | counter | Inbound failures |
| `ticket_db_errors_total` | counter | Database write or read errors |
| `ticket_queue_backlog_gauge` | gauge | Background job backlog size |
| `ticket_dedup_group_open_gauge` | gauge | Open dedup groups |

Cardinality guardrails
- Do **not** label metrics with raw `tenant_id`. Use `tenant_bucket` or omit.
- Limit `tags` and `subcategory` labels to curated sets.

## Logging
Structured JSON logs with safe fields only. `tenant_id` included only when present and needed.

Log events
- ticket.created, ticket.updated, ticket.assigned, ticket.state_changed, ticket.comment_added
- ticket.webhook.delivered, ticket.webhook.failed
- ticket.inbound.received, ticket.inbound.rejected

Sampling
- Log all failures
- Sample successful writes at 10 percent
- Sample searches at 1 percent

## Tracing
OpenTelemetry spans for `ticket.create`, `ticket.update`, `ticket.search`, `ticket.webhook.deliver`, `ticket.inbound.consume` with child DB and IO spans. Always sample failures; sample 5 percent of successful writes.

## Dashboards
Overview
- Create/update rates, success ratios
- P95 write/search latency
- Open tickets by state and category
- SLA due buckets and breach counts
- Webhook failures and retries
- DB error rate and Lambda errors
- Queue backlog

Tenant slices
- Top tenants by create volume and open backlog (bucketed)
- Breaches by tenant bucket

## Alerts
- Create error ratio > 1 percent for 5 minutes → investigate DB, throttling, auth
- P95 write latency > 500 ms for 10 minutes → check DB saturation/cold starts
- SLA breach spikes > threshold → page on‑call
- Webhook failures per target > 5 percent → quarantine and retry
- Backlog > 1000 for 10 minutes → scale workers
- Dedup rate drops to zero while incidents arrive → check idempotency store

## Retention
- Metrics hot 30 days and cold 6 months
- Logs 30 days with failure extracts archived 90 days
- Traces 7 days; failure traces 30 days
- History tables retained 24 months

## Summary
Observability is platform‑wide, with careful use of tenant slices to stay cost‑efficient and actionable.