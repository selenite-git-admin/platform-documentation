# Observability

## Scope
Observability for Data Contract Registry. This page defines metrics, logs, traces, dashboards, alerts, and SLOs for the four-layer, artifact-only model.

## Diagram
Signal flow at a glance.

<a href="#fig-dcr-observability" class="image-link">
  <img src="/assets/diagrams/data-contract-registry/observability-architecture.svg" alt="Data Contract Registry observability architecture">
</a>

<div id="fig-dcr-observability" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-contract-registry/observability-architecture.svg" alt="Data Contract Registry observability architecture">
</div>

_Figure 1: Data Contract Registry observability architecture_{.figure-caption}

## Signals

### Metrics
Emit the following metrics with explicit units. Add labels where noted.

- dcr_schema_ingests_total
  Counter. Labels: layer, result (ok, invalid, conflict). Purpose: ingest volume and errors.
- dcr_schema_ingest_latency_ms
  Histogram. Labels: layer. Purpose: end to end ingest time.
- dcr_version_classifications_total
  Counter. Labels: layer, classification (compatible, backward, forward, none, breaking). Purpose: change mix.
- dcr_current_set_total
  Counter. Labels: layer. Purpose: counts of current flips.
- dcr_breaking_changes_total
  Counter. Labels: layer. Purpose: breaking signals to consumers.
- dcr_diff_latency_ms
  Histogram. Labels: layer. Purpose: diff computation time.
- dcr_subscriptions_total
  Gauge. Labels: layer. Purpose: consumer coverage per layer.
- api_requests_total
  Counter. Labels: route, method, status. Purpose: read and write traffic.
- api_request_duration_ms
  Histogram. Labels: route, method, status. Purpose: tail latency tracking.
- registry_store_latency_ms
  Histogram. Labels: operation (read, write). Purpose: datastore health.
- registry_store_errors_total
  Counter. Labels: operation. Purpose: error budget accounting.

### Logs
Use structured JSON logs. Include correlation identifiers for write paths.

Event names
- dcr.dataset.created
- dcr.schema.ingested
- dcr.version.classified
- dcr.current.set
- dcr.breaking.detected
- dcr.subscription.created
- dcr.subscription.listed

Required fields
- correlation_id
- dataset_id
- namespace
- name
- layer
- version
- schema_registry_id
- classification
- is_current
- consumer
- subscription_id
- at

### Traces
Create traces for write and read paths.

Write path spans
- IngestSchema (root)
- ValidateSchema
- LoadCurrent
- ComputeDiff
- ClassifyChange
- PersistVersion
- SetCurrent (conditional)
- EmitSignals

Read path spans
- GetSchemaVersion (root)
- ListSchemaVersions
- ComputeDiff

Attributes
- dataset_id, namespace, name
- layer, version
- classification, is_current
- correlation_id

## Dashboards

Contracts Health
- ingests over time by result and layer
- classification mix by layer
- current flips by layer
- subscriptions by layer and consumer

Breaking and Current Changes
- breaking changes time series
- recent breakings table with dataset, layer, version
- recent current flips table

API and Store Health
- request rate by route and status
- p95 and p99 latency by route
- store latency and errors by operation

Consumer Impact
- subscriptions by activation layer
- recent breakings affecting activation datasets

## Alerts

Breaking detected
- Condition: dcr_breaking_changes_total rate exceeds threshold or any on activation layer
- Action: create incident and notify owners

Current flip anomaly
- Condition: dcr_current_set_total spikes for a dataset and layer
- Action: verify change history and consumers

Ingest error rate
- Condition: dcr_schema_ingests_total with result=invalid or conflict rises
- Action: inspect schema validation and idempotency keys

Diff slow
- Condition: dcr_diff_latency_ms p95 exceeds target
- Action: check schema size, diff algorithm, store latency

Store degradation
- Condition: registry_store_latency_ms p95 or errors rise
- Action: check database health and recent changes

Read API latency
- Condition: api_request_duration_ms p95 breaches target on read routes
- Action: profile queries and indexes

## Service level objectives

Availability
- SLO: successful read responses over total read requests
- Monitor with api_requests_total labels method=GET and status

Latency
- SLO: p95 latency on read endpoints within target
- Monitor with api_request_duration_ms

Ingest timeliness
- SLO: p95 ingest latency within target
- Monitor with dcr_schema_ingest_latency_ms

## Retention and sampling
- Retain write-path logs for the platform retention window
- Sample traces to meet storage budgets while preserving ingest and breaking events
- Downsample high-volume metrics if needed

## Runbook hooks
See [Runbook](runbook.md) for investigation and recovery steps tied to the alerts listed here.

## References
- [API](api.md)
- [Data Model](data-model.md)
