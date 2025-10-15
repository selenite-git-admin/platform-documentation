# Notifications Runbook

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Actionable playbooks for operating the Notifications module in a baseline deployment of API Gateway + Lambda + SQS + SES. Covers detection, triage, mitigation, verification, and post‑incident steps. All examples assume `ap-south-1` but apply to any region.

## Architecture context
Producer → API Gateway → Lambda (ingress) → PostgreSQL write → SQS queue → Lambda workers → Channel adapters → SES or other providers → Provider callbacks → Evidence Ledger.

Ownership
- Platform Foundation: API, workers, queue policies, channel adapters
- SRE: alarms, runbook automation, incident leadership
- Security: secrets rotation, suppression policy
- Product teams: template correctness and variables

## Severity matrix
| Severity | Symptoms | Blast radius | Examples |
|---|---|---|---|
| P1 | Delivery success drops below 98 percent for 10 minutes or queue backlog explodes | Many tenants | SES region outage, provider API throttling, SQS permission issue |
| P2 | One channel or template degraded | Some tenants | Slack token revoked, webhook target down |
| P3 | Client misuse or authoring errors | Single tenant or template | Variable validation failures, rate limit exceeded |

## Golden signals to check
- Delivery success ratio per channel
- Queue depth and age
- P95 end‑to‑end latency
- Provider latency and error rate
- Bounce and suppression trends
- Rate‑limited requests

## Standard dashboards
- Overview: submissions, deliveries, failures, queue depth, latency
- Provider health: SES send, bounce, complaint, throttle
- Template and tenant breakdowns
- Alarm overview with burn rates

---

## P1 playbook: provider outage or heavy degradation (SES)

### Detect
- Alerts fire: high failure rate or provider latency spike
- SES dash shows increased `Throttling` or `ServiceUnavailable`

### Triage
- Confirm if region specific by comparing multiple regions
- Check AWS Health Dashboard for SES events
- Verify that API ingress is healthy and queue is filling

### Mitigation
- Enable backpressure
  - Reduce worker concurrency by 50 percent to stop hot‑loop retries
  - Increase `Retry‑After` on API `429` responses
- Fail open for low priority templates
  - Defer low priority sends by increasing schedule offsets
- Consider cross‑region failover if approved
  - Switch SES endpoint to secondary region for high priority templates

### AWS commands
Scale worker concurrency down
```bash
aws lambda put-function-concurrency   --function-name notifications-worker   --reserved-concurrent-executions 10   --region ap-south-1
```

Pause low priority processing via env flag
```bash
aws lambda update-function-configuration   --function-name notifications-worker   --environment "Variables={PAUSE_LOW_PRIORITY=true}"   --region ap-south-1
```

Check SES account send quota
```bash
aws sesv2 get-account --region ap-south-1
```

### Verify
- Failure rate returns under 2 percent for 15 minutes
- Queue depth trending down and age < 60 seconds
- P95 latency within target

### Close
- Restore worker concurrency gradually
- Postmortem and provider ticket link recorded

---

## P1 playbook: queue backlog

### Detect
- Alert fires: `queue_depth > 5000` or `max message age > 60s`

### Triage
- Identify which channel is slow by looking at attempt logs
- Inspect worker errors for throttling or provider timeouts

### Mitigation
- Scale up workers for the affected channel
- Temporarily suspend non‑critical templates
- Split long running templates to smaller messages if applicable

### AWS commands
Increase worker concurrency
```bash
aws lambda put-function-concurrency   --function-name notifications-worker-email   --reserved-concurrent-executions 200   --region ap-south-1
```

Peek at queue attributes
```bash
aws sqs get-queue-attributes   --queue-url https://sqs.ap-south-1.amazonaws.com/123456789012/notifications-main   --attribute-names ApproximateNumberOfMessages ApproximateAgeOfOldestMessage
```

Purge a dead‑letter queue after snapshot
```bash
aws sqs purge-queue --queue-url https://sqs.ap-south-1.amazonaws.com/123456789012/notifications-dlq
```

### Verify
- Queue depth and age fall to baseline
- Delivery success ratio stabilizes

---

## P2 playbook: bounce surge

### Detect
- Alert: bounce rate > 3 percent over 15 minutes

### Triage
- Identify templates and tenants with highest bounces
- Check recent domain or DNS changes for From domain

### Mitigation
- Auto‑suppress offending addresses and tenants
- Pause sends for the affected template or tenant
- Validate DKIM, SPF, and DMARC

### AWS commands
List recent bounces
```bash
aws sesv2 list-email-identities --region ap-south-1
aws sesv2 get-identity-mail-from-attributes --email-identity no-reply@example.com --region ap-south-1
```

Add suppressions
```bash
aws sesv2 put-suppressed-destination   --email-address baduser@example.com   --reason BOUNCE   --region ap-south-1
```

### Verify
- Bounce rate returns to baseline for the last 60 minutes
- No new complaints recorded

---

## P2 playbook: webhook target failures

### Detect
- Channel failures rise on `webhook` with `timeout` or `dependency_unavailable`

### Triage
- Confirm destination TLS and signature verification behavior
- Check rate limit or outage on the partner system

### Mitigation
- Increase backoff and max attempts for webhook channel
- Switch failing endpoints to inactive and notify tenant
- Move to dead‑letter and schedule replay during off‑peak

### Verify
- Successful delivery ratio improves
- DLQ replays succeed during maintenance window

---

## P3 playbook: validation failures

### Detect
- `template_errors_total` spikes or API returns `validation_failed`

### Triage
- Identify the template and variable keys causing failures
- Confirm template version change and schema

### Mitigation
- Roll back to last known good template version
- Add schema hints and defaults
- Improve error messages in UI and SDK

### AWS commands
Rollback a template version flag in metadata store (example SQL)
```sql
update template_version
set is_active = false
where template_id = 'kpi-alert' and id = 'bad-version-uuid';

update template_version
set is_active = true
where template_id = 'kpi-alert' and id = 'good-version-uuid';
```

### Verify
- API `validation_failed` rate returns to baseline
- New submissions succeed using the restored version

---

## P3 playbook: idempotency conflicts

### Detect
- API `409 conflict` with same Idempotency‑Key and divergent payloads

### Triage
- Identify the client and reason for duplicate keys
- Check clock skew or retry library behavior

### Mitigation
- Educate client to use unique keys per logical operation
- Increase idempotency window if legitimate replays occur
- Add server‑side hashing to reject divergent payloads early

### Verify
- Conflict rate falls and delivery is stable

---

## Cross‑cutting diagnostics

### CloudWatch Logs Insights
Recent provider errors
```sql
fields @timestamp, error_code, channel, template_id, tenant_id, correlation_id
| filter service = "notifications" and event = "attempt.completed" and status = "failed"
| sort @timestamp desc
| limit 50
```

Slow deliveries
```sql
fields @timestamp, latency_ms, channel, template_id, correlation_id
| filter service = "notifications" and event = "attempt.completed" and status = "delivered" and latency_ms > 10000
| sort latency_ms desc
| limit 20
```

### SQL: hot queries
Top failing templates 1h
```sql
select r.template_id, a.channel, count(*) as failures
from notification_attempt a
join notification_request r on r.id = a.request_id
where a.state = 'failed' and a.last_attempt_at > now() - interval '1 hour'
group by r.template_id, a.channel
order by failures desc;
```

Oldest messages in queue (sample from DLQ table if mirrored)
```sql
select * from notifications_dlq order by enqueued_at asc limit 20;
```

---

## Alarm mappings

| Alarm name | Metric and condition | Severity | Auto‑action |
|---|---|---|---|
| `notif-failure-rate-high` | failures over attempts > 5 percent for 5 minutes | P1 | Page oncall |
| `notif-provider-latency-p95` | p95 latency > 15 s for 10 minutes | P2 | Notify engineering |
| `notif-queue-depth-high` | SQS ApproximateNumberOfMessages > 5000 for 5 minutes | P1 | Scale workers up |
| `notif-queue-age-high` | ApproximateAgeOfOldestMessage > 60 s for 5 minutes | P1 | Scale workers and throttle ingress |
| `notif-bounce-rate-surge` | bounce rate > 3 percent for 15 minutes | P2 | Auto‑suppress and alert |
| `notif-callback-missing` | callback not received within 2x median latency | P2 | Investigate provider and network |
| `notif-rate-limited-burst` | rate_limited_total > 1000 in 10 minutes | P3 | Review abusive tenants |

CloudFormation example (excerpt)
```yaml
NotifQueueDepthHigh:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: notif-queue-depth-high
    MetricName: ApproximateNumberOfMessagesVisible
    Namespace: AWS/SQS
    Statistic: Sum
    Period: 60
    EvaluationPeriods: 5
    Threshold: 5000
    ComparisonOperator: GreaterThanThreshold
    Dimensions:
      - Name: QueueName
        Value: notifications-main
    AlarmActions:
      - arn:aws:sns:ap-south-1:123456789012:oncall-pages
```

---

## Recovery patterns

- Gradual concurrency ramp
  - Increase Lambda reserved concurrency in steps of 20 percent every 5 minutes
- Replay from DLQ
  - Export DLQ to S3, validate, and re‑enqueue in small batches with an idempotent loader
- Cross‑region divert
  - Enable pre‑approved template list to send via secondary SES region
- Template rollback
  - Switch `is_active` pointer and invalidate cached renderers

---

## Post‑incident

- Verification
  - Error rates and latency at baseline for 30 minutes
  - Queue metrics nominal
  - Sample messages confirm correct rendering and delivery
- Forensics
  - Evidence Ledger entries linked by correlation id
  - Attach SES ticket id and AWS Health event
- Actions
  - Update alarms or thresholds if noisy
  - Add test coverage for the regression
  - Document customer impact and credits if applicable

## Quick reference

### Health checks
```bash
aws lambda get-function --function-name notifications-worker --region ap-south-1
aws sqs get-queue-attributes --queue-url https://sqs.ap-south-1.amazonaws.com/123456789012/notifications-main --attribute-names ApproximateNumberOfMessages ApproximateAgeOfOldestMessage
aws sesv2 get-account --region ap-south-1
```

### Toggle features
```bash
aws lambda update-function-configuration   --function-name notifications-worker   --environment "Variables={PAUSE_LOW_PRIORITY=false,MAX_RETRIES=5}"   --region ap-south-1
```

### Tail errors
```bash
aws logs tail /aws/lambda/notifications-worker --since 30m --format short --region ap-south-1 | grep ERROR
```

## Summary
This runbook gives operators clear, tested responses to the most common failure modes in a Lambda + SQS + SES deployment. Start with signals, apply the targeted mitigation, verify through metrics and logs, and close the loop with Evidence Ledger and template hygiene.