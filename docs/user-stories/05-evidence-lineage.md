# Evidence

> Goal: Capture immutable evidence and lineage for audits and investigations.  
> Scope: Covers audit logging, evidence packaging, lineage capture, and export.

## Context
Every meaningful action and data change must be traceable.  
This story sets up evidence capture and lineage so that any KPI or workflow outcome can be explained to auditors and stakeholders.  
Exports must be regulator ready and reproducible.

## Actors (Personas and Roles)
- Compliance Officer: defines evidence policies and retention rules  
- Platform Admin: enables evidence capture and export endpoints  
- Auditor: reviews and downloads evidence packs  
- Observability Engineer: verifies completeness of evidence streams

## Preconditions
- Guardrails and DQC in place  
- Evidence store provisioned  
- Lineage metadata model available

## Scenario Flow
1. Compliance Officer defines evidence retention and export policy  
2. Platform Admin enables audit logging on key services and routes logs to evidence store  
3. Lineage capture configured for raw to GDP to KPI transformations and for workflow execution  
4. Evidence export templates created for internal reviews and regulator requests  
5. Auditor verifies sample exports and cross checks lineage references

## Acceptance Criteria
- Evidence logs present for key events and linked to identities  
- Lineage captured across data and action flows  
- Evidence export templates available and tested  
- Retention policy applied

## Failure Paths
- Missing event logging: evidence gaps detected and incident created  
- Lineage break: transformation step lacks trace and remediation is required  
- Export mismatch: template fails validation and corrected template is published

## Observability and Governance
- Audit Events: evidence.enabled, lineage.captured, export.generated  
- Metrics: evidence_completeness_rate, lineage_link_rate  
- Evidence: sample export packs and lineage graphs

## Interfaces and Cross Links
- Previous: [Setting Up Guardrails and Data Quality Controls](04-guardrails-dqc.md)  
- Next: [Automated Housekeeping and Cost Controls](05b-housekeeping-cost-controls.md)

## Configuration Examples

**Evidence Export Template (YAML)**
```yaml
template_id: EV-STD-01
sections:
  - action_receipts
  - kpi_snapshots
  - lineage_diagrams
  - identity_map
retention_years: 7
```

**Lineage Record (JSON)**
```json
{
  "kpi": "DSO",
  "source_tables": ["raw_invoices", "gdp_ar"],
  "transformations": ["std_currency", "dedupe_by_invoice_id"],
  "workflow_receipts": ["WF-12345"],
  "evidence_id": "EV-2025-09-29-001"
}
```

## BDD Scenarios

### Scenario: Evidence export is generated for a workflow
```gherkin
Given evidence capture is enabled
When a workflow executes
Then an evidence pack is generated
And the pack contains action receipts and lineage references
```

### Scenario: Lineage gap triggers an incident
```gherkin
Given lineage capture is configured
When a transformation lacks a lineage record
Then an incident is created
And remediation is tracked to closure
```

## Review Checklist
- [x] Evidence capture enabled  
- [x] Lineage captured end to end  
- [x] Export templates tested  
- [x] Retention policy enforced  
