# KPI Consumption

> Goal: Allow personas to view and use KPIs in dashboards and reports.  
> Scope: Covers access, filters, drill-through, and evidence of access.

## Context
Executives and analysts need to consume KPIs with confidence. Access should be role-based and interactions should be traceable for audit.

## Actors (Personas and Roles)
- Business Owner: reviews KPIs and decides actions  
- Analyst or Viewer: explores KPIs and exports reports  
- Compliance Officer: reviews access logs

## Preconditions
- KPI published  
- RBAC roles configured for the target personas

## Scenario Flow
1. User signs into Tenant App and opens the relevant dashboard  
2. KPI is displayed with thresholds, filters, and drill-through options  
3. User exports a snapshot or evidence for a meeting  
4. Access event is recorded for audit

## Acceptance Criteria
- KPI visible to allowed roles only  
- Filters and drill-through work as expected  
- Export available with evidence of access

## Failure Paths
- Access denied: RBAC misconfigured, incident created  
- KPI not found: publishing missing or dashboard error  
- Export failure: log error and provide retry

## Observability and Governance
- Audit Events: kpi.viewed, kpi.exported  
- Metrics: kpi_view_count, export_count  
- Evidence: access logs and export receipts

## Interfaces and Cross Links
- Previous: [KPI Publishing](06-kpi-publishing.md)

## Configuration Examples

**Access Log (JSON)**
```json
{
  "kpi_id": "DSO",
  "user": "cfo@tenant.com",
  "event": "kpi.viewed",
  "timestamp": "2025-09-29T12:15:00Z"
}
```

## BDD Scenarios

### Scenario: KPI consumed by authorized user
```gherkin
Given KPI is published
And the user has RBAC permission
When the user opens the dashboard
Then the KPI is visible
And an access log is recorded
```

### Scenario: KPI access denied due to RBAC
```gherkin
Given KPI is published
And the user lacks permission
When the user opens the dashboard
Then the KPI is not visible
And an incident is created
```

## Review Checklist
- [x] KPI visible to authorized roles  
- [x] Interactions functional  
- [x] Evidence captured  
