# Health UI

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define product patterns for visualizing service and data health across the platform. The UI provides a fleet view, drilldowns, freshness signals, and safe diagnostics without leaking sensitive information.

## Principles
- One glance clarity for operators
- Safe by default with minimal sensitive details
- Consistent with Health API response shapes
- Fast feedback on deploys and incidents
- Accessible and keyboard friendly

## Primary views
### Fleet overview
- Grid of services grouped by environment and region
- Status chips: ok, degraded, fail, unknown
- Counters: services ready, degraded, failing
- Filters: environment, region, service group
- Actions: open service details, copy summary to clipboard

### Service details
- Header shows service name, environment, region, version
- Status summary with last probe times and p95 readiness latency
- Dependency table
  - Columns: dependency, status, latency, hint, last checked
  - Filters: status, dependency type
- Readiness history chart with error bars
- Data health section if the service owns datasets
  - Cards per dataset with fresh, as_of, lag
- Links: open logs for last failure, open traces, open runbook

### Data health board
- Table of datasets with freshness and lag
- Filters: owner service, status, lag range
- Row actions: open dataset detail, copy as_of, view DRR entry

### Dataset detail
- Summary: name, owner service, current status, as_of, lag
- Sparkline of lag over time
- Validation results if available
- Evidence link when present
- Actions: open runbook, open DRR record

### Aggregator status
- Fleet rollup timeline
- Services missing or stale
- Aggregator job health and last snapshot time

## Components
### Status chip
Props: `state` = ok | degraded | fail | unknown
- Color coded with text label
- Includes an icon and aria label
- Works in tables and cards

### Probe badge
Props: `probe` = healthz | readyz | startupz | dataz, `state`
- Compact badge used in headers and toolbars

### Dependency table
Props: list of checks with `name`, `status`, `latency_ms`, `hint`, `ts`
- Sortable by latency and time
- Optional column for region when a service spans regions

### Dataset card
Props: `name`, `fresh`, `as_of`, `lag_minutes`
- Shows a small sparkline of recent lag
- Tooltip reveals last three checks with times
- Copy button for `as_of` value

### Error banner
- Uses platform error envelope
- Shows a short hint and correlation id
- Collapsible details for advanced users

### Empty state
- Clear message and primary action
- Secondary link to documentation
- Optional sample data screenshot for new users

## Navigation and information architecture
- Left nav: Fleet, Services, Data, Aggregator
- Global search for service name, dataset name, correlation id
- Breadcrumbs for dataset details
- Consistent action placement: primary actions top right, filters top left

## Accessibility
- All iconography has text labels and tooltips
- Keyboard navigation across grids and tables
- Focus visible on interactive elements
- Tables announce headers for screen readers
- Color contrast meets WCAG AA

## Telemetry
Emit UI events with correlation id when available
- `ui.health.fleet_opened`
- `ui.health.service_viewed`
- `ui.health.dataset_viewed`
- `ui.health.open_logs_clicked`
- `ui.health.open_traces_clicked`
- `ui.health.copy_summary_clicked`

## Copy guidelines
- Lead with status and action
- Avoid internal codes in primary copy
- Keep hints short and neutral
- Always include a correlation id when linking to logs or traces

Examples
- "Service is not ready. Open runbook and check database connectivity"
- "Dataset is late. View DRR entry for source run status"

## Safe diagnostics
- Do not show hostnames, IPs, usernames, or SQL text
- Hide stack traces by default
- Dataset names are public identifiers only
- Hints are short and non sensitive

## Error states
- Fleet unavailable
  - Message: "Fleet rollup is unavailable. Try again or open aggregator logs"
  - Actions: retry, open logs
- Service unreachable
  - Message: "Service did not respond to readiness probe"
  - Actions: open runbook, open last successful snapshot
- Data unavailable
  - Message: "Data health is not reported"
  - Actions: open DRR, open owner service

## Validation checklist
- [ ] Status chips render consistently
- [ ] Tables sort and filter correctly
- [ ] Timezones are clear and use UTC labels
- [ ] Links to logs and traces carry correlation id
- [ ] Copy to clipboard actions work in all supported browsers
- [ ] Screen reader workflow covers fleet to detail flow

## Summary
This UI presents platform health clearly and safely. Operators get fast situational awareness, direct paths to diagnostics, and consistent controls that align with the Health API and observability stack.