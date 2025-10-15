# Observability

## Scope
Observability for Platform Catalog. This page defines metrics, logs, traces, dashboards, alerts, and SLOs for a read heavy service with audited writes.

## Diagram
<a href="#fig-pc-obs" class="image-link">
  <img src="/assets/diagrams/platform-catalog/observability-architecture.svg" alt="Platform Catalog observability architecture">
</a>

<div id="fig-pc-obs" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/platform-catalog/observability-architecture.svg" alt="Platform Catalog observability architecture">
</div>

_Figure 1: Platform Catalog observability architecture_{.figure-caption}

## Metrics
- catalog_reads_total
  Counter. Labels: route, status. Purpose: read traffic.
- catalog_read_latency_ms
  Histogram. Labels: route, status. Purpose: tail latency.
- catalog_writes_total
  Counter. Labels: resource, result. Purpose: write volume and errors.
- catalog_write_latency_ms
  Histogram. Labels: resource. Purpose: admin write latency.
- catalog_events_published_total
  Counter. Labels: topic. Purpose: cache busting activity.

## Logs
Structured JSON with correlation identifiers on all writes. Log event names:
- catalog.region.upsert
- catalog.plan.create
- catalog.plan.feature.upsert
- catalog.limit.upsert
- catalog.calendar.definition.create
- catalog.calendar.event.create
- catalog.calendar.set.create
- catalog.overlay.put

Required fields
- correlation_id, actor, target, etag_before, etag_after

## Traces
- Write path spans: Validate, Persist, PublishEvent
- Read path spans: CacheCheck, StoreRead, Transform

## Dashboards
- Read health: rate, p95, p99 by route
- Write health: count and latency by resource
- Eventing: events published by topic
- Error budget: 5xx and timeouts

## Alerts
- Read latency p95 breach for hot routes
- Write error rate spike on any resource
- Event publish failures

## SLOs
- Read availability based on 2xx rate
- Read latency p95 within target
- Write success rate for admin endpoints

## Retention and sampling
- Keep write logs per audit policy
- Sample traces for reads, keep writes at higher rate
