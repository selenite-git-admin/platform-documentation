# Slowly Changing Dimensions (SCD) Index

**Family:** Data Store  
**Tier:** Core  
**Owner:** Platform Foundation  
**Status:** Review  

## Overview
Slowly Changing Dimensions (SCD) govern how business entities maintain historical accuracy in the PostgreSQL data store. This capability enables point-in-time analysis without introducing new services or complex pipelines. The Runtime layer executes merges; the Store layer enforces constraints, views, and retention.

The design aligns with the platform’s principles:
- **Zero engineering:** SQL-first, no code generation or orchestration services.  
- **PostgreSQL native:** No warehouse dependency.  
- **Deterministic:** Hash-based change detection, consistent timestamps.  
- **Governed:** DRR tracks freshness, Evidence Ledger records merges.  

## Files
| Document                                    | Purpose |
|---------------------------------------------|----------|
| [SCD Playbook](scd-playbook.md)             | Conceptual design, column rules, naming, and guardrails |
| [SCD SQL Templates](scd-sql-templates.md)   | Ready-to-use DDL and merge SQL for SCD1 and SCD2 |
| [SCD Runtime Loader](scd-runtime-loader.md) | Runtime execution and transaction management pattern |
| [SCD Validation](scd-validation.md)         | Validation SQLs, QA checks, and PIT integrity tests |

## Architecture Role
| Layer | Responsibility |
|--------|----------------|
| Data Store | Defines SCD schema, constraints, and views |
| Runtime | Executes merges using templates and retries on conflict |
| DRR | Publishes freshness for SCD datasets and views |
| Governance | Approves retention, ensures audit parity in Evidence Ledger |

## Naming Example
| Type | Convention |
|------|-------------|
| SCD2 table | `dim_customer` |
| Current view | `vw_dim_customer_current` |
| PIT view | `vw_dim_customer_asof` |
| Staging table | `stg_customer_delta` |

## Key Patterns
- Single writer via Runtime jobs  
- MD5 hash for attribute change detection  
- Non-overlapping validity ranges  
- Idempotent merges with serializable transactions  
- UTC-based `timestamptz` for all validity fields  

## Entry Points
Developers and data engineers start with:  
1. **Design schema** → use `scd-playbook.md`  
2. **Generate DDL** → copy snippets from `scd-sql-templates.md`  
3. **Integrate loader** → follow steps in `scd-runtime-loader.md`  
4. **Validate integrity** → run checks in `scd-validation.md`  

## Summary
SCD within the Data Store family provides disciplined, low-maintenance historical tracking directly inside PostgreSQL. It keeps the platform compliant, auditable, and analytics-ready without requiring additional data-warehouse or transformation layers.
