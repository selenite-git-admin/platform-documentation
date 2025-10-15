# Observability

## Scope
Observability for Lineage Obligations.

## Metrics
- lo_events_ingested_total
  Counter. Labels: tenant. Purpose: intake volume.
- lo_edges_total
  Counter. Labels: tenant. Purpose: graph size.
- lo_obligation_evaluations_total
  Counter. Labels: status. Purpose: outcome volume.
- lo_obligation_eval_latency_ms
  Histogram. Purpose: evaluation latency.
- lo_api_requests_total
  Counter. Labels: route, method, status. Purpose: API volume.
- lo_api_request_duration_ms
  Histogram. Labels: route, method, status. Purpose: latency.

## Logs
- lo.event.ingest
- lo.obligation.create
- lo.obligation.update
- lo.evaluate.run

## Traces
- IngestEvent (root), Normalize, UpsertAssets, UpsertEdges
- EvaluateNow (root), LoadScope, Compute, Persist

## Dashboards
- Events ingested over time
- Graph edges by tenant
- Evaluations pass or fail over time
- API latency and error rates

## Alerts
- Ingest failure rate breach
- Evaluation failure spikes
- API error rate breach
- Latency p95 breach on evaluate

## SLOs
- Read availability based on 2xx rate
- Evaluate p95 within target
