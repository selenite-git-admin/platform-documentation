# Raw Stage

## Purpose
Create Bronze tables from the raw schema contract.
Apply keys and types with minimal transformation.

## Table creation
Generate DDL from the raw schema payload.
Honor naming rules and column types.
Create indexes that support reads.

## Load behavior
Load as idempotent batches.
Use change markers when present.
Do not drop source columns without approval.

## Evidence
Record loaded rows and rejected rows.
Record constraint violations with row samples.

## Example DDL pattern
```sql
CREATE TABLE {target_schema}.{target_table} (
  /* columns from payload */
);
```


## Continuous load and pre-fill

## Continuous load and pre-fill
Raw can run alone.
You can schedule Raw to load new data while GDP and KPI are not ready.
You can run a pre-fill over a historical window to seed Raw.
Set a checkpoint at the end of pre-fill to protect later increments.
