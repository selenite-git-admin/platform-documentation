# Anomaly Engine Integration

> Goal: Detect anomalies in KPIs and workflows.  
> Scope: Covers anomaly detection, alerts, integration with workflows, and evidence.

## Context
Anomaly detection provides early signals of issues or risks. The anomaly engine must integrate with workflows so that detected anomalies trigger reviews or corrective actions.

## Actors (Personas and Roles)
- Anomaly Engine: detects outliers and triggers alerts
- Workflow Author: configures anomaly rules in workflows
- Business Owner: reviews anomalies and decides actions
- Compliance Officer: validates anomaly evidence

## Preconditions
- KPI and workflow telemetry available
- Anomaly engine configured with thresholds and models
- Notification channels active

## Scenario Flow
1. Anomaly engine detects deviation in KPI or workflow signal
2. Alert generated and linked to context
3. Workflow triggered for review or corrective action
4. Business Owner reviews and decides outcome
5. Evidence captured

## Acceptance Criteria
- Anomalies detected accurately
- Alerts linked to workflows
- Evidence recorded

## Failure Paths
- False positive: anomaly dismissed
- False negative: anomaly undetected
- Evidence missing: compliance issue

## Observability and Governance
- Audit Events: anomaly.detected, anomaly.alert.generated, anomaly.workflow.triggered
- Metrics: anomaly_detection_rate, false_positive_rate, false_negative_rate
- Evidence: anomaly reports and receipts

## Interfaces and Cross Links
- Previous: [AI Actors in Workflows](15-ai-actors-workflows.md)
- Next: [Executive Dashboards](17-anomaly-tuning.md)

## Configuration Examples

**Anomaly Detection Config (JSON)**
```json
{
  "anomaly_id": "ANOM-2025-09-29-001",
  "signal": "DSO",
  "threshold": "45",
  "status": "DETECTED",
  "linked_workflow": "WF-ANOM-DSO-REVIEW"
}
```

## BDD Scenarios

### Scenario: Anomaly triggers workflow
```gherkin
Given an anomaly engine is configured
When a KPI deviation is detected
Then an alert is generated
And a workflow is triggered for review
```

### Scenario: Anomaly dismissed as false positive
```gherkin
Given an anomaly is detected
When Business Owner reviews and dismisses it
Then no corrective action is taken
And evidence is recorded
```

## Review Checklist
- [x] Anomalies detected
- [x] Alerts linked to workflows
- [x] Evidence recorded
