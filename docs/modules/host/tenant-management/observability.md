# Observability

## Scope
Observability for Tenant Management. This page defines metrics, logs, traces, dashboards, alerts, and SLOs for control plane operations.

## Metrics
- tm_tenants_total
  Counter. Labels: status. Purpose: count by lifecycle state.
- tm_lifecycle_transitions_total
  Counter. Labels: from, to. Purpose: transition volume and safety.
- tm_api_requests_total
  Counter. Labels: route, method, status. Purpose: API volume.
- tm_api_request_duration_ms
  Histogram. Labels: route, method, status. Purpose: latency.
- tm_write_errors_total
  Counter. Labels: route. Purpose: safety and alerting.

## Logs
Structured JSON. Event names
- tm.tenant.create
- tm.tenant.update
- tm.tenant.lifecycle
- tm.tenant.plan.put
- tm.tenant.residency.put
- tm.tenant.regions.put
- tm.tenant.contacts.put
- tm.tenant.external_ids.put
- tm.tenant.tags.put

## Traces
Spans
- CreateTenant (root), ValidateInputs, WriteTenant, PublishChange
- PutRegions (root), LoadTenant, ValidateRegions, UpsertRegions, PublishChange
- PutPlan (root), ValidatePlan, UpsertPlan, PublishChange

## Dashboards
- Tenant count by status
- Lifecycle transitions by outcome
- API latency and error rates
- Write error spikes

## Alerts
- Lifecycle transition failure rate breach
- API error rate breach
- Latency p95 breach on write routes

## SLOs
- Read availability based on 2xx rate
- Write p95 within target

## Retention and sampling
- Keep write logs per audit policy
- Sample traces on writes and transition flows
