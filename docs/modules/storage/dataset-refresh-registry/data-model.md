# Dataset Refresh Registry (DRR) Data Model

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Purpose
The DRR data model records dataset freshness and run history. It is optimized for low-latency reads and controlled writes.
Runtime systems write to this model after each dataset job completion. All other modules perform read-only queries.

## Model Overview
The schema consists of four primary entities:

| Table                      | Purpose                                               |
|----------------------------|-------------------------------------------------------|
| `dataset_registry`         | Canonical registry of all datasets tracked by DRR     |
| `dataset_refresh_schedule` | Holds schedule metadata and freshness SLO per dataset |
| `dataset_refresh_state`    | Stores current freshness state (one row per dataset)  |
| `dataset_run_log`          | Stores recent run events for observability and audit  |

Each table enforces foreign key integrity through `dataset_id`. Writes are transactional and idempotent.

## Entity Relationships

<a href="#enlarge-image" class="image-link">
  <img src="/assets/diagrams/dataset-refresh-registry/ddr-erd.svg" alt="Dataset Refresh Registry">
</a>

<div id="enlarge-image" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/dataset-refresh-registry/ddr-erd.svg" alt="Dataset Refresh Registry">
</div>

_Figure 2: Dataset Refresh Registry_{.figure-caption}

## Entity Definitions

### dataset_registry
Canonical registry of all datasets that participate in DRR tracking.
Populated automatically when a new dataset is registered in Storage Catalog.

| Column | Type | Description |
|---------|------|-------------|
| `dataset_id` | text (PK) | Unique identifier for the dataset |
| `layer` | text | Storage layer (raw, gdp, kpi, published) |
| `owner_module` | text | Module responsible for generating the dataset |
| `tenant_scope` | text | Scope indicator (single or multi) |
| `tags` | text[] | Optional classification tags |
| `created_at` | timestamptz | Creation timestamp |
| `updated_at` | timestamptz | Last metadata update |

**Notes**
- Dataset IDs mirror catalog naming (`layer.dataset_name_version`).
- Row created on first Runtime post or manual registration.

### dataset_refresh_schedule
Defines expected refresh cadence and SLO.

| Column | Type | Description |
|---------|------|-------------|
| `dataset_id` | text (FK) | Reference to `dataset_registry` |
| `cron` | text | Cron expression in UTC |
| `timezone` | text | Execution timezone |
| `freshness_slo_sec` | integer | Expected freshness window in seconds |
| `updated_at` | timestamptz | Last schedule update |

**Rules**
- Each dataset has at most one schedule record.
- A schedule update is atomic and versioned.

### dataset_refresh_state
Represents the current refresh condition for a dataset.
Exactly one row per dataset, updated after each successful or failed run.

| Column | Type | Description |
|---------|------|-------------|
| `dataset_id` | text (PK, FK) | Dataset reference |
| `last_success_at` | timestamptz | Timestamp of last successful run |
| `last_status` | text | Last recorded status (success, failed) |
| `next_scheduled_at` | timestamptz | Next expected run |
| `freshness_lag_sec` | integer | Difference between now and last_success_at |
| `status` | text | Derived status (fresh, late, failing, unknown) |
| `source_run_id` | text | Originating Runtime run identifier |
| `updated_at` | timestamptz | Last update timestamp |

**Status Derivation Logic**
| Condition | Status |
|------------|---------|
| `now - last_success_at <= freshness_slo_sec` | fresh |
| `now - last_success_at > freshness_slo_sec` | late |
| `no update for > 48h` | unknown |
| `last_status = failed` | failing |

### dataset_run_log
Append-only log of dataset runs. Used for traceability and analytics.

| Column | Type | Description |
|---------|------|-------------|
| `run_id` | text (PK) | Unique Runtime run identifier |
| `dataset_id` | text (FK) | Dataset reference |
| `started_at` | timestamptz | Run start time |
| `finished_at` | timestamptz | Run end time |
| `status` | text | success or failed |
| `rows_in` | bigint | Input record count |
| `rows_out` | bigint | Output record count |
| `crc` | text | Data integrity checksum |
| `error_code` | text | Error classification |
| `error_message` | text | Optional diagnostic string |

**Indexes**
- `(dataset_id, finished_at)` for recent lookups
- `(status)` for failure analysis

**Retention**
- 90 days for detailed run logs
- Older data compacted into weekly aggregates

## DBML

```dbml
Project DRR {
  database_type: "PostgreSQL"
  note: "Dataset Refresh Registry schema"
}

Table dataset_registry as DR {
  dataset_id text [pk]
  layer text
  owner_module text
  tenant_scope text
  tags text[]
  created_at timestamptz
  updated_at timestamptz
}

Table dataset_refresh_schedule as S {
  dataset_id text [ref: > DR.dataset_id]
  cron text
  timezone text
  freshness_slo_sec int
  updated_at timestamptz
}

Table dataset_refresh_state as ST {
  dataset_id text [pk, ref: > DR.dataset_id]
  last_success_at timestamptz
  last_status text
  next_scheduled_at timestamptz
  freshness_lag_sec int
  status text
  source_run_id text
  updated_at timestamptz
}

Table dataset_run_log as RL {
  run_id text [pk]
  dataset_id text [ref: > DR.dataset_id]
  started_at timestamptz
  finished_at timestamptz
  status text
  rows_in bigint
  rows_out bigint
  crc text
  error_code text
  error_message text
  indexes {
    (dataset_id, finished_at)
  }
}
```

## Constraints and Integrity
- All foreign keys are ON DELETE CASCADE.
- Inserts and updates require valid dataset registry entries.
- DRR rejects writes with timestamps older than current `updated_at`.
- Run logs are immutable after insert.

## Retention and Classification
| Table | Retention | Classification |
|--------|------------|----------------|
| dataset_registry | Permanent | Metadata |
| dataset_refresh_schedule | Permanent | Metadata |
| dataset_refresh_state | Permanent | Operational metadata |
| dataset_run_log | 90 days | Operational log (no PII) |

## Query Access Patterns
| Use Case | Query Target | Expected Latency |
|-----------|---------------|------------------|
| UI freshness check | dataset_refresh_state | <100 ms |
| Scheduled job lag report | dataset_refresh_state + schedule | <200 ms |
| Tenant dashboard summary | dataset_refresh_state filtered by tenant_id | <100 ms |
| Historical job trend | dataset_run_log | <500 ms (aggregated) |

## Reliability Guarantees
- Writes are atomic per dataset.
- Reads are strongly consistent within a single region.
- Backfill operations are executed under controlled maintenance mode only.

## Data Ownership
- Primary writer: Runtime service.
- Primary reader: Platform APIs and dashboards.
- Shared access via storage APIs using service tokens.