# Synthetic Data Services - Context

![status-internal](https://img.shields.io/badge/status-internal-blueviolet)
![owner-shared_services](https://img.shields.io/badge/owner-shared_services-informational)
![last_updated-2025-08-28%2015:00%20UTC+05:30](https://img.shields.io/badge/last_updated-2025-08-28%2015:00%20UTC%2B05:30-blue)

---

!!! info
    Goal is developer velocity. Do not model enterprises. Do not depend on external dumps.

## Problem
Engineers are blocked waiting for prospect data dumps. Cleansing and mapping delays builds. Compliance often prevents sharing. Iterations stall.

## Solution
Fabricate schema-true, business-plausible data on demand. Deterministic runs with seeds. Referential integrity across related tables. Fast write to DB or files.

## Workflow
- Pick source system and table  
  Data Source System → Provider → Version → Protocol → Module → Table  
  Example: ERP → SAP → S/4HANA → OData v2 → FI → SKA1
- Set generation parameters  
  Row count, seed, null rate, value ranges, faker locale, uniqueness, foreign-key mode, CDC toggle, outliers percent
- Choose destination  
  Databases: Postgres, MySQL, SQLite  
  Files: CSV, Parquet with optional partitioning
- Generate  
  Preview 20 rows, then write. Output includes run id and ready path.

## What this is not
- Not a synthetic enterprise twin
- Not a privacy research project
- Not client-facing collateral

## Design anchors
- Schema Services is the source of truth for shapes and constraints
- Determinism by seed; same config reproduces the same dataset
- Guardrails prevent nonsense parameter combos
- Runs on a laptop or dev VM; zero heavy ops

## Quality gates
- Reproducibility: same config → same hash signature
- Integrity: FK checks pass; uniqueness constraints hold
- Performance: target rows per second per generator are met
- Traceability: config + run id + artifact manifest are logged
