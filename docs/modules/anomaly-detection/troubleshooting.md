
# Anomaly Detection Module — Troubleshooting and Operations Guide

Audience: SRE, DevOps, data engineers, tenant administrators  
Status: Version 1.0  
Purpose: Provide a structured approach to diagnosing and resolving issues in rule based anomaly detection within a tenant boundary, with full emphasis on isolation, observability, and repeatability.

---

## Operating model

All investigations begin with three identifiers that must be captured at the start of work.

- tenant id  
- correlation id or request id associated with the job or API call  
- time window and metric or rule involved

With those in hand, use the diagnostics workflow below to avoid guesswork.

---

## Diagnostics workflow

1. Verify pipeline freshness  
   - Confirm the KPI table changed as expected.  
   - Check event bus delivery of the refresh event.  
   - Inspect pipeline run logs for the same correlation id.

2. Verify rule catalog and tenant rules  
   - Ensure the rule exists, is active, and references a valid metric.  
   - Validate baseline window and predicate bounds against system constraints.  
   - Confirm the rule version that was effective during the period.

3. Verify evaluation job  
   - Query the job by request id.  
   - Check job state, counts, and evaluator shard identity.  
   - Review evaluator logs for validation or compute errors.

4. Verify anomaly registry writes  
   - Look up events by tenant id and request id.  
   - Confirm idempotent behavior for retries.  
   - Check severity and period keys for correctness.

5. Verify notifications and workflows  
   - Inspect webhook delivery attempts and status.  
   - Check email or workflow creation logs.  
   - Replay delivery if destination was unavailable.

6. Verify status and resolution  
   - Confirm that analysts can update event status.  
   - Check audit entries for configuration changes tied to the incident.  
   - Record final actions in the postmortem note.

---

## Observability checklist

Metrics to check first

- anomaly_rule_evaluation_seconds  
- anomaly_events_created_total  
- anomaly_rule_execution_failures  
- anomaly_pipeline_trigger_lag_seconds  
- anomaly_false_positive_ratio

Logs to review

- evaluator logs keyed by job id and correlation id  
- dispatcher logs for queue depth and rate limits  
- webhook delivery logs for failures or dead letter entries

Audit entries to confirm

- rule create or update around the incident window  
- configuration changes for baseline windows or severity mapping  
- access changes that could impact permissions

---

## Common incident patterns

### KPI refresh event missing

Symptoms  
- No evaluation jobs created after a known KPI publish.  
- Trigger lag metric increases for the tenant.

Checks  
- Pipeline published event with correct tenant id and table name.  
- Event bus subscription for control plane dispatcher is healthy.  
- Dispatcher logs show receipt of event or backpressure.

Remediation  
- Re publish the refresh event with the correct identifiers.  
- Reduce dispatcher queue depth if saturated.  
- Add alert on missing refresh events per table.

### Evaluation job stuck or slow

Symptoms  
- Job remains in running state beyond expected duration.  
- evaluator latency histogram shows long tails.

Checks  
- Look for large KPI slice sizes or wide baseline windows.  
- Check for SQL pushdown limits or missing indexes.  
- Review concurrent job count against tenant quota.

Remediation  
- Reduce window size for the rule during peak hours.  
- Add or tune indexes on period keys and tenant id.  
- Increase tenant concurrency quota if capacity allows.

### No anomalies written when expected

Symptoms  
- Analysts report a visible drop or spike, but registry has no events.

Checks  
- Predicate too strict or baseline too wide for the signal.  
- Rule not active or disabled by policy.  
- Period key alignment mismatch between KPI table and evaluator.

Remediation  
- Run a dry evaluation for the same window and inspect predicate math.  
- Narrow baseline window or reduce threshold.  
- Align period key format and time zone across KPI and evaluator.

### Excess anomalies or false positives

Symptoms  
- Sudden surge in event counts, high false positive ratio.  
- Noise floods notification channels.

Checks  
- Baseline window too narrow for seasonal data.  
- Predicate ignores minimum volume requirements.  
- Data pipeline introduced backfill or duplication.

Remediation  
- Increase baseline window to include seasonal context.  
- Add minimum volume guard to the rule.  
- Pause notifications during backfill and resume after stabilization.

### Webhook or email delivery failures

Symptoms  
- Missing notifications or workflow tickets.  
- Dead letter queue growth in delivery logs.

Checks  
- Destination TLS or certificate validation failure.  
- Rate limits or authentication errors at destination.  
- Network egress policy blocking the endpoint.

Remediation  
- Update allowed endpoints or rotate secrets.  
- Enable exponential backoff with jitter and replay.  
- Provide alternate channel as fallback for critical severities.

### Idempotency collision

Symptoms  
- Replays or retries do not create expected events.  
- Natural key already exists for the same tuple.

Checks  
- Confirm request id usage in evaluate and write paths.  
- Duplicate replay attempted with unchanged input slice.

Remediation  
- Change request id for intended re evaluation.  
- If truly new inputs, verify evaluator includes the latest KPI snapshot version in its slice key.

### Access denied for API calls

Symptoms  
- 403 responses for rule or evaluation endpoints.

Checks  
- Missing or expired token, wrong tenant id, or role lacks permission.  
- Access module change that removed required scopes.

Remediation  
- Re authenticate and confirm JWT scopes.  
- Assign the correct role to the caller and retry.

### Configuration rejected

Symptoms  
- Validation failure with message about bounds or missing references.

Checks  
- Baseline windows within allowed system range.  
- Referenced metrics and workflows exist.  
- Rule pack name and version valid.

Remediation  
- Adjust to allowed bounds.  
- Create missing dependencies or correct names.  
- Use simulation mode to verify before activation.

---

## Runbooks

### Replay a failed evaluation window

Preconditions  
- Known tenant id and window.  
- Rules to include in replay.  
- Root cause remediated.

Steps  
1. Submit replay request to evaluate endpoint with `replay=true`.  
2. Use a new request id to avoid idempotency collision.  
3. Monitor job status and counters.  
4. Confirm events appear in registry and notifications resume.  
5. Link replay summary in the incident ticket.

### Contain a false positive storm

Steps  
1. Suspend noisy rules temporarily.  
2. Increase baseline window or add minimum volume guard.  
3. Re enable notifications after dry run confirms noise reduction.  
4. Document changes and create a follow up for permanent tuning.

### Restore webhook delivery

Steps  
1. Test endpoint reachability and TLS.  
2. Rotate the shared secret and update destination.  
3. Requeue deliveries from dead letter queue.  
4. Confirm successful delivery and clear backlog alerts.

### Reduce evaluator latency

Steps  
1. Profile queries for KPI slices and add missing indexes.  
2. Push down more computation to SQL where safe.  
3. Increase worker pool near data location.  
4. Split large rule sets into smaller batches.  
5. Re check latency histograms to confirm improvement.

---

## Verification queries

Recent job state  
```sql
select run_id, started_at, completed_at, evaluated_count, match_count, error_count
from eval_runs
where tenant_id = $1
  and started_at >= now() - interval '1 day'
order by started_at desc;
```

Anomalies for a metric and window  
```sql
select *
from anomaly_event
where tenant_id = $1
  and metric = $2
  and period_key between $3 and $4
order by created_at desc;
```

Delivery failures in the last hour  
```sql
select *
from event_delivery
where tenant_id = $1
  and status in ('retry','failed','dead_letter')
  and created_at >= now() - interval '1 hour'
order by created_at desc;
```

---

## Performance guidance

- Keep period keys aligned to the KPI granularity.  
- Avoid extremely wide baseline windows without an indexing plan.  
- Prefer vectorized SQL operations for aggregates, then compute predicates in the evaluator.  
- Batch rules by metric family to improve cache locality.  
- Use separate worker pools for heavy tenants to avoid noisy neighbor effects.

---

## Security checks

- Confirm that worker roles have least privilege access to the KPI tables and the registry.  
- Validate that exports use signed URLs and expire quickly.  
- Review access logs for repeated 403 responses that might indicate permission drift.  
- Ensure audit trails exist for every rule change.

---

## Frequently asked questions

Q. Why did a replay not write any new events  
A. The natural idempotency key matched existing events. Change the request id or window to reflect new inputs.

Q. Why do I see anomalies only after several hours  
A. Evaluation is waiting for the KPI refresh event or scheduled cron window. Check trigger lag metrics and dispatcher state.

Q. Can a tenant admin bypass platform limits on baseline windows  
A. No. System constraints apply to prevent excessive load and to preserve stable evaluation behavior.

Q. Can we re evaluate only one rule out of a pack  
A. Yes. Provide the rule id list in the evaluation request payload.

Q. How do we reduce false positives for seasonal data  
A. Use a longer trailing window or compare against the same period last year, if sufficient history exists.

---

## Summary

Troubleshooting focuses on traceable identifiers, predictable evaluation lifecycle, and strict tenant isolation.  
Use metrics and logs to locate the stage where work stalled or failed.  
Apply runbooks that change one dimension at a time and always close with audit entries, status updates, and a short postmortem note.
