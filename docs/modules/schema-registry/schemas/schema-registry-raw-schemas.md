# Schema Registry — Raw Schemas
> Applies to: Raw/Staging Layer (pre-GDP normalization) • Owner: Platform Engineering • Last updated: 2025-10-07

## Purpose
Define the **Raw** (a.k.a. *staging* or *bronze+*) schema layer that receives extractor outputs and applies **minimal normalization** so downstream GDP models are deterministic and repeatable.

> **Positioning:** Extractor Schemas describe **transport** (envelope, file/stream layout, CDC markers).  
> **Raw Schemas** describe the **first durable contract for records** in the platform — stable columns, types, and light harmonization — **without** imposing business semantics.

---

## Objectives
- Provide a **source-agnostic, minimally normalized** record layout to bridge Extractor → GDP.  
- Enforce **type stability, timestamp normalization, timezone discipline**, and **id policies**.  
- Preserve **lossless lineage** back to extractor batches and source keys.  
- Enable **idempotent reprocessing** and **late-arrival handling**.  
- Keep Raw schemas simple, scalable, and backwards-compatible.

---

## Scope
Included:
- Column typing, naming, and normalization rules (no business renames).  
- Soft standardization (timezone, decimals, booleans, null policy).  
- CDC harmonization (`op`, `op_ts`, soft deletes).  
- Lineage fields and batch metadata for reproducibility.  
- Partitioning and storage conventions.

Excluded:
- Business semantics, KPI derivations, entity modeling (handled in GDP/KPI).  
- Heavy transformations, dedup across entities, or business key resolution.

---

## Architecture Overview
```mermaid
flowchart LR
    EX[Extractor Output (Transport)] --> RAW[Raw Ingest Normalize]
    RAW --> CAT[Raw Catalog (Published)]
    CAT --> GDP[GDP Modeling]
    RAW --> OBS[Observability & Audit]
```
- Raw performs **type casting + light harmonization**, writes to **published catalog**, and emits metrics.

---

## Core Responsibilities
- **Normalize types**: timestamps → `TIMESTAMP WITH TZ`, currency → `DECIMAL(p,s)`, booleans → logical.  
- **Standardize names**: enforce `snake_case`, forbid spaces/symbols.  
- **Harden CDC**: unify `op` ∈ {I,U,D}, carry `op_ts`, optional `deleted_at`.  
- **Attach lineage**: `batch_id`, `sequence_no`, `source_system`, `source_object`, checksum.  
- **Guarantee idempotency**: deterministic upserts keyed by **raw natural key**.  
- **Partition for scale**: `dt`, and optional domain partitions (e.g., company code).

---

## Raw Schema Contract (Fields)
| Field | Type | Req | Description |
|---|---|:--:|---|
| `raw_pk` | STRING | ✓ | Deterministic hash of source PK(s); stable across replays |
| `op` | STRING | ✓ | `I`,`U`,`D` |
| `op_ts` | TIMESTAMP | ✓ | Source operation time (normalized to UTC) |
| `ingested_at` | TIMESTAMP | ✓ | Platform ingest time (UTC) |
| `payload` | STRUCT | ✓ | Flattened columns from extractor record, minimally cast |
| `deleted_at` | TIMESTAMP |  | Soft delete timestamp (when `op='D'`) |
| `batch_id` | STRING | ✓ | Extractor batch identifier |
| `sequence_no` | INTEGER | ✓ | Ordering within batch |
| `source_system` | STRING | ✓ | e.g., `SAP` |
| `source_object` | STRING | ✓ | e.g., `BSEG` |
| `checksum` | STRING |  | File or record checksum |
| `dt` | DATE | ✓ | Partition column (ingested date, UTC) |

> **Design rule:** `payload` keys **mirror source column names** (snake-cased) — do **not** rename to business semantics here.

---

## Normalization Rules
- **Timestamps**: convert to UTC; store original timezone in `payload._tz` if provided.  
- **Numbers**: use `DECIMAL(p,s)` for currency/amounts; avoid float.  
- **Booleans**: map `Y/N`, `0/1` to logical `BOOLEAN`.  
- **Strings**: trim control characters; normalize newlines to `\n`.  
- **Nullability**: preserve nulls; avoid sentinel values (e.g., `-1`).  
- **Enums**: keep **source values**; do not remap to business categories.

---

## CDC & Idempotency
- Compute `raw_pk = hash(source_pk_components)` using stable order and type coercion.  
- Upsert policy: latest `op_ts` wins; tie-break by `sequence_no`.  
- For `D` operations: set `deleted_at=op_ts`, retain last known payload for audit.  
- Late arrivals (≤72h) are accepted; beyond window sent to **raw_quarantine**.

---

## Storage & Partitioning
- Table/view name: `{domain}__raw__{subject}` (e.g., `finance__raw__invoice_header`).  
- Partitions: `dt` (daily), optional secondary partition (e.g., `bukrs`).  
- File format: **Parquet + Snappy**; cataloged in Glue/HMS; external location on S3.  
- Location: `s3://warehouse/raw/{domain}/{subject}/dt={YYYY-MM-DD}/part=<n>`.

---

## Configuration
| Parameter | Description | Req | Default |
|---|---|:--:|---|
| `timezone_mode` | `utc` or `preserve_with_offset` |  | `utc` |
| `late_arrival_window_hours` | Accept late records within window |  | 72 |
| `raw_pk_strategy` | `hash` / `concat` / `source_pk_passthrough` |  | `hash` |
| `cdc_enforced` | Require op/op_ts presence |  | true |
| `partition_keys` | Extra partitioning fields |  | [] |

---

## Observability
| Metric | Description | Unit | Target |
|---|---|---|---|
| `raw.ingest_success_rate` | Success / total batches | % | >99 |
| `raw.late_ratio` | Late records / total | % | <2 |
| `raw.quarantine_count` | Records to raw_quarantine | count/day | 0 |
| `raw.upsert_conflicts` | Conflicts resolved by tie-break | count/day | trend |

**Alerts**
- Late ratio > 5% → source clock skew investigation.  
- Upsert conflicts spike → check duplicate keys or out-of-order batches.

---

## Error Catalog
| Code | Condition | Operator Action |
|---|---|---|
| RAW-1001 | Missing `op` or `op_ts` | Fix extractor mapping |
| RAW-1102 | Invalid timestamp format | Normalize to RFC3339 |
| RAW-1204 | Raw PK collision | Review PK components / widen key |
| RAW-1303 | Partition write failure | Retry / recompact |
| RAW-1401 | Late beyond window | Route to `raw_quarantine` |

---

## Governance Notes
- **Ownership & Scope:** Raw Schemas are **global platform assets** owned by Platform Engineering. Tenants consume them and **cannot publish or modify** them. Tenant-specific needs (e.g., Z/Y extensions) are implemented as **platform-approved tenant schemas** in `tenant.<code>` namespace via the CR → validation → governance → publish pipeline.
- **Compatibility:** Additive field additions in `payload` → **minor** version; breaking changes (type narrowing, field removal) → **major**.

---

## Examples

### Example A — SAP BSEG → Raw
**Input (Extractor JSONL)**  
```json
{"op":"U","op_ts":"2025-10-06T12:03:11Z","source_pk":"10001234","bukrs":"1000","belnr":"1900001234","gjahr":"2025","wrbtr":"1299.50","waers":"INR","budat":"2025-10-06"}
```

**Raw Row (Parquet logical view)**
```json
{
  "raw_pk": "sha1:3c5e...",
  "op": "U",
  "op_ts": "2025-10-06T12:03:11Z",
  "ingested_at": "2025-10-07T00:02:33Z",
  "payload": {
    "bukrs": "1000",
    "belnr": "1900001234",
    "gjahr": "2025",
    "wrbtr": "1299.50",
    "waers": "INR",
    "budat": "2025-10-06"
  },
  "batch_id": "01J9CZVQ8H5...",
  "sequence_no": 1,
  "source_system": "SAP",
  "source_object": "BSEG",
  "dt": "2025-10-07"
}
```

### Example B — Soft Delete
`op='D'` results in `deleted_at=op_ts` and payload retained for audit.

---

## Versioning & Change Management
- Raw schema versions follow `v<major>.<minor>[.<patch>]`.  
- Deprecation window: **90 days** minimum before retirement of prior major.  
- All changes logged with checksum and signer in `/audit/raw_schemas/`.

---
