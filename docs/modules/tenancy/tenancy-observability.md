# Tenancy Module Observability

**Audience:** SRE, platform operations, and service owners  
**Status:** Working draft  
**Purpose:** Define how the tenancy control plane and related subsystems emit metrics, logs, and traces, how alerts are evaluated, and how dashboards are constructed. The objective is fast incident detection, precise triage, and complete auditability. This document is self contained and uses the same model for all environments and regions.

## Scope

Observability covers controllers, orchestrators, registry APIs, webhook dispatchers, and policy evaluation calls. Signals are emitted for request handling, reconcile loops, queue operations, webhook delivery, policy checks, lifecycle workflows, quota enforcement, and migration or failover steps.

## Metrics

**Controller metrics**
- reconcile_duration_ms histogram with controller and region dimensions
- reconcile_success_total and reconcile_failure_total counters
- queue_depth gauge and dequeue_rate_per_sec gauge
- backoff_attempts_total counter and max_backoff_seconds gauge
- idempotent_replays_total counter

**Webhook metrics**
- webhook_delivery_latency_ms histogram
- webhook_failures_total counter by status class
- webhook_retries_total counter with retry_count dimension
- webhook_dlq_inserts_total counter and dlq_backlog gauge

**Policy metrics**
- policy_eval_latency_ms histogram
- policy_eval_errors_total counter
- residency_denied_total counter by region

**API metrics**
- http_request_duration_ms histogram by route and method
- http_requests_total and http_errors_total counters
- rate_limited_total counter and retry_after_seconds gauge

**Workflow metrics**
- lifecycle_job_latency_ms histogram
- lifecycle_job_failures_total counter
- migration_step_latency_ms histogram and cutover_window_seconds gauge

## Logs

**Structure**
- JSON lines with timestamp, level, tenantId, region, controller, requestId, correlationId, manifestVersion, and action
- Payload size is bounded and fields are consistent across services

**Content rules**
- No secrets in logs
- Error logs include error category, error code, and remediation hint
- Every lifecycle transition writes a before state and after state summary with identifiers only

**Correlation**
- X-Request-Id is echoed and logged on every hop
- X-Correlation-Id ties together controller, webhook, and policy calls

## Traces

**Propagation**
- Trace context headers are forwarded through API gateway, controllers, policy service, and webhook dispatchers

**Spans**
- Controller reconcile span with child spans for registry read, policy check, provisioning call, and webhook enqueue
- Webhook delivery span with DNS, connect, TLS, request, and response child spans
- Policy evaluation span with cache lookup and remote evaluation child spans

## Dashboards

**Controller health**
- Reconcile duration p50, p95, p99
- Queue depth and dequeue rate
- Failure rate and top error categories

**Webhook delivery**
- Delivery latency percentile chart
- Failures by status class and endpoint
- DLQ backlog and requeue rate

**Policy evaluation**
- Latency distribution and error rate
- Residency denials by region and plan code

**API health**
- Request rate, error rate, and rate limit hits
- ETag cache hit ratio

**Lifecycle jobs**
- Activation and migration latency distributions
- Running jobs and failed jobs by step

## Alerts

**Controller alerts**
- Reconcile failure rate above 2 percent for five minutes
- Queue depth above threshold for ten minutes
- Backoff attempts above threshold per tenant

**Webhook alerts**
- Delivery failure rate above 1 percent for five minutes
- DLQ backlog growth for fifteen minutes
- Requeue failure rate above threshold

**Policy alerts**
- Policy evaluation latency above 200 ms p95
- Policy evaluation errors above baseline

**API alerts**
- 5xx error rate above baseline
- Rate limited total spikes without correlated traffic increase

**Lifecycle alerts**
- Activation job latency above threshold
- Migration cutover window exceeded

Every alert includes a runbook link and the primary diagnostic queries.

## SLOs

**Availability and latency**
- API availability target 99.95 percent per region
- GET p95 under 150 ms, POST p95 under 300 ms at steady state
- Controller reconcile p95 under 3 seconds for steady state, under 30 seconds during spikes
- Webhook delivery p95 under 2 seconds

**Freshness and backlog**
- Controller queue p95 under 2000 items
- DLQ backlog drained within 1 hour for normal load

SLOs are measured per region and per tenant where applicable. Violations trigger error budget policies and change freezes.

## Retention And Sampling

**Metrics**
- High cardinality metrics are sampled or downsampled after 7 days
- Aggregates retained for 90 days

**Logs**
- Error logs retained for 180 days
- Info logs retained for 30 days with sampling at 0.3

**Traces**
- Head sampling at 10 percent baseline
- Tail sampling on error categories and slow spans

## Runbook Pointers

**Diagnostics**
- Recent reconciles for tenant id with failure category histogram
- Webhook retry heatmap by endpoint
- Policy evaluation latency over time with error overlay
- Queue depth trend with dequeue rate

**Common remediations**
- Requeue webhooks by sequence range
- Increase controller concurrency temporarily with admin override and audit
- Clear poisoned messages from DLQ after root cause is fixed
- Apply residency override only with governance approval and audit

## Emission And Naming Conventions

**Metric naming**
- Use snake case and subsystem prefixes such as tenancy_controller and tenancy_webhook
- Include dimensions tenantId, region, controller, endpoint where possible

**Log fields**
- Use fixed field names and types to simplify queries
- Record manifestVersion for all reconcile operations

**Trace attributes**
- service.name, tenant.id, region, controller.name, webhook.endpoint, policy.rule set

## Data Privacy And Compliance

**Redaction**
- PII is not logged
- Tenant display names are hashed in logs when policy requires it

**Access**
- Observability stores are scoped by role
- Break glass procedures are time bound and audited