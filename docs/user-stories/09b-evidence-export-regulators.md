# Evidence Export for Regulators

> Goal: Provide a repeatable export of evidence for external regulators.  
> Scope: Covers export configuration, generation, verification, and delivery.

## Context
Regulators and external auditors require structured evidence of controls, actions, and outcomes. The platform must produce consistent exports that include identity mapping, lineage, and action receipts.

## Actors (Personas and Roles)
- Compliance Officer: defines export scope and approves release
- Platform Admin: executes export generation and delivery
- Auditor or Regulator: receives and reviews export packs

## Preconditions
- Evidence capture enabled
- Export templates configured
- Access controls verified for export recipients

## Scenario Flow
1. Compliance Officer selects export template and time window
2. Platform Admin generates export pack
3. System validates completeness and produces a hash for integrity
4. Export delivered to secure destination and access logged
5. Compliance Officer receives confirmation and archive entry

## Acceptance Criteria
- Export pack contains required sections and passes integrity check
- Access control validated for recipients
- Archive entry created with retention policy applied

## Failure Paths
- Missing evidence: export fails completeness check
- Integrity mismatch: hash verification fails and export blocked
- Delivery failed: secure channel error and retry

## Observability and Governance
- Audit Events: export.requested, export.generated, export.delivered
- Metrics: export_success_rate, export_generation_time
- Evidence: export manifest and integrity hash

## Interfaces and Cross Links
- Previous: [Decision Making](09-decision-audit.md)
- Next: [Monitoring](10-observability-monitoring.md)

## Configuration Examples

**Export Manifest (YAML)**
```yaml
export_id: EV-2025-09-29-001
template: EV-STD-01
sections:
  - action_receipts
  - kpi_snapshots
  - lineage_graphs
  - identity_map
integrity:
  sha256: "a7d3..."
status: delivered
```

## BDD Scenarios

### Scenario: Evidence export generated and delivered
```gherkin
Given evidence capture is enabled
When a Compliance Officer requests an export
Then the system generates the pack
And delivers it to the configured destination
```

### Scenario: Export blocked due to completeness failure
```gherkin
Given evidence capture is enabled
When required evidence is missing
Then the export is blocked
And the system reports a completeness error
```

## Review Checklist
- [x] Template selected
- [x] Integrity checked
- [x] Delivered securely
- [x] Archived with retention
