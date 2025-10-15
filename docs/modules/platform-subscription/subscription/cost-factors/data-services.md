# Cost Factors: Data-Services

## Overview

This document explains data-related cost drivers that influence plan evaluation and tenant billing. It aligns metric semantics with AWS cost origins and defines guardrails that ensure predictable spend. Currency defaults to USD. The canonical entities are tenant and plan.

The data-services domain covers ingestion, transformation, storage, retention, and egress. Tenant dashboards publish only totals. Operator views include AWS service specifics for reconciliation.

## Objectives

- Identify the metrics that govern data costs and their aggregation rules.
- Describe how platform data classes map to AWS storage and transfer charges.
- Provide estimation guidance that is reproducible from platform telemetry.
- Define guardrails for retention, compaction, snapshots, and egress quotas.
- Document edge cases and operational controls.

## Metrics

| Metric code | Unit | Aggregation | Description | Tenant visibility |
|-------------|------|-------------|-------------|-------------------|
| `data_ingestion_gb` | GB | Sum daily | Accepted raw and processed input volume | Visible |
| `data_transformed_gb` | GB | Sum daily | Post-transform outputs persisted to lake or warehouse | Operator |
| `storage_gb_peak` | GB | Peak monthly | Maximum retained storage footprint during cycle, includes snapshots and backups | Visible |
| `snapshot_storage_gb` | GB | Peak monthly | Snapshot share included in storage peak | Operator |
| `egress_gb` | GB | Sum daily with published monthly quota | Total outbound data served to public internet or cross region | Visible |
| `glacier_archive_gb` | GB | Peak monthly | Cold tier archive footprint if enabled | Operator |

## Mapping to AWS Charges

| Platform component | AWS service | CUR keys | Notes |
|--------------------|------------|----------|-------|
| Data lake objects | AmazonS3 | `product_servicecode='AmazonS3' AND line_item_usage_type LIKE '%TimedStorage%'` | Standard storage; lifecycle transitions apply |
| Data lake requests | AmazonS3 | `line_item_usage_type LIKE '%-Requests%' OR line_item_usage_type LIKE '%Request-Tier%'` | Request charges where relevant |
| Warehouse volumes | AmazonEC2 EBS | `line_item_usage_type LIKE 'EBS:%'` | If warehouse runs on EC2 instances |
| Snapshots | EBS Snapshot or S3 | `EBS:SnapshotUsage`, `EBS:SnapshotDataTransfer` | Counted in `storage_gb_peak` |
| Archive tier | S3 Glacier | `GlacierStorage` and retrieval request types | Retrieval may incur fees |
| Data transfer out | AWSDataTransfer or S3 | `%-Out-Bytes%` | Validates `egress_gb` |
| Cross region replication | S3 | `CrossRegionDataTransfer` | Operator policy dependent |

The tenant UI masks AWS service names. Operators can drill into service and usage-type level evidence during reconciliation.

## Data Classes and Retention

Data is organized into classes. Classes control lifecycle, compaction, and replication behavior.

| Class | Intended use | Default retention | Lifecycle | Notes |
|------|--------------|-------------------|-----------|------|
| Bronze | Raw ingestion | 90 days | Standard to Infrequent Access at 30 days | No schema enforcement |
| Silver | Cleaned and modeled | 180 days | Standard | Partitioned for scan efficiency |
| Gold | Ready for analytics | 365 days | Standard | Strong schema and audit constraints |
| Archive | Long-term compliance | 3 to 7 years | Glacier | Retrieval fees apply |

Retention acts on object tags and manifests. Deletions and transitions are recorded in an audit table for change control.

## Storage Accounting

`storage_gb_peak` counts the maximum logical footprint per billing cycle. The footprint includes live objects, compaction overhead during merge windows, and snapshots. Snapshots always count toward storage peak.

```sql
-- Compute peak data-store within the active billing cycle
INSERT INTO tenant_usage_snapshot_daily (tenant_id, metric_code, metric_value, usage_date)
SELECT tenant_id, 'storage_gb_peak' AS metric_code,
       MAX(storage_used_gb) AS metric_value,
       CURRENT_DATE AS usage_date
FROM tenant_storage_monitor
WHERE usage_date >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY tenant_id;
```

Compaction windows should be sized so that peak does not exceed 1.3x of steady-state unless explicitly approved. Compaction policies must be documented per dataset with start and end timestamps.

## Egress Quota and Estimation

The platform publishes an egress quota per plan. The dashboard shows only the total tenant egress. Estimation uses platform telemetry with CUR validation as a backstop.

Telemetry rollup:

```sql
SELECT tenant_id,
       SUM(bytes_out) / 1024 / 1024 / 1024 AS egress_gb,
       DATE(usage_ts) AS usage_date
FROM network_flow_logs
WHERE tenant_id = :tenant
  AND usage_ts BETWEEN :start AND :end
GROUP BY tenant_id, DATE(usage_ts);
```

Validation against CUR:

```sql
SELECT SUM(line_item_usage_amount) / 1024 / 1024 / 1024 AS cur_egress_gb
FROM fact_cost_raw
WHERE product_servicecode IN ('AmazonS3','AWSDataTransfer')
  AND line_item_usage_type LIKE '%-Out-Bytes%'
  AND resource_tags_user_tenant_id = :tenant
  AND bill_billing_period_start_date BETWEEN :period_start AND :period_end;
```

Variance tolerance is set at plus or minus 5 percent for egress. Discrepancies above threshold open a reconciliation exception. Tenant presentation uses totals only and does not show per service splits.

## Lifecycle and Tiering

Lifecycle rules reduce storage cost by moving infrequently accessed objects to lower-cost tiers. Transitions are controlled by class policy and confirmed by storage audits.

```json
{
  "Rules": [
    {
      "ID": "bronze-to-ia-30",
      "Filter": { "Tag": { "Key": "class", "Value": "bronze" } },
      "Status": "Enabled",
      "Transitions": [{ "Days": 30, "StorageClass": "STANDARD_IA" }],
      "Expiration": { "Days": 90 }
    }
  ]
}
```

Lifecycle changes are coordinated with analytics teams to avoid surprise retrieval costs. Retrieval operations must be acknowledged by the tenant admin when Archive class is involved.

## Estimation Cheat Sheet

| Driver | Approximation method | Caveat |
|--------|----------------------|--------|
| Ingestion | Sum of accepted payloads from ingestion logs | Compression may vary |
| Storage peak | Max daily `storage_used_gb` during cycle | Include compaction and snapshot windows |
| Egress | Sum of tenant flow logs out bytes | Validate against CUR when available |
| Glacier | Sum of archived object sizes | Retrieval fees not included in estimate |

## Guardrails

- Snapshots always count toward `storage_gb_peak`.
- Cross-account sharing requires explicit operator approval.
- Replication must tag destination with the same tenant and plan identifiers.
- Large backfills should run off-peak with temporary compaction limits.
- Archive retrievals require acknowledgment of retrieval cost and expected timeline.

## Operator Controls

Operators can set per-tenant caps and throttles to protect the shared platform.

| Control | Target | Effect |
|--------|--------|-------|
| Ingestion rate limit | Tenant | Back-pressure on accepted payloads |
| Storage freeze | Dataset | Block writes when cap exceeded |
| Egress throttle | Tenant | Rate limit outbound data |
| Archive approval | Tenant | Require approval for bulk restore |

## Cross References

- metrics-definition.md for canonical metric rules.
- aws-cost-mapping.md for CUR correlation.
- plan-parameters.md for caps and thresholds.
- dashboard-design.md for gauges and trend charts.
- reconciliation.md for variance policy.
