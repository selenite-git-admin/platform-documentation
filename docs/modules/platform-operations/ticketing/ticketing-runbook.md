# Ticketing Runbook

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Operational guidance for the platform‑scoped Ticketing service on AWS (API Gateway + Lambda, RDS PostgreSQL, S3 attachments, SQS workers). Covers triage, recovery, and post‑incident actions.

## System Overview
- **Entry:** API Gateway (POST, PATCH, GET)
- **Execution:** Lambda (create/update/search, background workers)
- **Storage:** RDS PostgreSQL
- **Queue:** SQS for timers/webhooks
- **Notifications:** SES + Notifications module
- **Observability:** CloudWatch + OpenTelemetry

Key dependencies: Auth, RBAC, Notifications, DRR, Health, Runtime.

## Incident Taxonomy
| Type | Example | Impact |
|------|--------|--------|
| Create Failures | POST /tickets 5xx | Users and systems cannot open work |
| Update Failures | PATCH /tickets 5xx | States/assignees stale |
| Webhook Failures | downstream 4xx/5xx | Automations missed |
| SLA Timer Failure | timers not firing | SLA compliance risk |
| Queue Backlog | SQS > 1000 | Async lag |
| DB Unavailable | RDS down | Total outage |
| Auth/RBAC Errors | scope leaks or denials | Privacy or access issues |
| Dedup Disabled | duplicate incidents | Ops noise |

## Triage Flow
1. **Health check**
   - `/healthz`, `/readyz` on Ticketing
   - CloudWatch alarms for errors/latency

2. **Scope and impact**
   - Is it platform‑wide or limited to specific tenant buckets?
   - Check create/update success ratios and backlog

3. **Logs and traces**
   - Filter by `correlation_id` from alerts
   - Inspect DB errors and throttles

4. **Immediate containment**
   - Pause bulk webhooks to noisy endpoints
   - Increase Lambda concurrency for backlog drains
   - Roll back to last healthy alias if deploy related

## Common Scenarios and Fixes
### Create Failures
- **Checks:** RDS connectivity, auth verification latency, cold starts
- **Fixes:** warmers on critical paths, DB pool tuning, temporary rate limit

### Webhook Failures
- **Checks:** `ticket_webhook_out_fail_total`, target 4xx/5xx mix
- **Fixes:** quarantine failing targets, replay DLQ, notify owners

### SLA Timer Drift
- **Checks:** EventBridge schedule health, worker errors
- **Fixes:** backfill timers for last 2 hours, re‑enable mapping

### Queue Backlog
- **Checks:** SQS metrics, Lambda concurrency
- **Fixes:** raise reserved concurrency, add shards, clear poison messages

### Auth/RBAC Issues
- **Checks:** deny logs for out‑of‑scope reads, confirm `visibility` logic
- **Fixes:** hotfix policy evaluation, run scoped queries in canary tests

## Recovery Commands
Replay webhooks
```bash
aws lambda invoke --function-name ticketing-replay-dlq /dev/null
```

Check stale tickets
```sql
select id, key, state, updated_at
from ticket
where state not in ('closed','canceled')
and now() - updated_at > interval '7 days';
```

Backlog size
```bash
aws sqs get-queue-attributes --queue-url $QUEUE_URL --attribute-names ApproximateNumberOfMessages
```

## Closeout
- Verify `/readyz` and write success ratio back to normal
- Ensure SLA timers are caught up and breach counts stable
- Link Evidence Ledger entries to the incident ticket
- Postmortem with gaps and action items

## Validation Checklist
- [ ] API latency within SLO
- [ ] Error ratio < 1 percent
- [ ] RDS connections stable
- [ ] SQS backlog < 100
- [ ] SLA timers firing
- [ ] Webhooks delivering
- [ ] RBAC checks pass for tenant and platform roles

## Summary
Operate Ticketing as a centralized, platform‑wide service. Keep tenant privacy through RBAC and `visibility`, and optimize for quick recovery and low noise.