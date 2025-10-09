# Data Quality Control (DQC) Rule Packs

**Audience:** Data platform engineers, data stewards, and governance teams  
**Status:** Working draft  
**Purpose:** Define the structure, composition, and operational lifecycle of Data Quality Control (DQC) rule packs. Rule packs provide declarative, versioned definitions of quality checks applied to datasets at different stages of the data pipeline. They ensure consistent evaluation across tenants and integrate with Observability and Tenancy for transparency and enforcement.

## Rule Pack Structure

Each rule pack is a versioned configuration file written in YAML or JSON. It describes validation rules grouped by dataset and stage. A rule specifies a name, type, target field, severity, threshold, and optional reference or expression.

**Generic YAML template**
```yaml
version: 1
dataset: <dataset_name>
stage: <bronze|silver|gold>
rules:
  - name: <rule_name>
    type: <completeness|uniqueness|range|referential|freshness|reasonability|business_logic>
    field: <column_name>
    expression: <optional_sql_expression>
    threshold: <float or int>
    min: <optional>
    max: <optional>
    reference: <optional_reference_dataset>
    severity: <warning|critical>
    action: <block|warn|log>
```

## Rule Categories

### Completeness
Ensures that required fields are populated within acceptable limits.
```yaml
- name: completeness_invoice_id
  type: completeness
  field: invoice_id
  threshold: 0.995
  severity: critical
  action: block
```

### Uniqueness
Validates that primary identifiers are distinct.
```yaml
- name: uniqueness_invoice_id
  type: uniqueness
  field: invoice_id
  severity: critical
  action: block
```

### Range
Checks that numeric or date values fall within defined limits.
```yaml
- name: range_invoice_amount
  type: range
  field: invoice_amount
  min: 0
  max: 10000000
  severity: warning
  action: warn
```

### Referential Integrity
Ensures relationships between datasets remain consistent.
```yaml
- name: referential_customer_id
  type: foreign_key
  field: customer_id
  reference: customer_master.customer_id
  severity: critical
  action: block
```

### Timeliness
Checks for acceptable data arrival and processing delay.
```yaml
- name: timeliness_load_delay
  type: freshness
  max_delay_minutes: 30
  severity: warning
  action: warn
```

### Reasonability
Compares current values to historical or statistical bounds.
```yaml
- name: reasonability_invoice_amount
  type: reasonability
  field: invoice_amount
  expression: "invoice_amount between p1(invoice_amount) and p99(invoice_amount)"
  severity: warning
  action: warn
```

### Duplicate Detection
Detects duplicate rows or near-duplicate fingerprints.
```yaml
- name: duplicate_detection_invoice
  type: duplicate_detection
  field: [invoice_id, customer_id, invoice_date]
  threshold: 0.001
  severity: warning
  action: log
```

### Business Logic
Implements dataset-specific rules that express domain knowledge.
```yaml
- name: business_rule_tax_consistency
  type: business_logic
  expression: "abs(invoice_amount * tax_rate - tax_amount) < 1"
  severity: warning
  action: warn
```

## Stage-Based Rule Packs

Rule packs are defined per stage to enforce different validation levels.

### Bronze Stage
Focus on structure and schema validation.
```yaml
version: 2
dataset: sales_raw
stage: bronze
rules:
  - name: schema_conformance
    type: schema
    expression: "columns == expected_columns"
    severity: critical
  - name: completeness_key_fields
    type: completeness
    field: order_id
    threshold: 0.98
    severity: warning
```

### Silver Stage
Adds referential, range, and timeliness checks.
```yaml
version: 3
dataset: sales_enriched
stage: silver
rules:
  - name: referential_customer_id
    type: foreign_key
    field: customer_id
    reference: customer_master.customer_id
    severity: critical
  - name: range_order_amount
    type: range
    field: order_amount
    min: 1
    max: 100000
    severity: warning
  - name: timeliness_delivery_delay
    type: freshness
    max_delay_minutes: 60
    severity: warning
```

### Gold Stage
Focus on business-level consistency and statistical checks.
```yaml
version: 1
dataset: finance_revenue
stage: gold
rules:
  - name: reasonability_net_margin
    type: reasonability
    field: net_margin
    expression: "net_margin between 0 and 1"
    severity: warning
  - name: business_rule_profit_consistency
    type: business_logic
    expression: "abs(revenue - cost - profit) < 10"
    severity: critical
  - name: duplicate_detection_transactions
    type: duplicate_detection
    field: [invoice_id, period]
    threshold: 0.0005
    severity: warning
```

## Versioning And Lifecycle

- Each rule pack carries a version number and dataset identifier.  
- New versions are deployed in shadow mode for dry-run validation.  
- Only validated rule packs are promoted to active state.  
- Rule packs can be rolled back using previous version tag.  
- Deprecation requires explicit governance approval.

**Example metadata record**
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "version": 3,
  "activated_by": "dq_admin",
  "activated_on": "2025-10-09T10:00:00Z",
  "status": "active",
  "shadow_runs": 5,
  "previous_version": 2
}
```

## Validation Precedence And Severity

- Rules execute in deterministic order by type, then severity.  
- Critical rules can block data promotions.  
- Warning rules generate Observability metrics but do not block.  
- All violations are logged with rule name, severity, and dataset ID.

**Example validation precedence**
1. Schema and completeness  
2. Referential integrity  
3. Range and reasonability  
4. Timeliness and duplicates  
5. Business logic and warnings

## Promotion Gating And Overrides

- DQC Evaluator enforces promotion gates using rule severity.  
- Critical rule failure results in **block**.  
- Warnings are recorded but do not stop promotions.  
- Waivers can temporarily allow bypass of specific rules with expiry.  
- All gate decisions are logged and auditable.

**Example gate response**
```json
{
  "dataset": "finance_invoice",
  "stage": "silver",
  "passed": false,
  "blocking_rule": "referential_customer_id",
  "waiver_applied": false,
  "promotion_allowed": false,
  "timestamp": "2025-10-09T12:50:00Z"
}
```

## Integration With Observability

- Observability visualizes DQC rule-level metrics such as pass_rate and fail_count.  
- Violations generate events that trigger alerts and dashboards.  
- DQC exports dq_rule_latency_ms and dq_eval_error_total metrics.  
- Observability drilldowns link to rule names and versions.  

## Integration With Tenancy

- Tenancy aggregates dataset rule results into tenant trust indicators.  
- Rule pack metadata contributes to per-tenant DQ scoring.  
- Tenant dashboards display last validation time, failed rule count, and trust badge.  
- DQC API provides `/scorecards?tenantId=` endpoint for tenancy queries.

## Governance And Publishing Flow

1. Data steward authors rule pack draft.  
2. Governance board reviews and approves rules.  
3. Rule pack stored in configuration repository and version tagged.  
4. DQC registry publishes pack to Evaluator service.  
5. Shadow evaluation validates pack before activation.  
6. Observability monitors impact after rollout.  

**Example publishing record**
```json
{
  "dataset": "sales_enriched",
  "version": 3,
  "submitted_by": "data_steward_2",
  "reviewed_by": "dq_governance_team",
  "activated_on": "2025-10-10T09:30:00Z",
  "status": "active"
}
```

## Summary

Rule packs are the operational backbone of DQC. They encode expectations for dataset integrity, enforce consistency across pipeline stages, and enable transparent governance through versioning and metrics. Integration with Observability ensures visibility, while Tenancy provides per-tenant data trust indicators. The rule pack framework delivers deterministic, auditable, and adaptable data quality enforcement across the platform.