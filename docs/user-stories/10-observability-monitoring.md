# Monitoring

> Goal: Provide real time visibility into platform health and data flows.  
> Scope: Covers metrics, logs, traces, dashboards, and alerts.

## Context
Operations teams need to detect and resolve issues quickly. Monitoring provides signals across compute, storage, connectors, pipelines, workflows, and user actions.

## Actors (Personas and Roles)
- Observability Engineer: defines metrics and dashboards
- Platform Admin: responds to alerts and tracks SLOs
- Security Admin: reviews security-related signals

## Preconditions
- Telemetry pipeline active
- Metrics and logging agents deployed
- Alert channels configured

## Scenario Flow
1. Observability Engineer defines SLIs and SLOs for key services
2. Dashboards published for platform and tenant scopes
3. Alerts configured with thresholds and runbooks
4. Platform Admin triages alerts and tracks resolution times

## Acceptance Criteria
- Dashboards show current health and trends
- Alerts fire with actionable runbooks
- SLO compliance tracked

## Failure Paths
- Missing metrics: dashboards incomplete
- Alert fatigue: thresholds too low and need tuning
- Runbook gap: alert without a documented response

## Observability and Governance
- Audit Events: monitoring.enabled, alert.fired, alert.resolved
- Metrics: alert_mean_time_to_ack, alert_mean_time_to_resolve, slo_breach_count
- Evidence: dashboard snapshots and alert transcripts

## Interfaces and Cross Links
- Previous: [Evidence Export for Regulators](09b-evidence-export-regulators.md)
- Next: [Incident Handling](10b-incident-handling.md)

## Configuration Examples

**Alert Rule (JSON)**
```json
{
  "alert_id": "CONN-ERROR-RATE",
  "scope": "connector:CRM",
  "expr": "error_rate > 2",
  "window": "5m",
  "action": "page_oncall"
}
```

## BDD Scenarios

### Scenario: Alert fires and is resolved within SLO
```gherkin
Given alert rules are configured
When error rate exceeds threshold
Then an alert is fired
And the on call resolves it within the SLO
```

### Scenario: Missing metrics cause blind spot
```gherkin
Given monitoring is enabled
When a critical service does not emit metrics
Then dashboards lack visibility
And an action item is created to add metrics
```

## Review Checklist
- [x] SLIs and SLOs defined
- [x] Alerts actionable
- [x] SLO tracking in place
