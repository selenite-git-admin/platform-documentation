# Cost Factors: Compute-Networking

## Overview

This document describes compute and networking cost drivers and how they interact with plan parameters, tenant visible metrics, and AWS cost reconciliation. Compute is exposed to tenants as Runner tiers. Networking includes NAT Gateway, PrivateLink, VPC endpoints, and internet egress. The UI masks AWS service names while the operator view retains full detail for audit. Currency defaults to USD. Canonical entities are tenant and plan.

## Objectives

- Define metrics and aggregation for compute time and network processing.
- Map Runner tiers and network paths to AWS services and CUR usage types.
- Provide estimation guidance for scheduling and always on runners.
- Establish guardrails for NAT, PrivateLink, and egress behavior.
- Document example top ups and upgrade triggers tied to utilization.

## Metrics

| Metric code | Unit | Aggregation | Description | Tenant visibility |
|-------------|------|-------------|-------------|-------------------|
| `runner_hours` | Hour | Sum daily | Execution time across Runner tiers | Visible |
| `runner_idle_hours` | Hour | Sum daily | Provisioned but idle capacity | Operator |
| `cpu_core_hours` | Hour | Sum daily | Optional for advanced reporting | Operator |
| `nat_gb_processed` | GB | Sum daily | Bytes processed via NAT | Visible in operator reports |
| `privatelink_gb_processed` | GB | Sum daily | Bytes processed through PrivateLink endpoints | Operator |
| `egress_gb` | GB | Sum daily | Internet and cross region transfer | Visible |

## Runner Tiers

Runner tiers provide tenant friendly names over EC2 instance families. Allocation and mapping retain the original AWS details for audit, but the UI exposes only tier names.

| Tier | Intended workload | Internal mapping hint |
|------|-------------------|-----------------------|
| Light | General pipelines and small batches | t or m small to medium |
| Pro | Performance sensitive jobs | c or m medium to large |
| Enterprise | Memory or CPU intensive jobs | r or c large and above |

Scheduling metadata attaches a tier hint to each job. Hours accrue against tenant `runner_hours` regardless of tier unless a plan defines tier differentiated pools.

## Mapping to AWS Charges

| Component | AWS service | CUR keys | Notes |
|----------|-------------|----------|------|
| Runners on EC2 | AmazonEC2 | `line_item_usage_type LIKE 'BoxUsage%'` | On demand or SP and RI coverage if present |
| Containers | AWSFargate, AmazonECS | `product_servicecode IN ('AWSFargate','AmazonECS')` | Optional |
| Serverless | AWSLambda | `product_servicecode='AWSLambda'` | Optional |
| Volumes | EBS | `line_item_usage_type LIKE 'EBS:%'` | IOPS and throughput may apply |
| NAT | AmazonNATGateway | `product_servicecode='AmazonNATGateway'` | Shared allocation |
| PrivateLink | AmazonVPC | `line_item_usage_type LIKE '%Endpoint-Bytes%' OR line_item_usage_type LIKE '%VpcEndpoint-Hours%'` | Data or hour based |
| Egress | AWSDataTransfer, S3 | `%-Out-Bytes%` | Validates `egress_gb` |

## Scheduling and Estimation

### Batch and scheduled jobs

Use historical job run times to forecast `runner_hours`. For periodic jobs, compute expected monthly hours from schedule.

```sql
SELECT job_id,
       schedule_cron,
       AVG(runtime_minutes) AS avg_runtime_min,
       COUNT(*) AS runs_last_30d
FROM runner_job_history
GROUP BY job_id, schedule_cron;
```

Projected monthly hours:

```sql
SELECT job_id,
       expected_runs_per_month * avg_runtime_min / 60.0 AS projected_hours
FROM job_schedule_projection;
```

### Always on runners

Always on EC2 instances accrue `runner_idle_hours` when no active job is running. Plans may cap idle hours to control cost. Operators should consider converting long running workloads to scheduled jobs or autoscaling groups with aggressive scale in.

Idle detection example:

```sql
SELECT instance_id,
       SUM(idle_minutes) / 60.0 AS idle_hours
FROM runner_instance_activity
WHERE period = :month
GROUP BY instance_id;
```

## NAT and PrivateLink Allocation

NAT and PrivateLink often serve multiple tenants. Costs are allocated using `nat_gb_processed`, `privatelink_gb_processed`, or `endpoint_hours` according to the rules in allocation-rules.md. Allocation records preserve CUR line evidence and the rule version.

## Guardrails

- Always on runners must declare a justification in metadata and have a weekly review task.
- NAT exposure is capped per plan via `nat_gb_processed` where configured.
- PrivateLink consumption is monitored with alerts at 80, 95, and 100 percent of the configured cap.
- Egress quota is strictly enforced by policy. Top ups are available when enabled.
- EC2 spot is allowed for noncritical batch jobs if retry safe, with clear SLO exceptions.

## Estimation Cheat Sheet

| Driver | Approximation method | Caveat |
|--------|----------------------|--------|
| Runner hours | Sum of job durations or instance uptime | Include setup and teardown overhead |
| Idle hours | Instance uptime minus active runtime | Check schedule overlap and queue waits |
| NAT processed | Flow logs aggregation by NAT path | Validate against CUR NAT costs |
| PrivateLink | Endpoint bytes from VPC logs | Validate against CUR endpoint bytes |
| Egress | Flow logs out bytes | Validate against CUR where available |

## Example Top ups

| SKU code | Metric | Unit | Size | Notes |
|---------|--------|------|------|------|
| `TOPUP_RUNNER_25H` | `runner_hours` | Hour | 25 | Immediate effect, current cycle |
| `TOPUP_EGRESS_200GB` | `egress_gb` | GB | 200 | Published total only |
| `TOPUP_NAT_500GB` | `nat_gb_processed` | GB | 500 | Operator controlled availability |

## Operational Recommendations

- Prefer event driven or scheduled compute over 24x7 instances.
- Use instance right sizing and SP or RI coverage where eligible.
- Enable detailed VPC flow logs for accurate `nat_gb_processed` and `egress_gb`.
- Separate network paths for tenant versus operator traffic to avoid cross charging.
- Maintain explicit runner tier mappings in the admin database for audit.

## Cross References

- metrics-definition.md for metric semantics.
- allocation-rules.md for shared cost distribution.
- aws-cost-mapping.md for CUR keys and validation.
- plan-parameters.md for caps and thresholds.
- dashboard-design.md for tenant gauges and admin drilldowns.
