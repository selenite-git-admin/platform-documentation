# Schema Registry — Runbook
> Context: Operational Response • Owner: Platform Engineering • Last updated: 2025-10-07

## Purpose
Provide operational procedures and troubleshooting workflows for maintaining the **Schema Registry** and its integrations with AWS Glue, Lambda, EventBridge, and CloudWatch.  
This runbook is the primary reference for incident handling, ensuring platform uptime, schema integrity, and compliance continuity.

---

## Scope
Applies to all production and staging environments using Schema Registry for Extractor, Raw, GDP, and KPI schemas.  
Includes pipelines, validation, governance, and drift monitoring subsystems.  
Excludes tenant‑side schema extensions unless managed via Platform Governance.

---

## Operational Dependencies

| Component | Description | AWS Service / Resource |
|---|---|---|
| Registry API | Core schema CRUD and versioning | AWS Lambda + API Gateway |
| Registry DB | Metadata, lineage, audit storage | Amazon RDS (MySQL) |
| Storage | Published schema definitions | Amazon S3 (`s3://registry/schemas/`) |
| Validation Engine | Envelope & Payload validator | AWS Lambda |
| Drift Detector | Runtime drift monitoring | AWS Glue Job + Lambda |
| Orchestration | Event routing and triggers | Amazon EventBridge |
| Metrics & Logs | Observability and alerting | AWS CloudWatch |
| Quarantine Store | Drifted data batches | Amazon S3 (`s3://warehouse/quarantine/`) |

---

## Prerequisites (Operational Readiness)
Before running or troubleshooting:
1. Verify IAM permissions for `schema-admin`, `ops-engineer`, `pipeline-runner`.  
2. Check health of dependent AWS services (`glue`, `lambda`, `rds`, `eventbridge`, `s3`).  
3. Ensure CloudWatch alarms are active and not suppressed.  
4. Confirm the correct version of schema in use via API:  
   ```bash
   curl -X GET https://api.datajetty.com/v1/schema/finance.gdp.invoice:v1.2
   ```

---

## Common Incident Scenarios

| Incident | Symptom | Primary Cause | Severity |
|---|---|---|---|
| **Validation Failure** | Schema fails to publish | Payload violation or dependency missing | Medium |
| **Drift Detected** | Runtime mismatch between data & schema | Source field changes, new column | High |
| **Publish Blocked** | Governance approval halted | Validation incomplete or dependency unresolved | Low |
| **Metadata Sync Failure** | Pipeline lineage missing | RDS sync lag or network timeout | Medium |
| **API Latency Spike** | Registry >300 ms | High traffic or cache miss | Medium |
| **Glue Job Failure** | Pipeline aborts mid‑run | Schema mismatch or AWS resource quota | High |

---

## Run Procedures

### 🧩 1. Validation Failure
**Trigger:** `VAL-1102` / `VAL-1304` events from EventBridge  
**Actions:**
1. Retrieve validation logs from CloudWatch:
   ```bash
   aws logs filter-log-events --log-group-name "/aws/lambda/schema-validator" --filter-pattern "VAL-"
   ```
2. Identify schema and version from message payload.
3. If missing `$ref` or invalid dependency → publish dependency schema first.  
4. Re-run validation via API:
   ```bash
   curl -X POST https://api.datajetty.com/v1/schema/validate -d '{"fqid":"finance.gdp.invoice:v1.2"}'
   ```
5. If passes, mark status `validated` via governance tool.

---

### ⚠️ 2. Schema Drift Event
**Trigger:** `SchemaDriftDetected` in EventBridge or `drift.detected_count` alarm.  
**Actions:**
1. Open drift alert in CloudWatch → view affected FQID.  
2. Review quarantined batch in S3:  
   ```bash
   aws s3 ls s3://warehouse/quarantine/finance/gdp/invoice/ --recursive
   ```
3. Inspect payload difference (new or missing field).  
4. If valid change → raise schema evolution request via governance portal.  
5. After approval → new schema version published (`vX.Y+1`).  
6. Trigger Glue reprocess job:
   ```bash
   aws glue start-job-run --job-name finance_gdp_reprocess
   ```

---

### 🚧 3. Publish Blocked
**Trigger:** Schema stuck in `pending_approval`.  
**Actions:**
1. Verify governance log:
   ```bash
   aws logs filter-log-events --log-group-name "/aws/lambda/schema-governance" --filter-pattern "approval"
   ```
2. Ensure dependent schemas exist and are `validated`.  
3. Force publish (if approved by Governance):
   ```bash
   curl -X POST https://api.datajetty.com/v1/schema/publish -d '{"fqid":"finance.gdp.invoice:v1.2"}'
   ```
4. Confirm version tag updated in Registry DB.

---

### 🔄 4. Metadata Sync Failure
**Trigger:** Missing lineage entries or delayed RDS writes.  
**Actions:**
1. Check RDS connectivity:
   ```bash
   aws rds describe-db-instances --db-instance-identifier registry-db
   ```
2. Review Lambda sync job logs (`/aws/lambda/metadata-writer`).  
3. Retry failed sync via EventBridge replay or API:
   ```bash
   curl -X POST https://api.datajetty.com/v1/schema/sync/metadata -d '{"run_id":"jr-2a8bc9a1b1"}'
   ```
4. Verify lineage in dashboard → schema → pipeline linkage visible.

---

### 🧰 5. Registry API Latency Spike
**Trigger:** CloudWatch alarm `registry.api_latency_ms > 300`.  
**Actions:**
1. Inspect CloudWatch metrics and logs.  
2. Check Redis/DynamoDB cache hit ratio.  
3. If < 90 %, scale Lambda concurrency or warm cache:  
   ```bash
   aws lambda put-function-concurrency --function-name registry-api --reserved-concurrent-executions 50
   ```
4. Confirm P95 latency restored < 300 ms.

---

### 🧨 6. Pipeline Job Failure (Schema Mismatch)
**Trigger:** AWS Glue job terminated with schema error.  
**Actions:**
1. Review Glue job logs in CloudWatch `/aws-glue/jobs/logs-v2`.  
2. Identify failing schema FQID.  
3. Validate schema locally:
   ```bash
   curl -X GET https://api.datajetty.com/v1/schema/validate?fqid=finance.gdp.invoice:v1.2
   ```
4. If mismatch → evolve schema or update mapping in Glue script.  
5. Re-run Glue job:
   ```bash
   aws glue start-job-run --job-name finance_gdp_transform
   ```

---

## Rollback / Recovery

| Scenario | Recovery Action | Command / Reference |
|---|---|---|
| Schema published in error | Deprecate version via API | `curl -X POST /schema/deprecate` |
| Validation engine failure | Redeploy Lambda layer | `aws lambda update-function-code` |
| RDS corruption | Restore snapshot | `aws rds restore-db-instance-from-s3` |
| Drift quarantine overflow | Purge >30 day data | `aws s3 rm --recursive` |
| EventBridge backlog | Purge + replay | `aws events list-replay` |

---

## Escalation Matrix

| Severity | Description | Owner | SLA | Escalation Path |
|---|---|---|---|---|
| **Critical (P1)** | Drift or data loss in prod | Platform Eng | 1h | SRE → Eng Lead → CTO |
| **High (P2)** | Validation or pipeline blockage | Platform Ops | 4h | Ops Lead → Eng Lead |
| **Medium (P3)** | Governance sync delay | Governance | 1 day | Governance → Eng |
| **Low (P4)** | Minor UI/API bug | Dev Team | 3 days | Dev → Product |

---

## Audit & Post‑Incident Steps
1. Record root cause and corrective action in incident tracker.  
2. Tag associated schema FQIDs and job runs in governance ledger.  
3. Verify metric recovery and alarm clearance.  
4. Conduct RCA review in weekly Ops sync.  
5. Close ticket only after two successful pipeline cycles.

---

## Appendix — Useful Commands

### Schema Validation
```bash
curl -X POST https://api.datajetty.com/v1/schema/validate -d '{"fqid":"finance.gdp.invoice:v1.2"}'
```

### Publish Schema
```bash
curl -X POST https://api.datajetty.com/v1/schema/publish -d '{"fqid":"finance.gdp.invoice:v1.2"}'
```

### Drift Inspection
```bash
aws s3 ls s3://warehouse/quarantine/finance/gdp/invoice/
```

### Event Replay
```bash
aws events start-replay --replay-name registry-event-replay --event-source-arn arn:aws:events:us-east-1:123456789012:event-bus/default
```

### Glue Job Re‑run
```bash
aws glue start-job-run --job-name finance_gdp_transform
```

---

## References
- Lambda: `/aws/lambda/schema-validator`, `/aws/lambda/drift-detector`  
- Glue Jobs: `/aws-glue/jobs/logs-v2`  
- EventBridge Rules: `/events/schema_registry_events.json`  
- CloudWatch Dashboards: `/infra/monitoring/schema_registry_dashboard.json`  
- Governance Ledger: `/db/schema_audit_ledger.sql`

---
