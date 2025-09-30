# Pipeline Configuration

## Purpose
Define how to configure runs in a declarative way.

## Schema
Reference schema contracts in the run config.
Set SLO and DQ policy per run.
Set resource and budget hints.

## Example
```yaml
run:
  run_id: ${uuid}
  stage: gdp
  trigger: schedule
  contracts:
    - contract_id: gdp.finance.ar.invoice_line.v1
      version: 1.0.0
  inputs:
    backfill_window_days: 2
  dq_policy: strict
  slo:
    freshness_minutes: 120
    max_cost_usd: 5
  resources:
    max_parallel_tasks: 8
  notify:
    on_fail: ["ops@example.com"]
```


## Profiles, stage sets, and readiness policy

## Run profiles in configuration
You can select a profile to control which stages run.
You can also specify an explicit stage set.

### Example with profile
```yaml
run:
  run_id: ${uuid}
  profile: raw_only
  trigger: schedule
  contracts:
    - contract_id: raw.sap.fi.bseg.v1
      version: 1.0.0
  slo:
    freshness_minutes: 0
  resources:
    max_parallel_tasks: 4
```

### Example with explicit stage set
```yaml
run:
  run_id: ${uuid}
  stage_set: [ingestion, raw]
  trigger: manual
  contracts:
    - contract_id: raw.sap.fi.bseg.v1
      version: 1.0.0
  inputs:
    checkpoint_token: "2024-01-01T00:00:00Z"
  dq_policy: strict
```

## Readiness policy
A stage runs only if there is an Active contract for that stage.
A stage runs only if the target store exists and is reachable.
If a stage is not ready, the scheduler skips it.
The system records the skip decision in evidence.
