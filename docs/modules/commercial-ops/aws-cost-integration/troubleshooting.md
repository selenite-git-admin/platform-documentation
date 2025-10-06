# Troubleshooting

## Overview

This document provides an operational playbook for diagnosing and recovering failures across the AWS Cost Integration subsystem of Commercial-Ops. It covers CUR ingestion, tag propagation, allocation, budgets and alerts, and reconciliation. The guidance is written for operators and finance-engineering users. All steps assume read access to the billing S3 bucket, Glue data catalog, Athena workgroup, CloudWatch logs, and the Commercial-Ops admin database.

The objective is to restore a healthy state without mutating closed financial periods. All corrective actions must preserve auditability. Where edits are necessary, use reversal entries instead of destructive updates.

## Failure Classification

| Area | Symptom | Primary Signals | Typical Root Cause |
|------|---------|-----------------|--------------------|
| CUR Ingestion | Missing or partial partitions | Glue partitions out of date, Athena row count drop | S3 delivery delay, Glue crawler failure, schema change |
| Tag Propagation | High untagged cost | `tag_coverage_pct` drop, CUR lines with null tenant_id | Provisioning pipeline regression, IAM deny on tag APIs |
| Allocation | Mismatch between pooled cost and allocated total | `fact_cost_allocated` sum < raw pool | Empty keys, zero denominator, rule version mismatch |
| Budgets/Alerts | Alerts not firing or delayed | No SNS/Email activity, stale `budget_master` | Refresh job failure, throttling, IAM policy changes |
| Reconciliation | Variance beyond tolerance | recon_summary status warning/failed | Timing lag, allocation gap, invoice rounding or FX drift |

## Quick Diagnostic Path

1. Confirm **period** and **scope**. Work only on the affected month and workgroup.
2. Check **freshness**: latest CUR partition date and `cur_ingestion_log` last run.
3. Inspect **tag coverage**: percentage drop or tenant spikes.
4. Validate **allocation**: pool vs. allocated totals by service.
5. Verify **invoice match**: allocated vs. invoiced per tenant.
6. Record a **recon snapshot** before changes.

## CUR Ingestion Issues

### Symptoms
- Expected partitions missing for the current month.
- Row counts fall sharply compared to previous days.
- New columns appear in Glue and ingestion fails on schema validation.

### Signals
- CloudWatch logs for ingestion Lambda or Batch show errors.
- `cur_ingestion_log.status = failed`.
- Athena query to CUR table returns zero rows for recent dates.

### Commands and Queries

Check latest partition dates:
```sql
SELECT MAX(bill_billing_period_start_date) AS latest_period_start,
       MAX(line_item_usage_start_date) AS latest_usage_ts
FROM cur_billing_master;
```

Compare expected vs ingested counts:
```sql
SELECT 'cur' AS src, COUNT(*) cnt
FROM cur_billing_master
WHERE bill_billing_period_start_date = :period_start
UNION ALL
SELECT 'raw' AS src, COUNT(*) cnt
FROM fact_cost_raw
WHERE bill_billing_period_start_date = :period_start;
```

Re-run ingestion for a specific period:
```bash
aws lambda invoke --function-name commercial-ops-cur-ingestion   --payload '{"period":"2025-09"}' /dev/stdout
```

Schema diffs (expected vs Glue):
```sql
-- Example: detect unexpected columns
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'cur_billing_master'
EXCEPT
SELECT column_name
FROM expected_cur_schema_vN;
```

### Recovery

1. If Glue partitions are stale, re-run the crawler or add partition explicitly.  
2. If schema added columns, apply **append-only** changes to `fact_cost_raw` (nullable fields) and re-run.  
3. If S3 delivery lag, mark period as **delayed** and continue with provisional reconciliation. Do not close the period until CUR completes.  
4. Always write the outcome to `cur_ingestion_log` with run ID and digest list.

## Tagging and Coverage Issues

### Symptoms
- Unallocated cost due to missing `user:tenant_id` or `user:plan_id`.
- Spike in operator-overhead due to untagged resources.
- Tenant usage visible in platform metrics but not in CUR.

### Signals
- `tag_coverage_pct` falls below target.
- `missing_tenant_tag` count rises in validation queries.

### Queries

Find untagged cost:
```sql
SELECT DATE_TRUNC('month', bill_billing_period_start_date) AS period,
       SUM(line_item_unblended_cost) AS untagged_usd
FROM fact_cost_raw
WHERE resource_tags_user_tenant_id IS NULL
  AND bill_billing_period_start_date BETWEEN :start AND :end
GROUP BY 1;
```

Drill by service/component:
```sql
SELECT product_servicecode,
       resource_tags_user_service_component,
       SUM(line_item_unblended_cost) AS usd
FROM fact_cost_raw
WHERE bill_billing_period_start_date BETWEEN :start AND :end
  AND (resource_tags_user_tenant_id IS NULL OR resource_tags_user_plan_id IS NULL)
GROUP BY 1,2
ORDER BY usd DESC;
```

### Recovery

1. Correct tagging at source via provisioning templates or runtime tagger.  
2. For the current open month, re-run CUR ingestion to pick up fixed tags.  
3. For closed months, do **not** mutate historical CUR-derived records; record a variance note and, if necessary, allocate via a one-time rule with evidence.  
4. Raise a preventive ticket to add tag validation to the CI pipeline.

## Allocation Failures

### Symptoms
- `fact_cost_allocated` totals are less than the pooled raw costs.
- Tenants with known usage receive zero allocation.
- Allocation run fails due to division by zero.

### Signals
- Allocation job logs show zero denominator or empty key set.
- `allocation_rules` effective version changed mid-month without run notes.

### Queries

Pool vs allocated by service:
```sql
WITH pool AS (
  SELECT DATE_TRUNC('month', bill_billing_period_start_date) AS period,
         product_servicecode AS service,
         SUM(line_item_unblended_cost) AS pool_usd
  FROM fact_cost_raw
  WHERE bill_billing_period_start_date BETWEEN :start AND :end
  GROUP BY 1,2
),
alloc AS (
  SELECT period_start AS period, service, SUM(allocated_cost_usd) AS alloc_usd
  FROM fact_cost_allocated
  WHERE period_start BETWEEN :start AND :end
  GROUP BY 1,2
)
SELECT p.period, p.service, p.pool_usd, COALESCE(a.alloc_usd,0) AS alloc_usd,
       (COALESCE(a.alloc_usd,0) - p.pool_usd) AS delta_usd
FROM pool p
LEFT JOIN alloc a ON a.period = p.period AND a.service = p.service
ORDER BY p.period, p.service;
```

Check empty keys:
```sql
SELECT period_start, SUM(key_total) AS key_total
FROM fact_cost_allocated
WHERE period_start BETWEEN :start AND :end
GROUP BY 1
HAVING SUM(key_total) = 0;
```

### Recovery

1. Confirm the **allocation key** source tables populated (for example `tenant_network_usage`).  
2. If key totals are zero, reprocess the usage key pipeline for the period, then re-run allocation.  
3. If rule version changed mid-cycle, re-run allocation with the earlier **effective_from** version and write reversals for the erroneous run.  
4. Document evidence links for each re-run in the allocation run log.

## Budgets and Alerts Issues

### Symptoms
- No alerts despite thresholds crossed in dashboard.  
- Budget numbers not updating daily.  
- Slack or SNS notifications missing.

### Signals
- `budget_master.last_refreshed_at` stale.  
- CloudWatch Lambda errors for budget refresh job.  
- SNS topic or subscription permissions changed.

### Queries

Refresh staleness:
```sql
SELECT budget_id, scope_type, last_refreshed_at
FROM budget_master
ORDER BY last_refreshed_at ASC
LIMIT 20;
```

Check projected overrun:
```sql
SELECT budget_id, actual_usd, target_usd,
       CASE WHEN actual_usd >= target_usd*0.95 THEN 'critical'
            WHEN actual_usd >= target_usd*0.80 THEN 'warning'
            ELSE 'ok' END AS level
FROM budget_master;
```

### Recovery

1. Re-run the budget refresh Lambda and check CloudWatch execution logs.  
2. Validate SNS topic policy and email integration. Re-subscribe if necessary.  
3. If AWS Budgets API quotas are throttled, stagger calls or cache CUR-derived aggregates in Aurora.  
4. Ensure alert deduplication does not silence legitimate repeats; check alert state tables.

## Reconciliation Variances

### Symptoms
- recon_summary status failed; variance above threshold.  
- Persistent invoice mismatch for one tenant.  
- Large timing gap between CUR and invoices.

### Queries

Cur vs allocated vs invoiced:
```sql
SELECT s.period_start,
       s.aws_total_usd, s.allocated_total_usd, s.invoiced_total_usd,
       s.variance_usd, s.variance_pct, s.status
FROM recon_summary s
WHERE s.period_start BETWEEN :start AND :end
ORDER BY s.period_start DESC;
```

Tenant-level drill:
```sql
SELECT a.tenant_id, a.period_start,
       SUM(a.allocated_cost_usd) AS alloc_usd,
       SUM(i.amount_usd) AS inv_usd,
       (SUM(i.amount_usd) - SUM(a.allocated_cost_usd)) AS delta_usd
FROM fact_cost_allocated a
LEFT JOIN invoice_detail i
  ON a.tenant_id = i.tenant_id AND a.period_start = i.period_start
WHERE a.period_start BETWEEN :start AND :end
GROUP BY a.tenant_id, a.period_start
ORDER BY a.period_start DESC, delta_usd DESC;
```

### Recovery

1. If variance due to timing lag, mark the recon run as **provisional** and re-run after the next CUR delivery.  
2. If allocation gap, re-run allocation for the period with corrected keys or rules; write reversals for prior incorrect allocations.  
3. If invoice rounding or FX variance, validate policy configuration and rerender the invoice with corrected rules; do not mutate the closed invoice without a credit note and reissue.  
4. Record the decision and evidence in `recon_exceptions` and attach links to the recon report.

## Safe Re-run and Rollback Policy

- All re-runs must be **idempotent** using a unique `run_id`.  
- Use **reversal entries** for corrections; never delete closed-period rows.  
- Store a **snapshot** of inputs and SQL text in the evidence store before action.  
- After a re-run, generate a new reconciliation summary and compare variance trend.

## Preventive Controls Checklist

| Control | Target | Check |
|--------|--------|-------|
| Glue crawler schedule | Daily | Crawler last run succeeded |
| CUR delivery lag watch | < 48h | Partition monitor alarms |
| Tag coverage | 100% | Daily validation job green |
| Allocation key freshness | < 24h | Key pipelines healthy |
| Budget refresh | Daily 04:00 UTC | Lambda success + SNS throughput |
| Recon lock | After CUR final | Period lock policy enforced |

## Escalation

- P1: Reconciliation failed on month close. Notify finance lead and platform on-call; freeze new invoices.  
- P2: Allocation mismatch > 2% in open period. Notify billing-ops; investigate keys and rules.  
- P3: Tag coverage < 98% for > 24h. Notify platform team; fix provisioning or runtime tagger.

## Reference CLI Snippets

List active cost allocation tags:
```bash
aws ce list-cost-allocation-tags --status active
```

Get Athena query execution status:
```bash
aws athena get-query-execution --query-execution-id <id>
```

Re-run Glue crawler:
```bash
aws glue start-crawler --name commercial-ops-cur-crawler
```

Invoke allocation job:
```bash
aws lambda invoke --function-name commercial-ops-allocation   --payload '{"period":"2025-09"}' /dev/stdout
```

## Cross References

- **cur-ingestion.md** for ingestion design and runbook steps.  
- **tag-strategy.md** for tag schema and validation.  
- **allocation-rules.md** for pooling and split formulas.  
- **budgets-alerts.md** for thresholds and alert channels.  
- **reconciliation.md** for variance policy and evidence logging.
