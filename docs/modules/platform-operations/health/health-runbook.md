# Health Runbook

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Provide operators with a consistent incident response and recovery process for service and data health degradation. The runbook focuses on Lambda + API Gateway deployments and assumes the use of SQS and CloudWatch for monitoring and alerting.

---

## Incident taxonomy

| Category | Definition | Typical Severity |
|---|---|---|
| **Liveness failure** | `/healthz` returns 500 or no response | P1 |
| **Readiness degradation** | `/readyz` returns 503 or critical dependency fails | P1–P2 |
| **Startup stall** | `/startupz` remains failing >10 min after deploy | P2 |
| **Data freshness failure** | `/dataz` shows core dataset late or invalid | P1 |
| **Fleet partial readiness** | <90% of services ready in `/fleet/readyz` | P2 |
| **Metrics unreported** | `/metrics` endpoint not scraped for >10 min | P3 |
| **Synthetic probe mismatch** | External check contradicts internal readiness | P2 |

---

## Detection sources
- **CloudWatch alarms** tied to readiness error rate, latency, and missing metrics
- **Data Health SLO monitor** on data freshness lag
- **Lambda error rate / throttling alarms**
- **Notifications module alerts** (email and Slack)
- **Fleet dashboard** visualizing readiness across services

---

## Response workflow

### 1. Identify scope
Check the alert payload or dashboard for:
- Service name
- Region and environment
- Probe (`readyz`, `dataz`, etc.)
- Correlation ID (trace)

If multiple services fail together, suspect shared dependencies (e.g., RDS, Secrets Manager, or SQS).

### 2. Verify impact
Run these checks:

```bash
curl -sS https://<service>/healthz
curl -sS https://<service>/readyz
curl -sS https://<service>/dataz
```

Then confirm in CloudWatch:
- Log group: `/aws/lambda/<function_name>`
- Metrics: `Errors`, `Duration`, `Throttles`

### 3. Contain
- Stop new Lambda deployments if readiness failures are caused by new builds.
- Drain incoming SQS queues if workers are unhealthy.
- Temporarily route traffic away in API Gateway (deploy previous stage if required).

### 4. Diagnose

| Failure Type | Common Causes | Diagnostic Steps |
|---|---|---|
| **Liveness** | Out of memory, crash loop | Check Lambda logs, memory usage, cold starts |
| **Readiness** | DB/network/secrets issue | Review dependency checks in logs |
| **Startup** | Migration pending, circular dependency | Verify DB schema readiness and startup events |
| **Data freshness** | Stuck pipeline, failed dataset ingestion | Check DRR entries and runner logs |
| **Fleet rollup** | Aggregator job failed | Check CloudWatch logs for aggregator Lambda |

Check the **Evidence Ledger** for correlated incidents or dependency SLAs.

### 5. Recover
Depending on diagnosis:

**Lambda runtime:**
```bash
aws lambda update-function-configuration --function-name <fn> --memory-size 512
aws lambda publish-version --function-name <fn>
aws lambda update-alias --function-name <fn> --name live --function-version <version>
```

**Restart aggregator Lambda**
```bash
aws lambda invoke --function-name health-aggregator --payload '{}' /dev/null
```

**Re-trigger data validation**
```bash
aws sqs send-message --queue-url <data_health_queue> --message-body '{"action":"validate"}'
```

### 6. Validate
Ensure `/readyz` and `/dataz` return `ok`.
Check dashboards for stable latency and no open SLO violations.

### 7. Close incident
- Update `health_sla_violation` record to `closed`
- Attach root cause and mitigation note
- Notify stakeholders through the Notifications module

---

## Recovery time targets

| Metric | Target |
|---|---|
| Liveness recovery | < 5 minutes |
| Readiness recovery | < 15 minutes |
| Data freshness recovery | < 30 minutes |
| Fleet readiness recovery | < 15 minutes |
| Startup completion | < 10 minutes |

---

## Preventive actions
- Enforce dependency timeouts < 5 seconds
- Add retry + exponential backoff for transient failures
- Maintain warm pool of Lambda workers for core services
- Enable alarms for data lag > 30 minutes
- Run chaos tests quarterly

---

## Escalation policy

| Severity | Response Time | Escalate To | Channels |
|---|---|---|---|
| P1 | 15 min | Platform On-call | Pager, Slack |
| P2 | 30 min | Service Owner | Slack |
| P3 | 4 hr | Module Owner | Email |

---

## Audit evidence
Every incident produces a row in **health_sla_violation** and a linked entry in **Evidence Ledger** with hash, timestamp, and user who closed the record.

---

## Example diagnostic checklist

| Step | Command | Expected |
|---|---|---|
| Verify readiness | `curl /readyz` | JSON with `"status":"ok"` |
| Trace failures | `aws logs tail /aws/lambda/<fn>` | See root cause |
| Check dependency | `aws rds describe-db-instances` | DB available |
| Validate dataset | SQL query on `data_health_log` | No `"status":"late"` entries |
| Confirm dashboards | Open Grafana health overview | Green service tiles |

---

## Summary
This runbook gives operators a short, repeatable path to detect, diagnose, and fix service or data health issues. It minimizes noise, speeds recovery, and ensures consistent closure and evidence recording for audits.