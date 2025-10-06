# Runbook

## Overview

This runbook provides operational guidance for diagnosing and resolving issues in the Commercial-Ops subsystem. It complements the Observability module by mapping alert IDs, logs, and queries to prescriptive actions. All procedures assume AWS-native infrastructure with CloudWatch, Lambda, Glue, and Aurora as the execution environment.

---

## 1. CUR Ingestion Issues

### Symptoms
- CloudWatch alarm `cur-freshness` triggered
- `fact_cost_raw` partition missing or outdated
- Glue job duration > 30 minutes or fails with `AccessDenied`

### Diagnostic Steps
1. Confirm S3 partition presence for the current billing cycle:
   ```bash
   aws s3 ls s3://cur-bucket/cur-prefix/2025-09/
   ```
2. Run Athena validation:
   ```sql
   SELECT MAX(line_item_usage_end_date) FROM fact_cost_raw;
   ```
3. Check CloudWatch logs for ingestion Lambda:
   ```bash
   aws logs tail /aws/lambda/commercial-ops-cur-ingestion --since 1h
   ```

### Resolution
- If S3 path missing → trigger AWS CUR delivery manually or verify account link.
- If Glue job fails → re-run job with:
  ```bash
  aws glue start-job-run --job-name cur_ingest_prod
  ```
- Validate CUR IAM role has `s3:GetObject` and `athena:StartQueryExecution` permissions.

---

## 2. Allocation Failures

### Symptoms
- Alarm `allocation-variance` or `allocation-variance-critical`
- Variance > 0.5% by service
- Missing cost lines in `fact_cost_allocated`

### Diagnostic Steps
1. Identify affected service(s):
   ```sql
   SELECT service, variance_pct FROM recon_summary WHERE status='warning';
   ```
2. Compare raw vs allocated totals:
   ```sql
   SELECT * FROM recon_exceptions WHERE category='Allocation';
   ```
3. Inspect allocation rules in `rule_version_map`.

### Resolution
- Rerun allocation pipeline:
  ```bash
  aws lambda invoke --function-name allocation_runner
  ```
- If tagging gap detected, run tagging sync job.
- Verify `plan_metric_map` aligns with allocation rules.
- Escalate to FinOps if persistent >1% variance.

---

## 3. Budget and Alerts

### Symptoms
- Dashboard shows “Budget data stale”
- CloudWatch alarm `budget-stale`
- `budget_master.last_refreshed_at` older than 24h

### Diagnostic Steps
```sql
SELECT budget_id, last_refreshed_at FROM budget_master ORDER BY last_refreshed_at ASC;
```
Check Lambda logs:
```bash
aws logs tail /aws/lambda/budget-refresh --since 2h
```

### Resolution
- Re-run budget refresh Lambda:
  ```bash
  aws lambda invoke --function-name budget_refresh_prod
  ```
- Verify SNS topics exist and subscriptions are active:
  ```bash
  aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:...:tenant-budget-alerts
  ```

---

## 4. Reconciliation Variances

### Symptoms
- Reconciliation job status `failed`
- `variance_pct` > 1%
- Invoice issuance blocked

### Diagnostic Steps
```sql
SELECT * FROM recon_summary ORDER BY period_start DESC LIMIT 5;
SELECT * FROM recon_exceptions WHERE recon_id='RECON-2025-09';
```

### Resolution
- Validate upstream allocation totals.
- Manually reconcile differences using finance ops console.
- Rerun reconciliation job:
  ```bash
  aws lambda invoke --function-name recon_runner
  ```
- Mark as resolved in `recon_summary` once balance achieved.

---

## 5. Tagging and Coverage

### Symptoms
- Alarm `tag-coverage-drop`
- Missing `resource_tags_user_tenant_id` in `fact_cost_raw`
- Quarantined resource pool increase

### Diagnostic Steps
```sql
SELECT COUNT(*) FILTER (WHERE resource_tags_user_tenant_id IS NULL) AS untagged,
       COUNT(*) AS total,
       ROUND(100.0 * COUNT(*) FILTER (WHERE resource_tags_user_tenant_id IS NOT NULL) / COUNT(*), 2) AS tag_coverage_pct
FROM fact_cost_raw;
```

### Resolution
- Trigger tagging validation job:
  ```bash
  aws lambda invoke --function-name tag_validator
  ```
- Notify provisioning service for non-compliant resources.
- Update tag enforcement policy in AWS Config.

---

## 6. Invoice Generation

### Symptoms
- Alarm `invoice-lag`
- Missing invoice in `invoice_header` for current cycle
- Job `invoice_emitter` failed

### Diagnostic Steps
1. Check job logs:
   ```bash
   aws logs tail /aws/lambda/invoice_emitter --since 1h
   ```
2. Validate pending invoices:
   ```sql
   SELECT tenant_id, period_start, status FROM invoice_header WHERE status='open';
   ```

### Resolution
- Rerun emitter Lambda for affected tenant:
  ```bash
  aws lambda invoke --function-name invoice_emitter --payload '{"tenant_id": "TEN-00123"}'
  ```
- Ensure downstream reconciliation has succeeded before issuing.
- If repeated failure → verify `usage_snapshot_daily` completeness.

---

## 7. Payment Reconciliation

### Symptoms
- Payments not reflected in `invoice_header.status`
- Exception `PAYMENT_MISMATCH` in logs

### Diagnostic Steps
```sql
SELECT i.invoice_id, i.status, p.payment_id, p.status, p.amount_usd
FROM invoice_header i
LEFT JOIN payment_txn p ON p.invoice_id=i.invoice_id
WHERE i.status!='paid';
```

### Resolution
- Manually match transactions in finance portal.
- If bank webhook missing → reprocess event from queue.
- Correct mismatched totals and update invoice to `paid`.

---

## 8. Storage and Egress Quotas

### Symptoms
- Tenants exceeding storage/egress caps
- UI shows `quota reached`

### Diagnostic Steps
```sql
SELECT tenant_id, metric_code, metric_value, cap_value, utilization
FROM usage_snapshot_daily WHERE utilization >= 1.0;
```

### Resolution
- Notify tenant for plan upgrade.
- Apply top-up automatically if configured.
- Confirm dashboard refresh after update.

---

## 9. Runner Capacity Issues

### Symptoms
- Runner job queue backlog > threshold
- Lambda logs show `ThrottlingException`

### Diagnostic Steps
```bash
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization   --dimensions Name=InstanceId,Value=i-0123456789abcdef0 --start-time $(date -u -d '-10 minutes' +%Y-%m-%dT%H:%M:%SZ)   --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 60 --statistics Average
```

### Resolution
- Scale up EC2 runner ASG capacity.
- Validate NAT Gateway throughput not limiting PrivateLink.
- Schedule background jobs in off-peak hours.

---

## 10. General Recovery Commands

```bash
# Restart core Lambdas
aws lambda update-function-configuration --function-name cur_ingestion --environment Variables={RESTART=true}
aws lambda update-function-configuration --function-name allocation_runner --environment Variables={RESTART=true}

# Force refresh dashboards
aws lambda invoke --function-name dashboard_refresher

# Verify audit logs
aws logs tail /aws/lambda/audit-event-writer --since 1h
```

---

## 11. Escalation Path

| Severity | Time to Acknowledge | Action |
|-----------|--------------------|--------|
| SEV-1 | 15 min | Notify SRE and FinOps immediately |
| SEV-2 | 1 h | Open Jira incident and link evidence |
| SEV-3 | 4 h | Track via daily report |
| SEV-4 | 1 day | Add to maintenance backlog |

---

## 12. Postmortem Requirements

- Every SEV-1 or SEV-2 incident requires a postmortem within 48 hours.
- Include root cause, impact, and prevention actions.
- Store postmortems under `/ops/postmortems/<YYYY-MM-DD>` with evidence links and SQL exports.

---

## Cross References

- observability.md
- aws-cost-integration/troubleshooting.md
- aws-cost-integration/cur-ingestion.md
- aws-cost-integration/reconciliation.md
- data-model.md
