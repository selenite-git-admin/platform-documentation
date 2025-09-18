# Tenant App – Health Dashboards

## Purpose
Health dashboards provide visibility into the operational status of tenant workloads.  
They summarize system availability, data freshness, throughput, and error budgets.

## Capabilities
- **Service Status**
  - Current state of the Tenant App UI and BFF.
  - Dependency health for connected platform services.

- **Throughput and Latency**
  - P50 and P95 latencies for key operations.
  - Metrics for onboarding steps, report runs, and activation flows.

- **Error Budgets**
  - Burn rate views aligned to SLOs.
  - Recent incidents and open issues.
  - Retry queue depth and backlog.

- **Data Freshness**
  - Last updated timestamps for each onboarded source.
  - Lag targets defined per source contract.

## Roles Involved
- **Executives and Business Teams**
  - View high‑level status to confirm system reliability before making decisions.
- **Operators**
  - Monitor detailed signals for troubleshooting and remediation.
- **Admins**
  - Review source‑level freshness and contract compliance.

## Notes
- Dashboards are read‑only for decision roles.  
- All metrics are tagged with tenant and correlation IDs.  
- Historical trends are retained for incident review and capacity planning.  
