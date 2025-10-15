# Schema Registry — Pipelines Integration
> Context: Orchestration Integration • Owner: Platform Engineering • Last updated: 2025-10-07

## Purpose
Integrate the **Schema Registry** with AWS Glue–based pipelines and Lambda–driven orchestration to ensure all ingested data conforms to validated schemas across Extractor, Raw, GDP, and KPI layers.  
Schema Registry serves as the **source of truth** for schema definitions, version control, and validation policies used by all data processing jobs.

---

## Architecture Overview
```mermaid
flowchart LR
  SRC[Data Source] --> EXTRACTOR[AWS Lambda Extractor]
  EXTRACTOR --> RAW["AWS Glue – Raw Layer Job"]
  RAW --> GDP[AWS Glue - GDP Transform Job]
  GDP --> KPI[AWS Glue - KPI Aggregation Job]
  SCHEMA[Schema Registry] -->|Validation, Metadata| EXTRACTOR
  SCHEMA --> RAW
  SCHEMA --> GDP
  SCHEMA --> KPI
  KPI --> OBS[Observability & Drift Monitor (Lambda)]
  OBS --> ALERT[EventBridge Alerts]
```
Each pipeline stage binds to schemas in the registry through a **Schema Contract** validated at runtime and version‑controlled through governance.

---

## Schema–Pipeline Contracts

| Layer | Pipeline Component | Schema Source | Integration Mode | Validation Timing |
|---|---|---|---|---|
| Extractor | AWS Lambda function | Extractor Schema | On invocation | Envelope & Payload |
| Raw | AWS Glue Job | Raw Schema | Pre‑job validation | Structural |
| GDP | AWS Glue Job | GDP Schema | Pre‑job + post‑transform | Semantic |
| KPI | AWS Glue Job | KPI Schema | Build time + publish | Metric conformance |

Contracts are stored as JSON in the Schema Registry and resolved by pipeline runners using the **Schema Resolver SDK**.

---

## Integration Flow
1. **Schema Fetch:** Each Glue/Lambda task fetches the schema definition from the Registry via REST API or cached SDK layer.  
2. **Envelope Validation:** Schema structure and metadata validated by Lambda before job trigger.  
3. **Payload Validation:** AWS Glue validates data batch shape against the payload schema.  
4. **Compatibility Enforcement:** Version diffs are computed; incompatible schemas block the run.  
5. **Publish Hooks:** Successful job completion triggers a `SchemaValidated` or `SchemaDriftDetected` event to EventBridge.  
6. **Drift Handling:** Drifted records are routed to S3 quarantine (`s3://warehouse/quarantine/...`).  
7. **Governance Sync:** Registry marks schema lineage updates and execution metadata for audit.  

**EventBridge Topics**
| Event | Trigger | Target |
|---|---|---|
| `SchemaValidated` | Successful Glue job validation | Governance ledger |
| `SchemaDriftDetected` | Drift found in data batch | Ops alerts |
| `SchemaPublished` | New version released | Downstream consumers |
| `PipelineFailed` | Glue/Lambda job error | Ops escalation |

---

## Lineage and Metadata Propagation
Every Glue job registers output lineage into the **Schema Registry Metadata DB** (RDS):  
| Field | Source | Example |
|---|---|---|
| `pipeline_id` | Glue Job Name | `finance_gdp_transform` |
| `schema_fqid` | Registry | `finance.gdp.invoice:v1.2` |
| `run_id` | Glue Job Run | `jr-2a8bc9a1b1` |
| `s3_output_path` | Job Config | `s3://warehouse/gdp/invoice/2025/10/07/` |
| `status` | Runtime | `success` |
| `validation_result` | Validator | `pass` |

The metadata enables end‑to‑end data traceability and drift analytics.

---

## Observability
| Metric | Description | Source | Unit | Target |
|---|---|---|---|---|
| `pipeline.validation_success_rate` | Jobs passing schema validation | Glue Metrics | % | >99 |
| `pipeline.drift_events` | Schema drift detected per day | EventBridge | count/day | 0 |
| `pipeline.runtime_validation_latency_ms` | Validation runtime | Lambda | ms | P95 ≤ 500 |
| `schema.resolver_latency_ms` | Schema fetch time | Registry API | ms | P95 ≤ 200 |
| `pipeline.failure_rate` | Total failed jobs / day | Glue | % | <1 |

**Event Flow (Observability Path):**  
Glue → Lambda Drift Detector → EventBridge → CloudWatch Metrics → Ops Dashboard.

---

## Error Catalog
| Code | Condition | Operator Action |
|---|---|---|
| PIPE-1001 | Schema fetch timeout | Check Registry API or network |
| PIPE-1002 | Validation failed | Inspect envelope/payload errors |
| PIPE-1103 | Incompatible schema | Blocked — request schema update |
| PIPE-1204 | Drift detected | Review quarantine and trigger fix |
| PIPE-1301 | Lambda invocation error | Retry or redeploy function |
| PIPE-1402 | Metadata sync failure | Re-run metadata writer job |

---

## Governance Notes
- All Glue jobs **MUST** declare the schema FQID in their configuration.  
- Schemas are immutable during job execution — mid‑run version change triggers drift alert.  
- Lambda and Glue jobs record execution metadata in the governance ledger.  
- Governance can block new schema publication if open drifts exist.  
- Platform Ops maintains IAM isolation between pipeline runners and registry API.  

---

## Example Scenarios

### Example A — Normal Flow
1. Lambda extractor invokes with `finance.extractor.invoice:v1.0`.  
2. Glue Raw job validates batch → passes.  
3. GDP transform job applies `v1.1`, publishes success event.  
4. KPI aggregation runs hourly using latest compatible schema.  
**Result:** All events pass, registry lineage updated.

### Example B — Drift Detection
1. GDP Glue job detects unexpected field `invoice_region_code`.  
2. Data quarantined to S3; EventBridge alert raised.  
3. Ops team reviews drift and requests schema `v1.2`.  
4. Governance approves → new schema published → pipeline re‑runs.  
**Result:** Drift resolved, lineage updated, SLA met.

---

## References
- AWS Glue Job Definitions (`/jobs/gdp_transform_job_def.json`)  
- AWS Lambda Validator Layer (`/lambda/schema_validator.py`)  
- Schema Registry REST API (`/api/v1/schema/fetch`)  
- EventBridge Event Model (`/events/schema_registry_events.json`)

---
