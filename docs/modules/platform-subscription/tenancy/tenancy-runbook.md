# Tenancy Module Runbook

**Audience:** Site Reliability Engineers, Operations, Platform Support  
**Status:** Working draft  
**Purpose:** Provide a structured operational guide for detecting, triaging, and remediating incidents in the Tenancy module. This document defines standard procedures for alert handling, diagnostics, command usage, rollback, and escalation. It consolidates all runbook material from Tenant Management and aligns it with the Tenancy observability signals and SLOs.

## Incident Response Framework

**Principles**
- Safety first: protect customer data and prevent cascading failures.
- Reversibility: any mitigation action must have a defined rollback path.
- Auditability: all interventions must be logged with actor, time, and command trace.
- Coordination: major incidents must have a declared incident commander.

**Severity levels**
- Sev1: customer data inaccessible or major control plane outage.
- Sev2: partial degradation or significant latency in reconcile or webhook delivery.
- Sev3: functional errors within SLA impact window but not user visible.
- Sev4: documentation or monitoring gap, no production impact.

## Alert Ingestion

Alerts originate from the observability stack and are routed to PagerDuty, Slack, and email channels. Every alert includes:
- subsystem name (controller, webhook, policy, api)
- region
- primary metric and threshold
- current value
- direct links to dashboards and this runbook

All alerts are actionable. Non-actionable alerts must be tuned or removed.

## Diagnostic Workflow

### Controller health
1. Open dashboard `Controller Health`.
2. Inspect `reconcile_failures_total` and `queue_depth` graphs.
3. Run command `kubectl logs controller-<id> | grep ERROR` to identify failure signatures.
4. Verify SQS queue depth and DLQ metrics for backlog.
5. Confirm if failures correlate to specific tenants or regions.

### Webhook delivery
1. Open dashboard `Webhook Delivery`.
2. Review `webhook_failures_total` and `webhook_latency_ms` trends.
3. Identify endpoints with persistent failures.
4. Query DLQ for recent inserts using `aws sqs receive-message --queue-url ...`.
5. Validate endpoint availability using curl or synthetic probe.

### Policy evaluation
1. Check `policy_eval_latency_ms` and `policy_eval_errors_total`.
2. Verify connectivity to policy service and cache hit rate.
3. Re-run policy evaluation with verbose flag for one failing tenant.
4. Confirm residency and encryption policy IDs match expected version.

### API health
1. Monitor `http_requests_total` and `http_errors_total`.
2. Inspect 429 or 5xx error bursts.
3. Validate gateway rate limit configuration and backend latency.
4. Reproduce with known-good token to isolate client versus service issue.

### Lifecycle orchestration
1. Inspect `lifecycle_job_failures_total`.
2. Query job logs and identify stuck steps.
3. Use API `GET /tenants/{tenantId}/jobs` to check current status.
4. Retry failed job with admin override when safe and audited.

## Remediation Procedures

### Controller restart
- Validate that replicas > 1 for redundancy.
- Drain a single pod before restart.
- Confirm queue backlog draining after restart.
- Verify reconcile success rate after five minutes.

### Webhook requeue
- Identify DLQ messages using sequence range.
- Use requeue API `POST /tenants/{tenantId}/webhooks:requeue`.
- Monitor delivery success rate post requeue.
- Archive old DLQ messages after success confirmation.

### Policy cache refresh
- Execute cache invalidate command via admin CLI.
- Confirm next evaluation latency normalizes.
- Document cache key and root cause in incident notes.

### API rate limit adjustment
- Temporarily raise burst multiplier via admin override API.
- Record reason and expected rollback time.
- Validate rollback after incident closure.

### Migration rollback
- Stop ongoing migration jobs.
- Switch traffic to previous region or database endpoint.
- Validate data integrity by checksum comparison.
- Re-run migration under controlled schedule.

## Common Failure Patterns

**Excessive reconcile backlog**
- Cause: transient policy failures, DLQ congestion, controller throttling.
- Action: scale controller replicas, requeue failed tenants, clear DLQ, validate policy endpoint.

**Webhook delivery storm**
- Cause: endpoint outage or misconfiguration.
- Action: disable offending endpoint temporarily, increase backoff, alert tenant admin.

**Policy evaluation timeout**
- Cause: downstream policy service slowness.
- Action: verify service health, adjust timeout, enable fallback cache.

**Rate limit saturation**
- Cause: bulk tenant sync or misbehaving client.
- Action: enable adaptive throttling, contact client owner, review quota policy.

**Migration hang**
- Cause: replication lag or verification step blocking.
- Action: check replication health, extend cutover window, resume job.

## Escalation Matrix

| Severity | Primary Owner | Backup Owner | Escalation Path |
|-----------|----------------|---------------|-----------------|
| Sev1 | Platform SRE | Engineering Manager | CTO / Incident Commander |
| Sev2 | Platform SRE | Tenancy Engineering | Engineering Manager |
| Sev3 | On-call SRE | Platform Engineering | Engineering Manager |
| Sev4 | Documentation Owner | N/A | SRE Manager |

Escalations must include timeline, affected tenants, and mitigation summary.

## Audit And Postmortem

Every incident requires a retrospective within five business days. The report includes:
- incident summary and impact
- detection and response timeline
- root cause and contributing factors
- corrective actions and prevention tasks
- owners and due dates

All postmortems are stored in the internal DocuHub and linked from the incident tracker.

## Verification After Recovery

**Checklist**
- Alerts cleared and SLOs met
- Queues drained
- Reconciles successful for last 15 minutes
- Webhook deliveries normal latency and no DLQ growth
- Policy evaluation latency below threshold
- Audit logs show closure event

## Automation Hooks

- Incident creation automatically attaches latest dashboards and this runbook link.
- Controller auto-heal scripts run for known transient conditions.
- DLQ auto requeue for specific retryable codes.
- Policy cache auto refresh after service redeploy.

## Maintenance Tasks

- Review alert thresholds quarterly.
- Test failover drill bi-weekly.
- Validate metric names and dashboard bindings monthly.
- Update SLO targets after major version changes.
- Verify webhook signing key rotation scripts quarterly.