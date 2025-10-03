# Runbook

## Scope
Operational procedures for Policy Registry during incidents and routine tasks.
Covers detection, triage, mitigation, rollback, and validation for common scenarios.

## Roles and access
- Platform operator with access to observability dashboards
- Policy administrator for policy and version changes
- Read access to Policy Registry logs and traces

## Safety
- Prefer reversible actions
- Record every operator action with correlation_id in the ticket
- Use API operations documented in [API](api.md). Do not perform direct database changes

## Incident identification
Incidents are typically raised by alerts defined in [Observability](observability.md). The most common alerts are:
- Evaluation error rate (policy_evaluator_errors_total)
- Evaluation latency p95 breach (policy_evaluation_latency_ms)
- Denial spike (policy_denials_total)
- Missing binding detected (policy_missing_bindings_total)
- Registry store degradation (registry_store_latency_ms)

## Quick reference
| Symptom | First checks | Safe mitigations | Validation |
| --- | --- | --- | --- |
| Error rate spike | Recent deploys, error codes, affected scopes | Roll back to prior policy version for affected policy | Error rate falls, evaluations succeed |
| Latency p95 high | Store latency, hot tenants, large payloads | Reduce load, scale service, review rule complexity offline | p95 and p99 back within target |
| Denial spike | Recent policy or binding changes | Confirm intent with owners, roll back current version if unintended | Denials normalize by tenant |
| Missing binding | Scope without active binding | Create binding for scope | Evaluations no longer report missing binding |
| Store degradation | DB errors and saturation | Investigate DB health, reduce concurrency temporarily | Store metrics recover |

## Procedures

### 1. Roll back to a previous policy version
Use when a new version causes errors or bad outcomes.

Prerequisites
- Policy ID and the last known good version

Steps
1. List versions to identify the last good version
   ```bash
   curl -s "$BASE/policy-registry/v1/policies/$POLICY_ID/versions"      -H "Authorization: Bearer $TOKEN"
   ```
2. Set the last good version as current
   ```bash
   curl -X POST "$BASE/policy-registry/v1/policies/$POLICY_ID/versions/$VERSION/current"      -H "Authorization: Bearer $TOKEN"
   ```
3. Note the change in the incident ticket with the version numbers and correlation_id

Validation
- Error rate or denial spike reduces
- Observability dashboards show recovery

### 2. Create a missing binding for a scope
Use when evaluations report no active binding for a scope.

Prerequisites
- Target scope_type and scope_ref
- Policy ID and version to bind

Steps
1. Create binding
   ```bash
   curl -X POST "$BASE/policy-registry/v1/bindings"      -H "Authorization: Bearer $TOKEN"      -H "Content-Type: application/json"      -d '{
           "policy_id": "'"$POLICY_ID"'",
           "version_id": "'"$VERSION_ID"'",
           "scope_type": "tenant",
           "scope_ref": "'"$SCOPE_REF"'",
           "status": "active"
         }'
   ```
2. Capture the returned binding_id in the ticket

Validation
- Missing binding alerts clear for that scope
- New evaluations for the scope show decisions

### 3. Investigate latency p95 breaches
Use when evaluation latency exceeds target.

Steps
1. Check store metrics and errors on the Registry Store Health dashboard
2. Sample traces for long evaluations. Look for Store and EvaluateRules spans
3. If load is a factor, reduce concurrent calls at the caller or scale the service
4. Review complex policies offline and consider refactoring to simpler rules

Validation
- policy_evaluation_latency_ms p95 and p99 return within target
- api_request_duration_ms tails align with expectations

### 4. Investigate denial spikes
Use when denials jump for one tenant or globally.

Steps
1. Review Policy Evaluation Health dashboard filtered by tenant and subject_type
2. Identify the responsible policy and version from the decision logs
3. Confirm with the policy owner whether the spike is intended
4. If unintended, follow procedure 1 to roll back to a previous version

Validation
- Denials normalize for the tenant or globally
- Audit entry reflects corrective action

### 5. Handle store degradation
Use when registry_store_latency_ms degrades or errors increase.

Steps
1. Check database health indicators (connections, CPU, I/O)
2. Inspect recent migrations and long-running queries
3. Reduce concurrent calls temporarily if saturation is observed
4. Coordinate with database operators to restore performance

Validation
- Store latency recovers
- Error counts return to baseline

## Routine tasks

### List recent evaluations for an incident
Use dashboards or log queries to filter by correlation_id, binding_id, or tenant.
If you have an eval_id from logs, fetch its details:
```bash
curl -s "$BASE/policy-registry/v1/evaluations/$EVAL_ID"   -H "Authorization: Bearer $TOKEN"
```

### Export evidence for audit
Use the Evidence export path documented in the consuming module. Record the eval_id and evidence references.

## Post-incident
- Add a short summary of cause and fix to the incident record
- Link the exact policy_id, version, and bindings involved
- If procedures were missing, update this runbook and open action items in Pending Actions

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
