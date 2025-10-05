# Observability

## Scope
Observability for Calendar Service. This page defines metrics, logs, traces, dashboards, alerts, and SLOs for range queries and working time utilities.

## Diagram
<a href="#fig-cal-obs" class="image-link">
  <img src="/assets/diagrams/calendar-service/observability-architecture.svg" alt="Calendar Service observability architecture">
</a>

<div id="fig-cal-obs" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/calendar-service/observability-architecture.svg" alt="Calendar Service observability architecture">
</div>

_Figure 1: Calendar Service observability architecture_{.figure-caption}

## Metrics
- cal_resolve_requests_total
  Counter. Labels: tenant, set_id, result. Purpose: resolve volume and errors.
- cal_resolve_latency_ms
  Histogram. Labels: set_id. Purpose: tail latency for resolve.
- cal_working_time_requests_total
  Counter. Labels: op (next_day, add_days, minutes_between), result.
- cal_working_time_latency_ms
  Histogram. Labels: op.
- api_requests_total
  Counter. Labels: route, method, status.
- api_request_duration_ms
  Histogram. Labels: route, method, status.
- store_latency_ms
  Histogram. Labels: operation.
- store_errors_total
  Counter. Labels: operation.

## Logs
Structured JSON. Event names
- cal.definition.create
- cal.event.create
- cal.set.create
- cal.overlay.put
- cal.resolve
- cal.working_time

## Traces
Spans
- ResolveCalendar (root), LoadSet, LoadOverlay, MergeEvents, TransformRange
- WorkingTime (root), LoadEffective, Compute

## Dashboards
- Resolve rate and latency
- Working time rate and latency by op
- Error budget by route
- Store health

## Alerts
- Resolve latency p95 breach
- Working time latency p95 breach
- Store error spikes

## SLOs
- Read availability based on 2xx rate
- Resolve and working time p95 within target

## Retention and sampling
- Keep write logs per audit policy
- Sample traces for resolves, keep working time ops at higher rate

## Date Table signals

Metrics
- cal_datetable_profiles_total
  Counter. Labels: tenant. Purpose: profile count.
- cal_datetable_materialize_total
  Counter. Labels: tenant, format. Purpose: export volume.
- cal_datetable_materialize_latency_ms
  Histogram. Labels: format. Purpose: export latency.

Logs
- cal.datetable.profile.create
- cal.datetable.profile.update
- cal.datetable.materialize

Traces
- Materialize (root), ResolveRange, ComputeRows, WriteOutput
