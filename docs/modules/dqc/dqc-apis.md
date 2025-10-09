# Data Quality Control (DQC) APIs

**Audience:** Backend engineers, data platform engineers, and SREs  
**Status:** Working draft  
**Purpose:** Define the DQC service API surface, including endpoints, request and response schemas, security, error handling, idempotency, observability hooks, and lifecycle flows. The APIs are designed to be deterministic, auditable, and easy to integrate with data pipelines, Observability, and Tenancy modules.

## Design Principles

- Stateless evaluation with explicit inputs and versioned rule packs.  
- Idempotency through request hash and correlation identifiers.  
- Clear separation between validation, verdict retrieval, scorecards, waivers, and rule pack management.  
- Predictable pagination and filtering for history endpoints.  
- Explicit error codes and actionable messages.

## Base Path And Media Types

Base path is `/dqc/v1`. Requests and responses use `application/json`. Time fields use RFC 3339 with timezone designator. All endpoints accept `X-Request-Id` and return `X-Correlation-Id`.

## Authentication And Authorization

- OAuth 2.0 bearer tokens issued by the access service.  
- Scopes include `dqc.read`, `dqc.write`, and `dqc.admin`.  
- Tenancy scoped tokens can restrict access by tenant when dataset is tenant tagged.  
- Administrative endpoints require `dqc.admin` scope.

## Endpoints

### Validate

`POST /dqc/v1/validate`

Triggers validation for a dataset and stage using the active or specified rule pack version. Returns a validation job or immediate verdict depending on the evaluator mode.

Request
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "rulepackVersion": 3,
  "runId": "run_20251009_1230",
  "options": {
    "mode": "batch",
    "partitions": ["2025-10-09"],
    "failFast": false,
    "shadow": false
  },
  "metadata": {
    "tenantId": "t_0456",
    "sourceSystem": "sap",
    "trigger": "pipeline_promotion"
  }
}
```

Response 202
```json
{"jobId":"job_9812","state":"running"}
```

Response 200 when synchronous
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "runId": "run_20251009_1230",
  "rulepackVersion": 3,
  "score": 98.76,
  "status": "PASS_WITH_WARNINGS",
  "results": {
    "passed": 123456,
    "failed": 1544,
    "criticalFailures": 2,
    "warnings": 48
  },
  "createdAt": "2025-10-09T12:30:00Z",
  "requestId": "req_9f3a",
  "correlationId": "corr_1c77"
}
```

### Get Verdicts

`GET /dqc/v1/verdicts/{dataset}/{stage}`

Returns the latest verdict for the requested dataset and stage. Supports filters by run id, date range, and tenant id.

Query parameters
- `runId` optional  
- `from` optional RFC 3339  
- `to` optional RFC 3339  
- `tenantId` optional

Response 200
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "verdicts": [
    {
      "runId": "run_20251009_1230",
      "rulepackVersion": 3,
      "score": 98.76,
      "status": "PASS_WITH_WARNINGS",
      "criticalFailures": 2,
      "warnings": 48,
      "createdAt": "2025-10-09T12:30:00Z"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "total": 1
}
```

### Get Scorecards

`GET /dqc/v1/scorecards/{dataset}`

Returns dataset quality scores over time. The stage parameter is optional and defaults to gold.

Query parameters
- `stage` optional  
- `windowDays` optional default 30  
- `tenantId` optional

Response 200
```json
{
  "dataset": "finance_invoice",
  "stage": "gold",
  "runs": [
    {"date": "2025-10-05", "score": 99.2},
    {"date": "2025-10-06", "score": 98.9},
    {"date": "2025-10-07", "score": 99.0}
  ],
  "trend": "stable"
}
```

### Create Waiver

`POST /dqc/v1/waivers`

Creates a waiver that allows a specific rule to be bypassed for a limited time.

Request
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "ruleName": "range_invoice_amount",
  "approvedBy": "data_owner_1",
  "reason": "migration anomalies",
  "expiresOn": "2025-10-31T00:00:00Z",
  "tenantId": "t_0456"
}
```

Response 201
```json
{"waiverId":"wvr_7001","status":"active"}
```

### List Waivers

`GET /dqc/v1/waivers/{dataset}`

Lists waivers for a dataset. Filters include stage and active only.

Query parameters
- `stage` optional  
- `active` optional boolean

Response 200
```json
{
  "dataset": "finance_invoice",
  "waivers": [
    {
      "waiverId": "wvr_7001",
      "ruleName": "range_invoice_amount",
      "stage": "silver",
      "approvedBy": "data_owner_1",
      "expiresOn": "2025-10-31T00:00:00Z",
      "status": "active"
    }
  ]
}
```

### Rule Packs

`GET /dqc/v1/rulepacks/{dataset}/{stage}`

Gets the active rule pack and history for a dataset and stage.

Response 200
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "active": {"version":3,"activatedOn":"2025-10-09T10:00:00Z","activatedBy":"dq_admin"},
  "history": [
    {"version":2,"activatedOn":"2025-08-15T09:00:00Z","activatedBy":"dq_admin"}
  ]
}
```

`POST /dqc/v1/rulepacks`

Publishes a new rule pack version. Requires admin scope.

Request
```yaml
version: 3
dataset: finance_invoice
stage: silver
rules:
  - name: completeness_invoice_id
    type: completeness
    field: invoice_id
    threshold: 0.995
    severity: critical
  - name: uniqueness_invoice_id
    type: uniqueness
    field: invoice_id
    severity: critical
  - name: range_invoice_amount
    type: range
    field: invoice_amount
    min: 0
    max: 10000000
    severity: warning
```

Response 201
```json
{"version":3,"status":"published","shadow":true}
```

`POST /dqc/v1/rulepacks/{dataset}/{stage}:activate`

Activates a published rule pack version after shadow evaluation.

Request
```json
{"version":3,"notes":"activate after five shadow runs without regressions"}
```

Response 200
```json
{"version":3,"status":"active"}
```

## Idempotency And Caching

- Validation calls honor `Idempotency-Key` header to dedupe retried requests.  
- GET endpoints return ETag headers. Clients use `If-None-Match` to reduce payloads.  
- Rule pack publish operations are idempotent by version and dataset.

## Error Handling

Errors use a structured model with stable codes and details.

Example
```json
{
  "error": {
    "code": "RULEPACK_NOT_FOUND",
    "message": "Rule pack for dataset finance_invoice stage silver not found",
    "requestId": "req_9f3a",
    "correlationId": "corr_1c77",
    "details": {"dataset":"finance_invoice","stage":"silver"}
  }
}
```

Common codes
- VALIDATION_FAILED  
- RULEPACK_NOT_FOUND  
- RULEPACK_VERSION_CONFLICT  
- WAIVER_EXPIRED  
- UNAUTHORIZED  
- FORBIDDEN  
- NOT_FOUND  
- INTERNAL_ERROR

## Observability And Audit

- Each request logs request id, correlation id, dataset, stage, and actor.  
- Metrics include validation_duration_ms, rules_evaluated_total, dq_score, and dq_eval_error_total.  
- Audit entries are written for rule pack publish and activate, as well as waiver creation and expiry.  
- Structured logs contain no secrets and are retained per policy.

## Lifecycle Examples

### Pipeline triggered validation and promotion
1. Pipeline finishes Silver transformation.  
2. Pipeline calls `POST /dqc/v1/validate` with `runId` and partitions.  
3. Receives job id, polls or subscribes for completion.  
4. Reads verdict using `GET /dqc/v1/verdicts/{dataset}/{stage}`.  
5. If status is pass and no critical failures, promote to Gold.  
6. Publish Observability metrics and update Tenancy DQ badge via Scorecard API.

### Shadow rule pack rollout
1. Admin publishes rule pack version 3.  
2. System runs shadow evaluations for five runs.  
3. Admin activates version 3 via `:activate` endpoint.  
4. Observability watches for regressions during first week.  
5. Rollback to previous version if deny rates spike unexpectedly.

## Security Notes

- Tokens must carry appropriate scopes and may include tenantId claims.  
- All admin actions require audit notes in the request payload.  
- Rate limits protect the evaluator and history endpoints.  
- Payload size caps are enforced to prevent abuse.

## Summary

The DQC API provides a concise and deterministic interface for dataset validation, result retrieval, scorecards, waivers, and rule pack lifecycle. It integrates with Observability for metrics and Tenancy for tenant trust indicators, enabling safe promotions and transparent governance across data products.