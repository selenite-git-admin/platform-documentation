# Plan Parameters

## Overview

This document defines the commercial parameters that govern how a tenant’s usage is evaluated against a plan. The objective is to provide a precise, auditable specification that the evaluation engine can apply deterministically to produce quotas, thresholds, top ups, and upgrade recommendations. Plans are versioned, expressed in USD, and always reference the tenant as the canonical customer entity.

Plans express entitlements for data services, compute and networking, and seats. Plans may include add ons and top ups. Only tenant visible totals are surfaced in the UI. Per service price details remain operator facing.

## Purpose and Role

Plan parameters translate metric definitions into tenant facing quotas and billing behavior. The evaluation engine joins daily usage snapshots to the active plan version, computes utilization, warns at thresholds, and emits overage or top up actions. Plans also provide the configuration for upgrade and downgrade paths and the rules for proration.

## Plan Model

A plan is a declarative contract made of metadata, metric entitlements, thresholds, and commercial actions. A plan is immutable after publication. Any change creates a new version and tenants explicitly move to the newer version.

**Key attributes**

| Attribute | Description |
|----------|-------------|
| `plan_code` | Unique identifier such as `CFO-Standard-v1` |
| `currency` | USD by default |
| `billing_cycle` | Monthly unless specified otherwise |
| `base_seats` | Seat allocation included in base price |
| `metric_entitlements` | Map of metric codes to caps and behaviors |
| `thresholds` | Warning levels such as 80, 95, and 100 percent |
| `actions` | Evaluation results to actions like notify, lock, top up, or recommend upgrade |
| `addons` | Optional purchasable increments such as additional seats or runner hours |
| `effective_from` | Start date for the plan version |
| `effective_to` | Optional end date for the plan version |

## Data Services Parameters

Plans define caps and behavior for data service metrics. Snapshots count toward storage peak. Egress uses published tenant visible quota only.

| Metric | Unit | Aggregation | Plan parameter | Notes |
|--------|------|-------------|----------------|-------|
| `data_ingestion_gb` | GB | Sum daily | `cap_gb` | Total data accepted by the platform |
| `storage_gb_peak` | GB | Peak monthly | `cap_gb` | Includes snapshots and backups |
| `egress_gb` | GB | Sum daily with published monthly quota | `cap_gb` | UI shows only tenant total, not AWS components |
| `data_retained_gb` | GB | Peak monthly | `cap_gb` | For retention policies where applicable |

**Behavior**

- Utilization is computed as usage divided by cap.  
- Thresholds at 80, 95, and 100 percent generate quota events.  
- Exceeding the egress cap triggers top up or plan upgrade according to policy.  
- Storage peak includes snapshots. There is no separate snapshot quota.  

## Compute and Networking Parameters

Plans express compute in runner hours and networking in processed or transferred GB. Client facing names mask AWS service families. Mapping to CUR remains internal for validation.

| Metric | Unit | Aggregation | Plan parameter | Notes |
|--------|------|-------------|----------------|-------|
| `runner_hours` | Hour | Sum daily | `cap_hours` | Runner tiers: Light, Pro, Enterprise |
| `runner_idle_hours` | Hour | Sum daily | `cap_hours_opt` | Optional control for always on runners |
| `nat_gb_processed` | GB | Sum daily | `cap_gb_opt` | Used to bound shared NAT exposure |
| `privatelink_gb_processed` | GB | Sum daily | `cap_gb_opt` | For PrivateLink data path control |

**Runner tiers**

| Tier | Intended workload | Typical instance families (internal) |
|------|-------------------|--------------------------------------|
| Light | General pipelines and small batches | t or m small to medium |
| Pro | Performance sensitive jobs | c or m medium to large |
| Enterprise | Memory or CPU intensive jobs | r or c large and above |

Plans may fix a tier or allow a mix. The evaluation engine reads runner tier hints from job metadata and charges runner hours against the tenant’s pool.

## Seats Parameters

Seats define how many users can access the platform under a tenant plan. Seats are commercial entitlements and are not enforced through AWS IAM.

| Attribute | Description |
|----------|-------------|
| `base_seats` | Seats included with the plan |
| `max_seats` | Hard ceiling before auto upgrade |
| `seat_topup_size` | Increment purchased per top up |
| `seat_overage_action` | Bill extra seat or trigger upgrade |

**Seat behavior**

- Active seats are counted as the maximum assigned users during the billing month.  
- Under utilization does not reduce price.  
- Over utilization either creates additional seat charges or recommends upgrade according to policy.  

## Thresholds and Actions

Thresholds define when the system informs the tenant, limits actions, or recommends changes. Plans define these thresholds per metric or at the domain level.

| Threshold | Action |
|----------|--------|
| 80 percent | Notify tenant and show warning in dashboard |
| 95 percent | Notify tenant and show urgent warning |
| 100 percent | Enforce top up or recommend upgrade based on policy |

**Action types**

- Notify through UI banner and email.  
- Enforce soft cap with purchase flow for top ups.  
- Recommend upgrade when consistent overuse is detected.  
- Lock certain non essential features in extreme cases if defined by plan.

## Proration Rules

**Mid cycle start** A tenant starting mid month pays for the subscription pro rated by days remaining. Usage caps are also pro rated unless the plan declares full month caps.

**Mid cycle upgrade** Upgrades take effect immediately. Subscription price is pro rated for the remainder of the cycle. Caps are increased from the upgrade timestamp. Previous overages may still bill if already incurred.

**Mid cycle downgrade** Downgrades schedule for the next cycle unless explicitly allowed. Caps do not decrease mid cycle to avoid surprise lockouts.

**Top ups** Top ups are effective immediately and apply only to the current billing cycle unless noted as recurring.

## Evaluation Logic

The evaluation engine compares tenant usage with plan parameters and emits events and actions. The logic is deterministic and relies only on frozen daily snapshots for billing.

```sql
-- Example: compute utilization and events
WITH usage AS (
  SELECT tenant_id, metric_code, SUM(metric_value) AS period_value
  FROM tenant_usage_snapshot_daily
  WHERE usage_date BETWEEN :period_start AND :period_end
  GROUP BY tenant_id, metric_code
),
ent AS (
  SELECT tenant_id, metric_code, cap_value, thresholds
  FROM plan_metric_map_active
  WHERE period = :period
)
SELECT
  u.tenant_id,
  u.metric_code,
  u.period_value,
  e.cap_value,
  CASE WHEN e.cap_value > 0 THEN u.period_value / e.cap_value ELSE NULL END AS utilization,
  CASE
    WHEN u.period_value >= e.cap_value THEN 'EVENT_QUOTA_100'
    WHEN u.period_value >= e.cap_value * 0.95 THEN 'EVENT_QUOTA_95'
    WHEN u.period_value >= e.cap_value * 0.80 THEN 'EVENT_QUOTA_80'
    ELSE NULL
  END AS quota_event
FROM usage u
JOIN ent e
  ON e.tenant_id = u.tenant_id AND e.metric_code = u.metric_code;
```

```yaml
# Example plan metric entitlement
plan_code: CFO-Standard-v1
currency: USD
billing_cycle: monthly
base_seats: 10
metric_entitlements:
  data_ingestion_gb:
    cap_gb: 200
    thresholds: [0.8, 0.95, 1.0]
    action_on_100: topup_or_upgrade
  storage_gb_peak:
    cap_gb: 500
    thresholds: [0.8, 0.95, 1.0]
    notes: "Snapshots count toward this cap"
  egress_gb:
    cap_gb: 100
    thresholds: [0.8, 0.95, 1.0]
    publish_total_only: true
  runner_hours:
    cap_hours: 50
    thresholds: [0.8, 0.95, 1.0]
  nat_gb_processed:
    cap_gb_opt: 500
    thresholds: [0.8, 0.95, 1.0]
addons:
  extra_seats:
    unit: seat
    size: 5
  runner_hours_pack:
    unit: hour
    size: 25
effective_from: 2025-01-01
```

## Upgrade and Downgrade Policy

Plans define safe paths for movement across tiers. Consistent overuse of any critical metric across two consecutive months triggers an upgrade recommendation. Repeated severe overuse may enforce an automatic upgrade if the plan declares this behavior. Downgrades are allowed only at cycle boundaries unless otherwise noted.

## Anti Abuse Guardrails

The platform protects shared resources and fairness between tenants through guardrails.

- Short burst behavior that exceeds caps by a large margin may be throttled.  
- NAT and PrivateLink caps prevent unknown cross tenant impact.  
- Automated alerts prevent silent overuse of always on runners.  
- Abnormal patterns open operational investigations before billing closes.

## Versioning and Change Management

Plans are approved and published through a controlled process. A new version is created for any change to quotas, thresholds, or actions. Tenants continue on their existing version until they accept or are migrated by policy. Historical invoices always reference the exact plan version that was active during the billing period.

## Cross References

- **metrics-definition.md** for the canonical metric catalog and aggregation rules.  
- **aws-cost-mapping.md** for mapping to CUR dimensions and allocation categories.  
- **topup-upgrade-policy.md** for purchase and upgrade workflows.  
- **dashboard-design.md** for utilization gauges and user facing warnings.  
- **data-model.md** for schema of `plan_master`, `plan_metric_map`, and related tables.
