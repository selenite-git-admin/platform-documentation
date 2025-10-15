# Schema Registry — REST API Reference
> Context: API Access Layer • Owner: Platform Engineering • Last updated: 2025-10-07

## Purpose
Provide REST endpoints for interacting with the Schema Registry — allowing programmatic schema management, validation, publishing, drift detection, and lineage retrieval.  
This interface powers both the UI and CLI layers, enforcing authentication, observability, and governance integration via AWS API Gateway + Lambda.

---

## Architecture Overview
```mermaid
flowchart LR
  CLIENT[Client / UI / CLI] --> API[API Gateway]
  API --> LAMBDA[Lambda (Schema Registry Functions)]
  LAMBDA --> RDS[Registry Metadata DB]
  LAMBDA --> S3[S3 Schema Store]
  LAMBDA --> EV[EventBridge (Governance / Drift Events)]
  API --> COGNITO[AWS Cognito Auth]
  API --> CW[CloudWatch Metrics]
```
All API calls are authenticated (JWT via Cognito or IAM SigV4) and audited through CloudTrail.

---

## Base URL
```
https://api.datajetty.com/v1/schema/
```

---

## Authentication
| Method | Description |
|---|---|
| **AWS SigV4** | For backend services and Lambda functions using IAM roles. |
| **Cognito JWT Bearer Token** | For human or tenant-admin API users. |
| **API Key (Internal Only)** | Used in CI/CD or governance workflows; stored in Secrets Manager. |

Example:
```bash
curl -X GET https://api.datajetty.com/v1/schema/list   -H "Authorization: Bearer <JWT_TOKEN>"
```

---

## Endpoints

### 1. List Schemas
```
GET /list
```
Retrieves all schemas matching filter criteria.

| Parameter | Type | Description |
|---|---|---|
| `domain` | string | Optional filter by domain |
| `status` | string | One of `draft`, `validated`, `published` |
| `tenant` | string | Namespace filter |
| `limit` | integer | Pagination size |

**Response**
```json
{
  "schemas": [
    {"fqid": "finance.gdp.invoice:v1.2", "status": "published"}
  ],
  "count": 1
}
```

---

### 2. Fetch Schema
```
GET /fetch/{{fqid}}
```
Returns full schema definition, metadata, and lineage information.

**Response**
```json
{
  "fqid": "finance.gdp.invoice:v1.2",
  "payload": { "fields": [{"name":"invoice_id","type":"STRING"}] },
  "lineage": {"source": "raw.invoice_extract"}
}
```

---

### 3. Validate Schema
```
POST /validate
```
Validates schema structure and compatibility before publishing.

**Body**
```json
{ "fqid": "finance.gdp.invoice:v1.2" }
```

**Response**
```json
{ "result": "pass", "latency_ms": 423 }
```

---

### 4. Publish Schema
```
POST /publish
```
Publishes validated schema to global registry and triggers EventBridge `SchemaPublished`.

**Body**
```json
{ "fqid": "finance.gdp.invoice:v1.2" }
```

**Response**
```json
{ "status": "published", "timestamp": "2025-10-07T09:15:22Z" }
```

---

### 5. Diff / Version Comparison
```
GET /diff/{{fqid1}}/{{fqid2}}
```
Compares two schema versions.

**Response**
```json
{
  "added_fields": ["amount_tax"],
  "removed_fields": [],
  "changed_types": []
}
```

---

### 6. Drift Events
```
GET /drift/{{fqid}}
```
Fetches drift history and quarantined record metadata.

**Response**
```json
{
  "fqid": "finance.gdp.invoice:v1.2",
  "drifts": [{"detected_at": "2025-09-30T11:22:00Z", "field": "invoice_region"}]
}
```

---

### 7. Metrics
```
GET /metrics/{{fqid}}
```
Returns validation and performance metrics for schema or pipeline.

**Response**
```json
{
  "validation_success_rate": 99.3,
  "avg_latency_ms": 210,
  "drift_events": 0
}
```

---

## Rate Limits & Quotas
| Tier | Requests / Minute | Burst | Notes |
|---|---|---|---|
| Public | 60 | 10 | Tenant-level |
| Platform | 300 | 50 | Internal services |
| Admin | 1000 | 100 | Governance and Ops |

---

## Observability & Error Codes
| Code | Description | HTTP | Action |
|---|---|---|---|
| SCHEMA-400 | Invalid schema payload | 400 | Fix and retry |
| SCHEMA-401 | Unauthorized access | 401 | Reauthenticate |
| SCHEMA-404 | Schema not found | 404 | Verify FQID |
| SCHEMA-409 | Version conflict | 409 | Retry after diff check |
| SCHEMA-500 | Internal service error | 500 | Contact support |

---

## Example Workflow: Validate + Publish
```bash
# Validate draft schema
curl -X POST https://api.datajetty.com/v1/schema/validate -d '{"fqid":"finance.gdp.invoice:v1.2"}'

# Publish after validation
curl -X POST https://api.datajetty.com/v1/schema/publish -d '{"fqid":"finance.gdp.invoice:v1.2"}'
```

---

## References
- API Gateway Config: `/infra/api/schema_registry_apigw.yml`  
- Lambda Handlers: `/lambda/schema_registry_handler.py`  
- EventBridge Rules: `/events/schema_registry_events.json`  
- CloudWatch Dashboard: `/infra/monitoring/schema_registry_api_dashboard.json`  

---
