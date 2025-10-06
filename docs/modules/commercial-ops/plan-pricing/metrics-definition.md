# Metrics Definition

## Overview

Metrics are the atomic units of commercial evaluation within Commercial-Ops.  
Every cost calculation, quota, and dashboard visualization originates from a defined metric.  
Each metric represents a measurable quantity of tenant activity such as data ingestion, storage, egress, compute runtime, or licensed seat usage.  

Metrics unify operational telemetry with AWS financial data. They translate raw service consumption into standardized, timestamped quantities that can be evaluated against subscription plans and validated through AWS Cost and Usage Reports.  
This common language ensures deterministic pricing, transparent reporting, and predictable scaling across tenants and workloads.

The metric layer functions as a stable contract between engineering systems, commercial plans, and financial reconciliation.

## Purpose and Role

Metrics bridge the technical and financial layers of the platform.  
Operational telemetry describes what the system did. AWS billing data describes what it cost.  
Metrics define how that activity is measured, aggregated, and exposed so that both can be compared without ambiguity.

Within the Commercial-Ops model:

- Metrics feed plan evaluation and quota enforcement.  
- Metrics drive tenant dashboards and usage alerts.  
- Metrics power AWS cost allocation validation and forecasting.  
- Metrics define contractual boundaries for each plan (CFO, COO, CGO, or custom).  

Each metric belongs to exactly one domain and follows consistent rules for units, time windows, and aggregation.

## Metric Taxonomy

Metrics are classified by functional domain and by visibility scope.  
Each category has a consistent set of attributes: unit, aggregation rule, visibility, and refresh cycle.

| Category | Example Metrics | Unit | Aggregation | Visibility | Description |
|-----------|----------------|------|--------------|-------------|-------------|
| **Data** | `data_ingestion_gb`, `data_transformed_gb`, `data_retained_gb`, `storage_gb_peak`, `snapshot_storage_gb` | GB | Sum daily, Peak monthly | Tenant | Represents data volume flowing through ingestion, transformation, and retention layers. |
| **Compute** | `runner_hours`, `runner_idle_hours`, `runner_active_hours`, `lambda_invocations`, `cpu_core_hours` | Hour | Sum daily | Tenant | Measures execution time or compute resource usage for scheduled and triggered workloads. |
| **Networking** | `egress_gb`, `intra_vpc_transfer_gb`, `private_link_transfer_gb`, `vpn_transfer_gb` | GB | Peak monthly | Tenant | Tracks network traffic leaving or traversing private environments. |
| **Seats** | `active_users`, `provisioned_users`, `api_keys_used` | Count | Max monthly | Tenant | Represents licensed user access and API credentials under a plan. |
| **Auxiliary** | `cur_allocated_cost`, `shared_resource_cost`, `unallocated_cost_pending`, `allocation_variance_pct` | USD | Sum monthly | Operator | Used for reconciliation, validation, and allocation control; not exposed to tenants. |
| **System** | `tag_coverage_pct`, `metric_refresh_latency_min`, `reconciliation_delay_hours` | % / Hours | Max daily | Operator | Monitors Commercial-Ops system health, ensuring tag integrity and timely data refresh. |

## Metric Lifecycle

The lifecycle of a metric follows a controlled, auditable path from capture to validation.

```mermaid
flowchart LR
  A[Telemetry Source] --> B[Normalization Rules]
  B --> C[Aggregation Pipeline]
  C --> D[Metric Catalog Registration]
  D --> E[Plan Evaluation Engine]
  E --> F[AWS CUR Validation]
  F --> G[Reporting & Dashboards]
```

1. **Capture** Metrics originate from platform telemetry or AWS usage data.  
2. **Normalization** Values are converted into canonical units such as GB, hours, or count.  
3. **Aggregation** Rules define how data is summarized (sum, max, average, peak).  
4. **Registration** The metric is recorded in the catalog with metadata, domain, and ownership.  
5. **Evaluation** Plan engine consumes metric data for quota and billing evaluation.  
6. **Validation** AWS Cost and Usage Reports confirm totals, allocation, and accuracy.  
7. **Publication** Tenant dashboards and invoices reference these validated metrics.

## Standardization Rules

All metrics adhere to strict normalization and governance rules to ensure comparability across tenants and time periods.

| Rule | Description |
|------|--------------|
| **Units** | Must be expressed in standard SI units. Data in GB, compute in hours, cost in USD, and counts as integers. |
| **Timestamps** | Always recorded in UTC with ISO 8601 format. Aggregations follow daily and monthly boundaries. |
| **Aggregation windows** | Defined at metric level: daily sum, monthly peak, or rolling average. |
| **Visibility** | Each metric is tagged as `tenant` or `operator`. Tenant-visible metrics appear in dashboards; operator-only metrics are for validation. |
| **Versioning** | Any change to unit, aggregation, or semantic meaning creates a new metric code with backward-compatible mapping. |
| **Retention** | Metric history is retained for 13 months minimum for variance and audit analysis. |
| **Reversals** | Corrections are logged as negative deltas referencing original metric IDs; no overwrites. |

### Example YAML Registration

```yaml
metric_code: data_ingestion_gb
domain: data
unit: GB
aggregation: sum_daily
visibility: tenant
source: platform_telemetry
owner_team: platform-data
retention_days: 395
effective_date: 2025-01-01
status: active
```

## Metric Derivation Logic

Derived metrics are computed through lightweight aggregation or transformation pipelines.  
These pipelines execute within the data platform using SQL or Python functions and produce daily records stored in `tenant_usage_snapshot_daily`.

Example SQL for `storage_gb_peak`:

```sql
INSERT INTO tenant_usage_snapshot_daily (tenant_id, metric_code, metric_value, usage_date)
SELECT
    tenant_id,
    'storage_gb_peak' AS metric_code,
    MAX(storage_used_gb) AS metric_value,
    CURRENT_DATE AS usage_date
FROM tenant_storage_monitor
WHERE usage_date >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY tenant_id;
```

Example derived metric `egress_gb` with tagging filter:

```sql
SELECT
    tenant_id,
    SUM(bytes_out) / 1024 / 1024 / 1024 AS egress_gb
FROM network_flow_logs
WHERE tag_tenant_id IS NOT NULL
GROUP BY tenant_id;
```

## Example Metrics Catalog Extract

| Metric Code | Domain | Unit | Aggregation | Source | Visibility | Description |
|--------------|---------|------|--------------|----------|-------------|-------------|
| data_ingestion_gb | Data | GB | Sum daily | Platform telemetry | Tenant | Total volume ingested into data lake during the day. |
| data_retained_gb | Data | GB | Peak monthly | Storage system | Tenant | Maximum retained dataset size after transformations. |
| snapshot_storage_gb | Data | GB | Peak monthly | Storage system | Tenant | Includes snapshots and backups; counts toward storage quota. |
| runner_hours | Compute | Hour | Sum daily | Runner logs | Tenant | Total runtime hours consumed by scheduled jobs. |
| runner_idle_hours | Compute | Hour | Sum daily | Runner logs | Tenant | Idle compute hours reserved but unused. |
| lambda_invocations | Compute | Count | Sum daily | AWS Lambda logs | Operator | Number of function invocations for auxiliary processes. |
| egress_gb | Networking | GB | Sum daily | Flow logs | Tenant | Total outbound network traffic volume. |
| private_link_transfer_gb | Networking | GB | Sum daily | AWS VPC logs | Operator | Data transferred through PrivateLink endpoints. |
| active_users | Seats | Count | Max monthly | Identity service | Tenant | Number of active authenticated users under plan. |
| cur_allocated_cost | Auxiliary | USD | Sum monthly | AWS CUR | Operator | Tenant’s share of AWS billed cost based on allocation rules. |
| tag_coverage_pct | System | % | Max daily | Cost audit job | Operator | Percentage of AWS resources correctly tagged. |

## Governance and Ownership

Metrics are managed under strict data governance policies.  
The **Commercial Data Governance Board (CDGB)** owns the metric catalog and reviews any proposed additions or changes.  
Changes follow the versioning process below:

1. Proposal submitted via change request with business justification.  
2. Technical and financial impact assessed by platform and finance leads.  
3. Approved changes merged into the metric catalog repository.  
4. Effective date and version recorded in `dim_metric_catalog_history`.  

Deprecated metrics remain archived for 24 months.  
No metric is deleted from the catalog; deprecation marks it inactive and removes it from dashboards.

Ownership is shared across three layers:
- Platform engineering defines source and extraction logic.  
- Commercial-Ops defines semantic meaning and quota impact.  
- Finance defines alignment with AWS CUR and reporting standards.

## Cross References

- **aws-cost-mapping.md** for mapping metrics to AWS CUR dimensions and cost categories.  
- **plan-parameters.md** for threshold, quota, and evaluation logic.  
- **data-model.md** for entity schemas (`dim_metric_catalog`, `tenant_usage_snapshot_daily`, `fact_metric_history`).  
- **observability.md** for metric freshness, drift alerts, and reconciliation dashboards.
