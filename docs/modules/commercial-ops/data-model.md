# Commercial-Ops Data Model

## Overview

This document defines the Commercial-Ops data model used for plan evaluation, usage metering, cost allocation, invoicing, payment reconciliation, and audit. The model is designed for Aurora (PostgreSQL-compatible) but is portable to other SQL engines with minor changes. The canonical entities are **tenant** and **plan**. Currency defaults to **USD**.

Design goals:

- Clear separation of raw, derived, and financial records
- Idempotent pipelines with immutable period freezes
- Evidence-first accounting with reproducible queries
- Backward-compatible schema evolution using versioned contracts

## Entity Summary

| Entity                 | Purpose                            | Notes                                             |
|------------------------|------------------------------------|---------------------------------------------------|
| `tenant_master`        | Registry of tenants                | Canonical identifiers, lifecycle, billing profile |
| `plan_master`          | Registry of plan SKUs and versions | Entitlements and thresholds                       |
| `plan_metric_map`      | Plan → metric caps and thresholds  | Versioned, forward-effective                      |
| `tenant_plan_binding`  | Active plan per tenant per period  | Proration fields for upgrades                     |
| `usage_snapshot_daily` | Daily metric snapshots             | Drives dashboards and thresholds                  |
| `fact_cost_raw`        | CUR-derived raw cost lines         | Ingested from AWS CUR (read-only)                 |
| `fact_cost_allocated`  | Shared-cost allocations            | Rule-based pooling and split                      |
| `budget_master`        | Budgets and thresholds             | Daily refresh and alert triggers                  |
| `invoice_header`       | Tenant invoice summary             | One per tenant per period                         |
| `invoice_detail`       | Line items                         | Metrics, top-ups, allocations                     |
| `payment_txn`          | Payments and receipts              | Card, wallet, bank transfer                       |
| `recon_summary`        | Monthly reconciliation result      | Variance, status                                  |
| `recon_exceptions`     | Itemized variances                 | Tagging, allocation, invoice                      |
| `audit_event`          | System audit log                   | Actor, action, object, evidence                   |

## Logical Relationships

- A tenant has zero or one active plan per billing cycle. Historical bindings are retained.
- Daily usage snapshots roll into monthly evaluation results and dashboard views.
- Raw CUR lines reconcile to allocated costs; allocated costs reconcile to invoices.
- Payments settle invoices; reconciliation validates the end-to-end trail.
- All financial artifacts link to immutable evidence (query IDs, file digests).

### Entity Relationship Diagram (ERD)

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/commercial-ops/commercial-ops-erd.svg" alt="Commercial Operations ERD">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/commercial-ops/commercial-ops-erd.svg" alt="Commercial Operations ERD">
</div>

_Figure 1: Commercial Operations ERD_{.figure-caption}

## Physical Schema (DDL)

> SQL below targets Aurora PostgreSQL. Adjust data types as needed for other engines.

### 1. Master and Reference

```sql
CREATE TABLE tenant_master (
  tenant_id        VARCHAR(64) PRIMARY KEY,
  tenant_name      VARCHAR(256) NOT NULL,
  status           VARCHAR(32)  NOT NULL DEFAULT 'active', -- active|suspended|closed
  billing_contact  JSONB,
  tax_profile      JSONB,
  created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE plan_master (
  plan_code        VARCHAR(64) PRIMARY KEY,
  plan_family      VARCHAR(64) NOT NULL, -- Enterprise
  version          VARCHAR(16) NOT NULL, -- v1
  currency         VARCHAR(8)  NOT NULL DEFAULT 'USD',
  base_price_usd   NUMERIC(18,6) NOT NULL,
  base_seats       INTEGER NOT NULL,
  metadata         JSONB,
  effective_from   DATE NOT NULL,
  effective_to     DATE
);

CREATE TABLE plan_metric_map (
  plan_code        VARCHAR(64) REFERENCES plan_master(plan_code),
  metric_code      VARCHAR(64) NOT NULL,
  cap_value        NUMERIC(18,6) NOT NULL,
  threshold_80     NUMERIC(18,6),
  threshold_95     NUMERIC(18,6),
  threshold_100    NUMERIC(18,6),
  unit             VARCHAR(32) NOT NULL,
  notes            TEXT,
  PRIMARY KEY(plan_code, metric_code)
);
```

### 2. Plan Binding

```sql
CREATE TABLE tenant_plan_binding (
  binding_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id        VARCHAR(64) REFERENCES tenant_master(tenant_id),
  plan_code        VARCHAR(64) REFERENCES plan_master(plan_code),
  period_start     DATE NOT NULL,
  period_end       DATE NOT NULL,
  status           VARCHAR(32) NOT NULL DEFAULT 'active', -- active|scheduled|expired
  proration_factor NUMERIC(18,6) DEFAULT 1.0,
  created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tpb_tenant_period ON tenant_plan_binding(tenant_id, period_start, period_end);
```

### 3. Usage Snapshots

```sql
CREATE TABLE usage_snapshot_daily (
  id               BIGSERIAL PRIMARY KEY,
  tenant_id        VARCHAR(64) REFERENCES tenant_master(tenant_id),
  metric_code      VARCHAR(64) NOT NULL,                -- data_ingestion_gb, storage_gb_peak, egress_gb, runner_hours, active_users
  metric_value     NUMERIC(18,6) NOT NULL,
  usage_date       DATE NOT NULL,
  cap_value        NUMERIC(18,6),
  utilization      NUMERIC(18,6),                       -- metric_value / cap_value
  quota_event      VARCHAR(32),                         -- EVENT_QUOTA_80|95|100
  last_updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (tenant_id, metric_code, usage_date)
);
```

### 4. CUR Raw and Allocation

```sql
CREATE TABLE fact_cost_raw (
  identity_line_item_id    VARCHAR(128) PRIMARY KEY,
  bill_billing_period_start_date DATE NOT NULL,
  bill_billing_period_end_date   DATE NOT NULL,
  line_item_usage_start_date     TIMESTAMP,
  line_item_usage_end_date       TIMESTAMP,
  product_servicecode            VARCHAR(64),
  line_item_usage_type           VARCHAR(128),
  line_item_usage_amount         NUMERIC(18,6),
  line_item_unblended_cost       NUMERIC(18,6),
  resource_tags_user_tenant_id   VARCHAR(64),
  resource_tags_user_plan_id     VARCHAR(64),
  ingested_at                    TIMESTAMP NOT NULL DEFAULT NOW(),
  source_digest                  VARCHAR(64)
);

CREATE TABLE fact_cost_allocated (
  id                BIGSERIAL PRIMARY KEY,
  tenant_id         VARCHAR(64) REFERENCES tenant_master(tenant_id),
  period_start      DATE NOT NULL,
  period_end        DATE NOT NULL,
  service           VARCHAR(64) NOT NULL,
  category          VARCHAR(32) NOT NULL, -- NAT|PLINK|CLOUDWATCH|S3|EBS|OTHER
  rule_id           VARCHAR(64) NOT NULL,
  allocated_cost_usd NUMERIC(18,6) NOT NULL,
  key_metric        VARCHAR(64),
  key_value         NUMERIC(18,6),
  key_total         NUMERIC(18,6),
  source_line_ids   JSONB,
  evidence_links    JSONB,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_fca_tenant_period ON fact_cost_allocated(tenant_id, period_start);
```

### 5. Budgets and Alerts

```sql
CREATE TABLE budget_master (
  budget_id        VARCHAR(64) PRIMARY KEY,
  scope_type       VARCHAR(16) NOT NULL,            -- tenant|plan|platform
  scope_ref        VARCHAR(64),                     -- tenant_id or plan_code
  metric_type      VARCHAR(32) NOT NULL,            -- aws_cost|platform_metric|composite
  period           VARCHAR(16) NOT NULL,            -- monthly|quarterly
  target_usd       NUMERIC(18,6) NOT NULL,
  actual_usd       NUMERIC(18,6) DEFAULT 0,
  thresholds_json  JSONB,
  status           VARCHAR(16) NOT NULL DEFAULT 'ok', -- ok|warning|breached
  last_refreshed_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### 6. Invoicing and Payments

```sql
CREATE TABLE invoice_header (
  invoice_id       VARCHAR(64) PRIMARY KEY,
  tenant_id        VARCHAR(64) REFERENCES tenant_master(tenant_id),
  period_start     DATE NOT NULL,
  period_end       DATE NOT NULL,
  status           VARCHAR(16) NOT NULL DEFAULT 'open', -- open|issued|paid|void
  subtotal_usd     NUMERIC(18,6) NOT NULL DEFAULT 0,
  tax_usd          NUMERIC(18,6) NOT NULL DEFAULT 0,
  total_usd        NUMERIC(18,6) NOT NULL DEFAULT 0,
  issued_at        TIMESTAMP,
  paid_at          TIMESTAMP,
  created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_invoice_unique ON invoice_header(tenant_id, period_start, period_end);

CREATE TABLE invoice_detail (
  id               BIGSERIAL PRIMARY KEY,
  invoice_id       VARCHAR(64) REFERENCES invoice_header(invoice_id) ON DELETE CASCADE,
  line_type        VARCHAR(32) NOT NULL,               -- subscription|topup|allocation|adjustment
  metric_code      VARCHAR(64),
  quantity         NUMERIC(18,6),
  unit             VARCHAR(32),
  unit_price_usd   NUMERIC(18,6),
  amount_usd       NUMERIC(18,6) NOT NULL,
  reference_ids    JSONB,                               -- links to allocation ids or topup ids
  notes            TEXT
);

CREATE TABLE payment_txn (
  payment_id       VARCHAR(64) PRIMARY KEY,
  invoice_id       VARCHAR(64) REFERENCES invoice_header(invoice_id),
  method           VARCHAR(32) NOT NULL,               -- card|wallet|bank_transfer|credit
  amount_usd       NUMERIC(18,6) NOT NULL,
  provider_ref     VARCHAR(128),
  status           VARCHAR(16) NOT NULL DEFAULT 'confirmed', -- pending|confirmed|failed|refunded
  created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### 7. Reconciliation and Audit

```sql
CREATE TABLE recon_summary (
  recon_id           VARCHAR(64) PRIMARY KEY,
  period_start       DATE NOT NULL,
  period_end         DATE NOT NULL,
  aws_total_usd      NUMERIC(18,6) NOT NULL,
  allocated_total_usd NUMERIC(18,6) NOT NULL,
  invoiced_total_usd NUMERIC(18,6) NOT NULL,
  operator_overhead_usd NUMERIC(18,6) NOT NULL,
  variance_usd       NUMERIC(18,6) NOT NULL,
  variance_pct       NUMERIC(18,6) NOT NULL,
  status             VARCHAR(16) NOT NULL,  -- ok|warning|failed
  created_at         TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE recon_exceptions (
  exception_id     VARCHAR(64) PRIMARY KEY,
  recon_id         VARCHAR(64) REFERENCES recon_summary(recon_id),
  tenant_id        VARCHAR(64),
  category         VARCHAR(32) NOT NULL,    -- Tagging|Allocation|Invoice|Timing|FX
  description      TEXT NOT NULL,
  variance_pct     NUMERIC(18,6),
  status           VARCHAR(16) NOT NULL DEFAULT 'open', -- open|resolved
  created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_event (
  event_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  occurred_at      TIMESTAMP NOT NULL DEFAULT NOW(),
  actor_type       VARCHAR(32),  -- system|tenant_user|operator_user
  actor_id         VARCHAR(128),
  action           VARCHAR(64),
  object_type      VARCHAR(64),
  object_id        VARCHAR(128),
  metadata         JSONB
);
```

## DBML (for ERD tools)

```dbml
Project commercial_ops {
  database_type: "PostgreSQL"
}

Table tenant_master {
  tenant_id varchar [pk]
  tenant_name varchar
  status varchar
  billing_contact json
  tax_profile json
  created_at timestamp
  updated_at timestamp
}

Table plan_master {
  plan_code varchar [pk]
  plan_family varchar
  version varchar
  currency varchar
  base_price_usd numeric
  base_seats int
  metadata json
  effective_from date
  effective_to date
}

Table plan_metric_map {
  plan_code varchar [ref: > plan_master.plan_code]
  metric_code varchar
  cap_value numeric
  threshold_80 numeric
  threshold_95 numeric
  threshold_100 numeric
  unit varchar
  notes text
  Indexes { (plan_code, metric_code) [unique] }
}

Table tenant_plan_binding {
  binding_id uuid [pk]
  tenant_id varchar [ref: > tenant_master.tenant_id]
  plan_code varchar [ref: > plan_master.plan_code]
  period_start date
  period_end date
  status varchar
  proration_factor numeric
  created_at timestamp
}

Table usage_snapshot_daily {
  id bigserial [pk]
  tenant_id varchar [ref: > tenant_master.tenant_id]
  metric_code varchar
  metric_value numeric
  usage_date date
  cap_value numeric
  utilization numeric
  quota_event varchar
  last_updated_at timestamp
}

Table fact_cost_raw {
  identity_line_item_id varchar [pk]
  bill_billing_period_start_date date
  bill_billing_period_end_date date
  line_item_usage_start_date timestamp
  line_item_usage_end_date timestamp
  product_servicecode varchar
  line_item_usage_type varchar
  line_item_usage_amount numeric
  line_item_unblended_cost numeric
  resource_tags_user_tenant_id varchar
  resource_tags_user_plan_id varchar
  ingested_at timestamp
  source_digest varchar
}

Table fact_cost_allocated {
  id bigserial [pk]
  tenant_id varchar [ref: > tenant_master.tenant_id]
  period_start date
  period_end date
  service varchar
  category varchar
  rule_id varchar
  allocated_cost_usd numeric
  key_metric varchar
  key_value numeric
  key_total numeric
  source_line_ids json
  evidence_links json
  created_at timestamp
}

Table budget_master {
  budget_id varchar [pk]
  scope_type varchar
  scope_ref varchar
  metric_type varchar
  period varchar
  target_usd numeric
  actual_usd numeric
  thresholds_json json
  status varchar
  last_refreshed_at timestamp
}

Table invoice_header {
  invoice_id varchar [pk]
  tenant_id varchar [ref: > tenant_master.tenant_id]
  period_start date
  period_end date
  status varchar
  subtotal_usd numeric
  tax_usd numeric
  total_usd numeric
  issued_at timestamp
  paid_at timestamp
  created_at timestamp
}

Table invoice_detail {
  id bigserial [pk]
  invoice_id varchar [ref: > invoice_header.invoice_id]
  line_type varchar
  metric_code varchar
  quantity numeric
  unit varchar
  unit_price_usd numeric
  amount_usd numeric
  reference_ids json
  notes text
}

Table payment_txn {
  payment_id varchar [pk]
  invoice_id varchar [ref: > invoice_header.invoice_id]
  method varchar
  amount_usd numeric
  provider_ref varchar
  status varchar
  created_at timestamp
}

Table recon_summary {
  recon_id varchar [pk]
  period_start date
  period_end date
  aws_total_usd numeric
  allocated_total_usd numeric
  invoiced_total_usd numeric
  operator_overhead_usd numeric
  variance_usd numeric
  variance_pct numeric
  status varchar
  created_at timestamp
}

Table recon_exceptions {
  exception_id varchar [pk]
  recon_id varchar [ref: > recon_summary.recon_id]
  tenant_id varchar
  category varchar
  description text
  variance_pct numeric
  status varchar
  created_at timestamp
}

Table audit_event {
  event_id uuid [pk]
  occurred_at timestamp
  actor_type varchar
  actor_id varchar
  action varchar
  object_type varchar
  object_id varchar
  metadata json
}
```

## Data Lineage and Partitioning

- **Raw layer**: `fact_cost_raw` ingested from AWS CUR (S3 → Glue → Athena). Partitions by `bill_billing_period_start_date`.
- **Derived layer**: `usage_snapshot_daily`, `fact_cost_allocated`. Derived from telemetry and raw layer; keyed by `tenant_id` and `period_start`.
- **Financial layer**: invoices, payments, reconciliation. Immutable after close; corrections via credit notes and reversals.

Recommended partitioning:

- `fact_cost_raw`: `bill_billing_period_start_date` monthly partitions
- `usage_snapshot_daily`: `usage_date` daily index
- `fact_cost_allocated`: `period_start` monthly partitions

## Operational Notes

- All changes to plan caps or thresholds are forward-effective via `plan_metric_map`.
- Idempotency is enforced through primary keys and dedupe digests.
- Reconciliation is required before invoice finalization. Successful `recon_summary.status = 'ok'` is a gate.
- Audit events are mandatory for plan upgrades, top-ups, invoice issuance, refunds, and reversals.
- Exports to external accounting systems should use a read-only replica or dedicated views.

## Cross References

- `aws-cost-integration/cur-ingestion.md`
- `aws-cost-integration/tag-strategy.md`
- `aws-cost-integration/allocation-rules.md`
- `aws-cost-integration/reconciliation.md`
- `plan-pricing/plan-parameters.md`
- `plan-pricing/metrics-definition.md`
- `ui/dashboard-design.md`
