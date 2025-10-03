# Runbook

## Scope
Operational procedures for Data Contract Registry in incidents and routine tasks. This runbook covers detection, triage, mitigation, and validation for the four layer, artifact only model.

## Roles and access
- Platform operator with access to observability dashboards
- Registry administrator for dataset and schema operations
- Read access to Data Contract Registry logs and traces

## Safety
- Prefer reversible actions
- Record each operator action with a correlation_id in the ticket
- Use the API documented in [API](api.md). Do not perform direct database changes

## Incident identification
Incidents are typically raised by alerts defined in [Observability](observability.md). Common alerts:
- Breaking detected (dcr_breaking_changes_total)
- Current flip anomaly (dcr_current_set_total spikes)
- Ingest error rate (invalid or conflict)
- Diff slow (dcr_diff_latency_ms p95)
- Store degradation (registry_store_latency_ms, registry_store_errors_total)
- Read API latency breach (api_request_duration_ms p95)

## Quick reference
| Symptom | First checks | Safe mitigations | Validation |
| --- | --- | --- | --- |
| Breaking detected on a dataset layer | Recent ingest logs and version history | Freeze promotions on that dataset by requiring set_current_if_compatible=false for new ingests; notify consumers | No new current flips; consumers acknowledge or adjust |
| Current flips spiking | Version timeline and actors | Confirm legitimate batch backfill. If not intended, instruct producers to pause ingests | dcr_current_set_total returns to baseline |
| Ingest invalid or conflict | Validation errors and idempotency keys | Fix schema, retry with a fresh Idempotency Key. Ensure the same key is not reused across different payloads | Ingests succeed; error rate falls |
| Diff slow | Payload size, store latency | Pre compute schema hashes, increase diff cache size, review indexes | dcr_diff_latency_ms p95 within target |
| Store degradation | DB metrics and saturation | Reduce concurrency temporarily, coordinate with DB operators | Store metrics recover |
| Read API latency | Route level latency and query plans | Add or adjust indexes, cache hot reads, verify pagination | Read p95 within target |

## Procedures

### 1. Investigate a breaking change signal
Use when `dcr_breaking_changes_total` raises an alert.

Steps
1. List recent versions for the dataset and layer to confirm current has not changed
   ```bash
   curl -s "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/$LAYER/versions?page=1&page_size=10"      -H "Authorization: Bearer $TOKEN"
   ```
2. Diff the candidate version against current to understand the break
   ```bash
   curl -s "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/$LAYER/diff?from=$CURRENT&to=$CANDIDATE"      -H "Authorization: Bearer $TOKEN"
   ```
3. Freeze promotions for this dataset by instructing producers to use `"set_current_if_compatible": false` while fixes are prepared
4. Communicate impact to subscribers of this dataset and layer

Validation
- No unexpected current flips appear
- Consumers confirm they can continue using the existing current version

### 2. Recover from a bad ingest attempt
Use when ingests are failing due to invalid schema or conflicts.

Steps
1. Inspect ingest logs for the correlation_id and error code
2. Correct the schema locally and perform an ad hoc compatibility check
   ```bash
   curl -s -X POST "$BASE/data-contract-registry/v1/compatibility/check"      -H "Authorization: Bearer $TOKEN"      -H "Content-Type: application/json"      -d '{"dataset_id":"'"$DATASET_ID"'","layer":"'"$LAYER"'","base_version":'"$BASE_VER"',"schema_json":{...}}'
   ```
3. Retry ingest with a fresh Idempotency Key
   ```bash
   curl -s -X POST "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/$LAYER/schemas"      -H "Authorization: Bearer $TOKEN"      -H "Content-Type: application/json"      -H "Idempotency-Key: $(uuidgen)"      -d '{"schema_json":{...},"set_current_if_compatible":true}'
   ```

Validation
- Ingest succeeds and the new version appears in the list
- If compatible, current flips as expected

### 3. Handle current flip anomalies
Use when `dcr_current_set_total` spikes unexpectedly.

Steps
1. Review version timeline for the dataset to identify actors
2. Confirm whether a planned backfill or migration is underway
3. If unintended, request producers to pause ingests for this dataset
4. Audit recent API calls by correlating `correlation_id` across logs and traces

Validation
- Current flip counts return to baseline
- Version history aligns with expected activity

### 4. Investigate slow diffs
Use when `dcr_diff_latency_ms` breaches the p95 target.

Steps
1. Check store latency to rule out storage slowness
2. Inspect payload sizes for very large schemas
3. Ensure schema hash and parsed form are cached
4. Consider limiting diff detail depth for very large artifacts

Validation
- Diff latency p95 and p99 return within target

### 5. Read API latency breach
Use when read routes exceed latency targets.

Steps
1. Identify the hot routes from the API and Store Health dashboard
2. Explain slow queries with `EXPLAIN ANALYZE` in a staging environment
3. Add or adjust indexes for version listing and retrieval
4. Verify pagination parameters are enforced by the UI and callers

Validation
- Read latency p95 within target
- Error rate remains stable

### 6. Store degradation
Use when registry store latency or errors increase.

Steps
1. Check database health indicators: connections, CPU, I O, locks
2. Inspect recent migrations
3. Reduce concurrency temporarily if saturation is observed
4. Coordinate with database operators to restore performance

Validation
- Store latency and error metrics recover

## Routine tasks

### List current versions
```bash
curl -s "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/$LAYER/versions?page=1&page_size=20"   -H "Authorization: Bearer $TOKEN"
```

### Export a schema by version
```bash
curl -s "$BASE/data-contract-registry/v1/datasets/$DATASET_ID/layers/$LAYER/versions/$VERSION"   -H "Authorization: Bearer $TOKEN"
```

### View subscriptions for activation layer
```bash
curl -s "$BASE/data-contract-registry/v1/subscriptions?dataset_id=$DATASET_ID&layer=activation"   -H "Authorization: Bearer $TOKEN"
```

## Post incident
- Add a short summary of cause and fix to the incident record
- Link the dataset_id, layer, versions, and correlation_id used
- If procedures were insufficient, update this runbook and open action items in Pending Actions

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
