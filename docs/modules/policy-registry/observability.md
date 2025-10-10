# Observability

## Scope
This page defines observability for Policy Registry. It covers metrics, logs, traces, dashboards, alerts, and service level objectives.

## Diagram
Architecture view for signals and flow.

<a href="#fig-policy-registry-observability" class="image-link">
  <img src="/assets/diagrams/policy-registry/observability-architecture.svg" alt="Policy Registry observability architecture">
</a>

<div id="fig-policy-registry-observability" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/policy-registry/observability-architecture.svg" alt="Policy Registry observability architecture">
</div>

_Figure 1: Policy Registry observability architecture_{.figure-caption}

## Signals

### Metrics
Emit the following metrics with labels where noted. Units are explicit.

- policy_evaluations_total
  Counter. Labels: decision, scope_type, subject_type, tenant. Purpose: track volume and mix of decisions.
- policy_evaluation_latency_ms
  Histogram. Labels: decision. Purpose: end to end latency from request to decision.
- policy_denials_total
  Counter. Labels: tenant, subject_type. Purpose: spike detection and tenant impact.
- policy_require_approval_total
  Counter. Labels: tenant, subject_type. Purpose: operational load on approvals.
- policy_evaluator_errors_total
  Counter. Labels: error_code. Purpose: error budget accounting.
- policy_missing_bindings_total
  Gauge. Labels: scope_type. Purpose: guard failure when an evaluation finds no binding.
- registry_store_latency_ms
  Histogram. Labels: operation (read, write). Purpose: datastore health for the registry.
- api_requests_total
  Counter. Labels: route, method, status. Purpose: standard API visibility.
- api_request_duration_ms
  Histogram. Labels: route, method, status. Purpose: tail latency tracking.

### Logs
Use structured, JSON logs. Include correlation identifiers.

Event names
- policy.evaluation.requested
- policy.evaluation.decided
- policy.binding.created
- policy.binding.disabled
- policy.policy.created
- policy.policy.version.created
- policy.audit.recorded

Required fields
- correlation_id
- eval_id
- binding_id
- policy_id
- policy_version
- decision
- reason_code
- scope_type
- scope_ref
- subject_type
- subject_ref
- evaluated_at

### Traces
Create a trace per evaluation and include spans for key stages.

Suggested spans
- EvaluatePolicy (root)
- LoadPolicy
- ResolveVersion
- LoadBindings
- EvaluateRules
- WriteEvaluation
- WriteEvidence
- PublishDecision

Attributes
- eval_id, policy_id, policy_version
- decision, reason_code
- scope_type, scope_ref
- subject_type, subject_ref

## Dashboards

Policy Evaluation Health
- evaluation volume by decision over time
- p95 and p99 evaluation latency
- error rate and error codes
- denials by tenant and subject_type

Registry Store Health
- store read and write latency
- error counts by operation
- connection pool saturation

Tenant Impact
- denials and require_approval by tenant
- recent evaluations table with filters

## Alerts

Evaluation error rate
- Condition: policy_evaluator_errors_total rate exceeds threshold
- Action: page on call and create incident

Evaluation latency
- Condition: policy_evaluation_latency_ms p95 exceeds target for sustained period
- Action: investigate store, rule complexity, or hot spots

Denial spike
- Condition: policy_denials_total rate jumps for a tenant or globally
- Action: check recent policy changes and bindings

Missing binding
- Condition: policy_missing_bindings_total rises above zero
- Action: verify bindings for affected scopes

Store degradation
- Condition: registry_store_latency_ms p95 rises or error count increases
- Action: check database health and recent migrations

## Service level objectives

Availability
- SLO: successful evaluation responses over total requests
- Error budget: defined with platform operations
- Monitor with api_requests_total and status labels

Latency
- SLO: evaluation latency at p95 within target
- Target set during performance testing
- Monitor with policy_evaluation_latency_ms

Decision correctness
- Define sampling plan for decision re-checks in lower environments
- Compare sampled decisions to expected outcomes

## Retention and sampling
- Retain decision logs as defined in Security policy
- Sample traces to meet storage budgets while preserving high-cardinality events
- Downsample high-volume metrics where needed

## Runbook hooks
See [Runbook](runbook.md) for investigation and recovery steps tied to the alerts listed here.

## References
- [API](api.md)
- [Data Model](data-model.md)
