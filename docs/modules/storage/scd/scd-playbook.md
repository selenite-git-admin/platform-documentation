# Slowly Changing Dimensions (SCD) – Playbook

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
This playbook standardizes SCD in PostgreSQL for mid sized enterprises. It provides naming, columns, constraints, and merge patterns. No extra services are required. Runtime executes the merges. DRR reports freshness. Catalog describes locations and schemas.

## Scope
- SCD Type 1: overwrite on change.
- SCD Type 2: history with valid ranges and current row flag.
- Point in time reads supported through views and helper functions.

## Naming
- Tables: `dim_<entity>` for SCD2, `dim_<entity>_s1` for SCD1.
- Staging: `stg_<entity>_delta` loaded by ingestion jobs.
- Views: `vw_dim_<entity>_current`, `vw_dim_<entity>_asof`.
- Constraints, indexes, and triggers prefixed with table name.

## Columns
**Common**
- `business_key` text not null
- Natural attributes as columns
- `last_updated_at` timestamptz not null default now()
- `scd_hash` text not null (md5 over natural attributes)

**SCD2 only**
- `dim_id` bigserial primary key
- `valid_from` timestamptz not null
- `valid_to` timestamptz not null default '9999-12-31'
- `is_current` boolean not null default true

## Guardrails
- Single writer (Runtime). Readers are read-only.
- Non overlapping ranges per `business_key`.
- Idempotent merges using hash and conflict handling.
- All merges executed in a single transaction with retry on serialization failure.
- Evidence Ledger records merge batch with correlation id.