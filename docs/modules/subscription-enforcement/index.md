# Subscription Enforcement

## Role in the Platform
The Subscription Enforcement module ensures that every tenant request respects the contracted plan, feature entitlements, and usage thresholds. It evaluates requests in real time, returns a decision, and records evidence for audit and billing reconciliation. It exposes tenant-facing APIs for entitlement queries, quota visibility, and what-if simulations. It operates after Authorization and before Metering so that usage is consistent with plan contracts.

## Position in the Platform
Authorization authenticates the subject and authorizes the action. Subscription Enforcement evaluates limits and entitlements for the same action. Metering records the usage deltas for billing and analytics. Evidence Ledger stores a tamper-evident record of the decision.

<a href="#fig-subscription-enforcement-sequence" class="image-link">
  <img src="/assets/diagrams/access/subscription-enforcement-sequence.svg" alt="Subscription Enforcement sequence across AuthZ, Enforcement, Metering, and Evidence">
</a>

<div id="fig-subscription-enforcement-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/access/subscription-enforcement-sequence.svg" alt="Subscription Enforcement sequence across AuthZ, Enforcement, Metering, and Evidence">
</div>

_Figure 1: Evaluation sequence from request to decision and evidence_{.figure-caption}

## Responsibilities
- Enforce plan limits for rate, volume, and feature access.
- Resolve effective entitlements by merging plan, tenant overrides, and promotions.
- Evaluate usage windows and apply soft or hard limits.
- Return a decision: `permit`, `throttle`, `deny`, or `grace`.
- Emit evidence with reason codes and policy references.
- Publish usage deltas to Metering for aggregation.
- Expose APIs for evaluation, plan retrieval, and simulation.
- Cache plan data and recent counters to meet latency objectives.
- Apply consistent reason phrases that map to operator runbooks.

## Inputs
- Plan registry definitions and versions.
- Tenant entitlement records and time-boxed overrides.
- Real-time usage counters for the active window.
- Authorization decision and subject claims.
- Policy flags for promotions and grace behavior.
- Calendar windows for blackout or maintenance periods when configured.

## Outputs
- Decision object with outcome, reason, quota snapshot, and optional retry hint.
- Evidence event with correlation identifiers for audit and support.
- Usage deltas for the selected feature and window.
- Telemetry signals for metrics, logs, and traces.

## Interfaces
- **Enforcement API**. Tenant and admin apps call evaluation and simulation endpoints. The module validates inputs, evaluates entitlements and limits, and returns a structured decision with reason and quota fields. The API is idempotent by `(tenant_id, feature, request_hash)`.
- **Plan Registry**. The module reads plan and entitlement data through a read-optimized store or cache. The registry owns plan authoring, versioning, and approvals. The module does not mutate plan data.
- **Metering Stream**. The module publishes usage deltas for the current window. Metering aggregates deltas by tenant and feature. The module does not perform billing.
- **Evidence Ledger**. The module writes a minimal record with decision, reason, and hashes for verification. The ledger owns immutability and retention.
- **Observability**. The module emits metrics for decisions, latency, and drift, writes structured logs for each evaluation, and links traces across dependencies.

## Operational Behavior
- **Evaluation sequence**. The evaluator computes a request key. It loads plan and entitlement state from the cache. It reads the usage snapshot for the active window. It applies hard limits first. It applies soft limits and grace next. It returns a decision with a reason phrase and optional `retry_after`. It emits evidence and publishes usage deltas when the outcome is `permit` or `grace`.
- **Caching**. The module caches plan and entitlement documents per tenant and edition. It stores a short-lived usage snapshot to avoid cross-service round trips on hot paths. It refreshes stale entries on read. It exposes an admin refresh endpoint.
- **Concurrency**. The evaluator serializes updates for the same `(tenant_id, feature, window)` key to avoid counter races. It allows parallel evaluations for different features or tenants.
- **Idempotency**. The evaluator computes a request hash from stable request fields. It deduplicates repeated calls within a small time window and returns the prior decision.
- **Failure handling**. If the plan cache is unavailable, the module falls back to the last valid version for the tenant. If the usage snapshot is missing, the module queries a secondary path or returns `throttle` with a dependency reason. If the Evidence Ledger is delayed, the module queues the write and completes the API call.
- **Latency objectives**. The module targets a P99 of 50 ms for evaluation. It preloads frequent plans. It avoids synchronous writes on the hot path except for decision computation.

## Constraints
- The module does not author, approve, or publish plans.
- The module does not authenticate or authorize subjects. It consumes claims from Authorization.
- The module does not compute invoices or billing totals. It emits deltas only.
- The module stores short-term caches and evidence pointers. It does not store raw PII.
- Decisions depend on plan version availability. A plan refresh delay can affect outcomes.
- The module requires a consistent calendar to evaluate day and month windows. If the calendar is misconfigured, soft limits can drift.

## Examples in Action
- **Within limit**. Tenant calls `exports.create`. Usage is 998 of 1000 for the day. The module returns `permit` with a quota snapshot of 999 of 1000 and emits an evidence event for the request.
- **Soft limit exceeded**. Tenant calls `exports.create`. Usage is 1002 of 1000 and the plan includes a soft limit. The module returns `throttle` with `retry_after` and a soft limit reason. The module does not publish a usage delta.
- **Hard limit exceeded**. Tenant calls `exports.create`. Usage is 1201 of 1200 and the plan includes a hard limit. The module returns `deny` with a limit reason and a support link.
- **Grace policy**. Tenant is over soft limit during a configured grace window. The module returns `grace` and emits a usage delta. The evidence record includes the grace policy reference.
- **What-if simulation**. Tenant submits a simulation request for the enterprise edition. The module computes outcomes under the target plan and returns the quota difference and the expected decision.

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
