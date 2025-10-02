
# Schema Registry Module

## Purpose

The Schema Registry Module is the backbone of how the BareCount Data Action Platform governs data structure.  
It provides a single source of truth for all schema types: Extraction, Raw, Gold (GDP), KPI or Metrics, and Activation.  
The registry makes schemas explicit, versioned, validated, and auditable. This removes ambiguity across teams, ensures compatibility between producers and consumers, and prevents silent breakage when systems evolve.

The registry does not transform or persist data itself. Instead, it defines the structural contracts that other modules must follow.  
Compute modules use schemas to validate inputs and outputs. Storage modules enforce schemas at rest. Consumption modules expose schemas as part of their APIs. Trust records every schema decision in the evidence ledger. Access controls who can read, propose, approve, or deprecate schemas. Runtime provides the scheduling, observability, and error handling that keep the registry reliable.

## Why it matters

Enterprise data breaks down when structure is left implicit. Each source system (ERP, CRM, HRMS, manufacturing) names fields differently and applies unique constraints. Without alignment, even basic KPIs such as revenue or gross margin fragment into competing versions. The BareCount Data Action Platform solves this by requiring every dataset to be tied to a schema.  

Schemas give developers clarity, operators confidence, and auditors traceability. They are also the foundation for data residency, classification, and privacy enforcement. Every data product in the platform must reference a schema in order to exist.

## Capabilities

The Schema Registry Module provides the following capabilities:

- Schema types: manages Extraction, Raw, GDP, KPI, and Activation schemas  
- Versioning: ensures each schema family evolves under explicit versions  
- Compatibility rules: enforces backward or forward compatibility depending on use case  
- Lifecycle: supports proposal, approval, publication, deprecation, and retirement states  
- Validation: validates sample payloads against published schemas before acceptance  
- Governance: enforces metadata such as owner, classification, PII tags, and residency  
- Events: emits lifecycle events (`schema.proposed`, `schema.approved`, `schema.published`, etc.) to Runtime  
- Evidence: records every approval and deprecation in the Trust evidence ledger  
- Discovery: exposes search and catalog APIs to find schemas by domain, entity, metric, or tags

## Boundaries

Owns:  
- Registry database for schema metadata  
- Artifact storage for schema definitions  
- Versioning and compatibility checks  
- Approval and deprecation workflow  
- Discovery and search APIs  

Does not own:  
- Job execution or data transformation (Compute)  
- Long-term data persistence (Storage)  
- User interface rendering (Applications)  
- Identity management (Access)  
- Cryptographic guarantees (Trust)  

## Lifecycle

Schemas move through well-defined states:

1. Proposed  
   Author submits draft schema with metadata such as owner, classification, and intended use.  

2. Approved  
   Host policy checks pass. An impact report is generated to show which datasets, KPIs, or APIs will be affected.  

3. Published  
   Schema becomes current for its family. Registry emits a `schema.published` event. All new datasets must comply.  

4. Deprecated  
   A cutoff date is announced. Migration guidance is provided. Deprecation windows vary by type:  
   - Extraction and Raw: 90 days  
   - GDP and KPI: 120 days  
   - Activation: 180 days  

5. Retired  
   Schema is closed to writes. Consumers may still read for audit. Evidence of retirement is written to Trust.

Rollback is supported. The previous Published version can be restored during the deprecation window. Every rollback is logged and evidenced.

## How it works

- Schema proposal: Developers submit schemas through the API. Metadata and JSON definition are required.  
- Validation: Payload samples are validated against the schema before approval. Compatibility is checked against previous versions.  
- Approval: Host administrators review. Trust records the decision. Access enforces approver roles.  
- Publication: Once published, schemas are discoverable by Compute, Storage, and Consumption modules.  
- Enforcement: Runtime injects schema validation into jobs. Storage validates records before commit. Consumption ensures API payloads conform.  
- Deprecation: Events notify consumers. Migration plans are distributed. Evidence is logged.  

## Governance

Every schema must include metadata:  

- Owner and approver  
- Business purpose  
- Data classification and PII flags  
- Retention and residency rules  
- Target storage layers  

Residency tags define where data governed by the schema may live. Approval is blocked if residency is undefined. Trust records the residency decision for audit.  

PII flags identify sensitive fields. Masking rules are enforced downstream in Compute and Storage. Classification tags flow to the catalog for discovery.

## Example schemas

### GDP schema

```json
{
  "$id": "gdp.sales.order:v3",
  "title": "Sales Order",
  "type": "object",
  "properties": {
    "order_id": { "type": "string" },
    "tenant_id": { "type": "string" },
    "customer_id": { "type": "string" },
    "order_date": { "type": "string", "format": "date-time" },
    "currency_code": { "type": "string", "pattern": "^[A-Z]{3}$" },
    "net_amount": { "type": "number" },
    "tax_amount": { "type": "number" },
    "total_amount": { "type": "number" },
    "discount_amount": { "type": ["number", "null"] }
  },
  "required": ["order_id", "tenant_id", "order_date", "currency_code", "net_amount", "total_amount"]
}
```

Notes:  
- currency_code must be ISO 4217  
- order_date must be UTC  
- Adding discount_amount as nullable is backward compatible  

### KPI schema

```json
{
  "$id": "kpi.cfo.gross_margin:v2",
  "title": "Gross Margin",
  "type": "object",
  "properties": {
    "period_key": { "type": "string" },
    "tenant_id": { "type": "string" },
    "revenue": { "type": "number" },
    "cogs": { "type": "number" },
    "gross_margin_pct": { "type": "number" }
  },
  "required": ["period_key", "tenant_id", "revenue", "cogs", "gross_margin_pct"]
}
```

Notes:  
- period_key must align with the Calendar Module  
- revenue and cogs must reference GDP sources  

## Integration with other modules

- Compute: fetches schemas to validate jobs and transformations  
- Storage: enforces schema before commit  
- Consumption: publishes schema as part of API metadata  
- Trust: stores evidence for approvals, deprecations, and residency  
- Access: enforces who can propose, approve, and read  
- Runtime: emits lifecycle events, schedules validations, and provides observability

## Operations

Service level objectives:  
- Read availability: 99.99 percent  
- Publish latency: 95th percentile under 200 ms  
- Validation throughput: 50 per second per tenant  

Metrics: publish count, validate count, read latency, queue depth.  
Logs: structured with request_id, tenant_id, schema_id, version, actor.  
Traces: per API call, linked to validation workers.  

Failure handling:  
- If policy engine is down, approvals block but reads continue  
- If storage is down, reads fallback to replicas and writes queue  
- If validation times out, retries occur with backoff and failures go to dead letter queues

Runbooks include how to promote schemas, roll back, and force deprecate with exception.

## Changelog

- 2025-09-30: Enriched version combining V1 depth with V3 structure
