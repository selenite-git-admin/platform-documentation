# DQC Runbook

**Audience:** SRE, data platform operations, and on call engineers  
**Status:** Working draft  
**Purpose:** Provide a practical guide for detecting, triaging, and resolving incidents in the Data Quality Control module. This runbook defines alerts, severity mapping, diagnostics, standard remediation steps, rollback, and escalation paths. It aligns with DQC Overview and DQC APIs and integrates with Observability and Tenancy.

## Incident Categories And Severity

**Categories**
- Evaluator failures or timeouts
- Rule pack rollout regressions
- Scorecard delays or gaps
- Waiver misuse or expired waivers blocking promotions
- Verdict store latency or partial outages
- API saturation or rate limiting
- Orchestrator job backlog

**Severity levels**
- Sev1: DQC unavailable for multiple datasets or blocks critical promotions across regions
- Sev2: Elevated failure rate or latency affecting a single domain or region
- Sev3: Degraded performance with warnings only or scorecard lag under four hours
- Sev4: Documentation or alert tuning issues without production impact

## SLOs

- Validation p95 under 10 minutes for standard Silver datasets
- Verdict retrieval p95 under 200 ms
- Scorecard generation p95 under 15 minutes from run end
- Rule pack activation shadow window minimum 5 clean runs
- API availability 99.95 percent per region

## Primary Dashboards

- DQC Overview: validation_duration_ms p50 p95 p99, dq_eval_error_total, jobs_running, jobs_failed
- Verdict Store Health: read latency, write latency, error rate, queue depth
- Rule Pack Rollout: shadow run pass rate, deny spikes by version, activation timeline
- Scorecards: lag minutes, generation success rate, per dataset score trend
- Waivers: active count, upcoming expiries, usage by dataset and tenant

## Standard Alert Triggers

- Validation failure rate above 5 percent for five minutes
- dq_eval_error_total above baseline for ten minutes
- Verdict store write latency above 500 ms p95
- Scorecard lag over 60 minutes for any gold dataset
- Deny spike over 3 times baseline after rule pack activation
- Waiver expiries above 20 in 24 hours for a single domain

## First Response Checklist

1. Acknowledge the alert and claim ownership in incident channel
2. Capture X Request Id and correlation id from the alert or logs
3. Identify impacted dataset, stage, region, and tenant scope
4. Check dashboards for correlated spikes or job backlog
5. Decide if promotions must be paused for safety
6. Communicate initial status and next update time

## Diagnostic Playbooks

### Evaluator failures or timeouts

1. Inspect evaluator logs for stack traces and rule names
2. Check orchestrator queue depth and running jobs
3. Verify input partitions and source availability
4. Re run a single partition with failFast true to isolate the rule

Command
```bash
curl -s -X POST https://api.example.com/dqc/v1/validate   -H "Authorization: Bearer $TOKEN"   -H "Idempotency-Key: test-$(uuidgen)"   -H "X-Request-Id: diag-$(uuidgen)"   -d '{
    "dataset":"finance_invoice",
    "stage":"silver",
    "rulepackVersion":3,
    "runId":"diag_run",
    "options":{"mode":"batch","partitions":["2025-10-09"],"failFast":true}
  }'
```

### Rule pack rollout regression

1. Open Rule Pack Rollout dashboard and compare deny rates by version
2. Fetch latest verdicts and sample violations
3. Switch to shadow mode or rollback to previous version if regressions confirmed

Commands
```bash
curl -s "https://api.example.com/dqc/v1/verdicts/finance_invoice/silver?from=2025-10-08"
curl -s -X POST https://api.example.com/dqc/v1/rulepacks/finance_invoice/silver:activate   -H "Authorization: Bearer $TOKEN"   -d '{"version":2,"notes":"rollback due to spike in referential denials"}'
```

### Scorecard delays

1. Check scorecard job queue and last successful generation time
2. Inspect pipeline logs for upstream run completion
3. Re run scorecard build for a single dataset

Command
```bash
curl -s "https://api.example.com/dqc/v1/scorecards/finance_invoice?windowDays=7"
```

### Waiver issues

1. List active waivers and expiries for the dataset
2. Confirm approver and reason meet policy
3. Extend or revoke waiver as needed

Commands
```bash
curl -s "https://api.example.com/dqc/v1/waivers/finance_invoice?stage=silver&active=true"
curl -s -X POST https://api.example.com/dqc/v1/waivers   -H "Authorization: Bearer $TOKEN"   -d '{
    "dataset":"finance_invoice",
    "stage":"silver",
    "ruleName":"range_invoice_amount",
    "approvedBy":"dq_owner",
    "reason":"temporary migration variance",
    "expiresOn":"2025-10-31T00:00:00Z"
  }'
```

### Verdict store latency

1. Check read and write latency graphs and DB connection health
2. Verify partition maintenance and index bloat
3. Enable read from replica if primary is saturated
4. Escalate to database SRE if p95 over threshold for 15 minutes

## Remediation Procedures

**Pause promotions**
- Set pipeline flag to hold Bronze to Silver or Silver to Gold promotions for affected datasets
- Announce scope and expected duration in incident channel

**Scale evaluator**
- Increase concurrent workers by 1.5 times and re evaluate queue depth
- Revert to baseline after backlog clears

**Shadow mode for risky packs**
- Convert active pack to shadow when deny spikes are not explained by data changes
- Require five clean shadow runs before re activation

**Purge poisoned queue messages**
- Identify failed jobs with permanent errors
- Purge messages and re queue with corrected parameters

**Rollback rule pack**
- Activate previous version and document justification in change log

## Communication And Escalation

**Roles**
- Incident commander for Sev1 and Sev2
- Communications lead for stakeholder updates
- Domain owner for dataset level remediation
- Database SRE for verdict store incidents

**Escalation**
- Sev1 escalates to platform leadership after 30 minutes of impact
- Sev2 escalates to engineering manager if unresolved after 60 minutes
- Sev3 handled by on call with async updates

## Post Incident Requirements

- Timeline of detection, response, mitigation, and recovery
- Root cause and contributing factors
- Action items with owners and due dates
- Rule pack or evaluator changes linked to change management ticket
- Scorecard of model metrics before and after the incident

## Verification After Recovery

**Checklist**
- Validation failure rate returned to baseline
- Verdict store latency within SLO
- Scorecard lag under 15 minutes
- Waiver expiries under control with alerts cleared
- Promotions resumed and successful for two consecutive cycles
- Observability dashboards green for 30 minutes

## Runbook Shortcuts

- Quick links to dashboards and logs
- Common API calls with placeholders for dataset and stage
- Known good test datasets for smoke checks
- Template for incident updates

**Smoke check sample**
```bash
curl -s -X POST https://api.example.com/dqc/v1/validate   -H "Authorization: Bearer $TOKEN"   -d '{"dataset":"sales_enriched","stage":"silver","runId":"smoke"}'
curl -s "https://api.example.com/dqc/v1/verdicts/sales_enriched/silver"
```

## Appendices

**Sample rule failure payload**
```json
{
  "dataset":"finance_invoice",
  "stage":"silver",
  "rule":"referential_customer_id",
  "violations": 245,
  "status":"FAIL",
  "createdAt":"2025-10-09T12:40:00Z"
}
```

**Sample gate denial event**
```json
{"dataset":"finance_invoice","stage":"silver","promotionAllowed":false,"blockingRule":"referential_customer_id"}
```

## Summary

This runbook gives SREs and on call engineers a direct path from alert to diagnosis and resolution. It defines consistent procedures for evaluator failures, rule pack regressions, scorecard delays, and storage latency, with clear rollback strategies and communication patterns. By following this guide, teams can restore DQC service levels quickly and keep data promotions safe and auditable.

## Incident categories and severity

Use a stable error taxonomy that maps to severity and playbooks. For example, DQ-VAL-001 and DQ-VAL-002 are severity two, DQ-WVR-001 is severity three.

## First response

Collect run_id, dataset_id, layer, and rule_pack_id. Retrieve recent verdicts and scorecards. Inspect observability events around the run window. Check waiver status and expiry.
