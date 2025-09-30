# Ops Connector Failure and Recovery

> Goal: Detect and recover from connector failures without data loss.  
> Scope: Covers failure detection, retry, escalation, and evidence.

## Context
Connectors link the platform with ERP, CRM, and other data systems. Failures can impact ingestion or actions. A recovery process is essential to maintain reliability and trust.

## Actors (Personas and Roles)
- Platform Admin: monitors connectors and triggers recovery
- Observability Engineer: configures alerts and monitors trends
- Tenant Admin: notified of tenant scope failures

## Preconditions
- Connectors deployed
- Monitoring and alerts active
- Retry policies defined

## Scenario Flow
1. Connector health check fails and triggers an alert
2. Retry policy attempts recovery automatically
3. If retries fail, Platform Admin intervenes
4. Incident logged and tenant notified if affected
5. Evidence recorded for audit

## Acceptance Criteria
- Failures detected and alerts triggered
- Recovery executed automatically or manually
- Evidence recorded

## Failure Paths
- Retry exhausted: manual intervention required
- Notification failure: incident escalated
- Evidence missing: compliance gap

## Observability and Governance
- Audit Events: connector.failure.detected, connector.recovery.started, connector.recovery.completed
- Metrics: connector_failure_count, mean_time_to_recover
- Evidence: incident logs and recovery receipts

## Interfaces and Cross Links
- Previous: [CFO Consumption and Activation](12-cfo-consumption-activation.md)
- Next: [Hybrid Deployment](14-hybrid-deployment.md)

## Configuration Examples

**Recovery Log (YAML)**
```yaml
connector_id: SAP-AR
failure: timeout
retries: 3
status: recovered
timestamp: "2025-09-29T12:30:00Z"
```

## BDD Scenarios

### Scenario: Connector recovers automatically
```gherkin
Given a connector fails
When the retry policy executes
Then the connector recovers
And a recovery receipt is recorded
```

### Scenario: Connector requires manual recovery
```gherkin
Given a connector fails
And retries are exhausted
When the Platform Admin intervenes
Then the connector is recovered manually
And an incident is logged
```

## Review Checklist
- [x] Failures detected
- [x] Recovery attempted
- [x] Evidence captured
