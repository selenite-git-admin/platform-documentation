# Lineage and Evidence

## Purpose
Track where data came from and what the pipeline did.
Produce evidence for audits and root cause analysis.

## Event schema
Use a standard schema for evidence events.

```json
{
  "run_id": "uuid",
  "stage": "ingestion|raw|gdp|kpi",
  "contract_id": "string",
  "contract_version": "string",
  "status": "started|succeeded|failed",
  "started_at": "ISO8601",
  "ended_at": "ISO8601",
  "counts": {"input_rows": 0, "output_rows": 0, "errors": 0},
  "links": {"log_url": "string", "report_url": "string"}
}
```

## Lineage edges
Record edges from extraction to raw, from raw to GDP, and from GDP to KPI.

## Storage and retention
Store evidence in a durable store.
Retain for a period that meets compliance goals.


## Skipped stages in evidence

## Skipped stages in evidence
A skipped stage produces an evidence record with status SKIPPED.
The record includes the stage name, the contract_id, and the reason.
