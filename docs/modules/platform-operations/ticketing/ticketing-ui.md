# Ticketing UI

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Provide a clear and safe user experience for creating, triaging, and resolving tickets across all tenants. The UI is platform scoped with RBAC based visibility. It balances speed for operators with safety for tenant users, and aligns with the Ticketing API and data model.

## Design goals
- First glance clarity for backlog and breaches
- Fast creation for humans and reliable intake for systems
- Consistent state transitions and SLA cues
- Safe presentation without leaking sensitive data
- Keyboard and screen reader friendly

## Information architecture
- Global sections: Backlog, Incidents, Requests, Webhooks, Settings
- Saved views by role: My Work, On Call, Platform Incidents, Tenant Requests
- Search and filters persistent in the header
- Breadcrumbs for ticket detail

## Primary views
### Backlog
Grid and board that summarize open work. Designed for on call and coordinators.

Elements
- Filters: category, state, severity, tenant, assignee team, environment, region, time
- Table columns: key, title, state, severity, tenant, assignee, updated_at, SLA chip
- Board lanes by state for drag and drop between states when role allows
- Bulk actions: assign team, change state, add tag, add comment
- Export CSV with applied filters

### Ticket detail
Single page to understand context and act.

Header
- Key, state, severity, tenant, environment, region
- SLA chips for ack, first response, resolution
- Actions: change state, assign, add comment, add link, add attachment

Body
- Summary section with requester, source, visibility, idempotency key
- Timeline of events: state changes, comments, webhooks, evidence links
- Links section: datasets, services, jobs, incidents, evidence
- Attachments with antivirus status and size
- Suggested actions based on category and recent failures

### Create ticket
Form with compact sections and smart defaults.

Fields
- Category and subcategory
- Severity and optional priority
- Title and summary
- Tenant scope or platform incident checkbox
- Environment and region
- Optional links and tags
- Preview before submit
- Idempotency key auto generated if caller is a human

### Webhooks status
Operational view for outbound deliveries.

Elements
- Recent deliveries table: target, status, latency, attempts, last error
- Filters by target, status, and time
- Resend and quarantine actions with confirmation

### Settings
Operator only. Manage routing rules, SLA policies, and webhook subscriptions.

## Components
### Status chip
Props: `state` in new, ack, in_progress, wait_requester, wait_dependency, resolved, closed, canceled. Shows color, label, and aria label.

### SLA chip
Props: `kind` and `due_at`. Shows remaining time, neutral when far, warning when near, danger when overdue. Tooltip shows due, started, paused.

### Tenant badge
Props: `tenant_id` or platform. Renders short name and icon. Clicking opens tenant summary panel.

### Visibility pill
Props: `visibility` in platform_only, tenant, mixed. Tooltips explain who can view the item.

### Comment editor
Supports markdown with live preview. Redaction helper suggests trims for emails, phone numbers, ids. Visibility can be set per comment when role allows.

### Link picker
Search across datasets, services, jobs, and incidents. Adds a typed relation. Shows last health for the selected object when available.

### Attachment uploader
Client side size checks and file type allow list. Upload uses a signed URL and shows progress. Antivirus scan status appears after upload.

## Accessibility
- WCAG AA contrast
- Full keyboard navigation
- Focus visible on all interactive elements
- Live regions for toast messages
- Table headers are announced for screen readers
- Drag and drop has keyboard alternative

## Telemetry
Emit events with correlation id when available
- `ui.ticketing.view_backlog`
- `ui.ticketing.view_ticket`
- `ui.ticketing.create_opened`
- `ui.ticketing.created`
- `ui.ticketing.state_changed`
- `ui.ticketing.assigned`
- `ui.ticketing.webhook_resend`
- `ui.ticketing.settings_updated`

## Safe content guidelines
- Do not show raw stack traces, SQL, hostnames, or credentials
- Mask PII by default. Use redaction helper in comments
- Truncate long summaries in tables. Full content in detail view only
- Show tenant badges and visibility pills to reduce confusion
- Attachments always open through time limited signed URLs

## RBAC behavior in UI
- Tenant users see tickets where tenant_id matches their scope and visibility is tenant or mixed
- Platform operators see all tickets and can set visibility to platform_only when needed
- Dangerous actions are role gated. Bulk actions require confirmation with a typed token when impact is high

## Empty and error states
- Empty search: explain filters and suggest clearing a few
- No access: state who to contact for permission
- API error: show a short message and correlation id with a copy button

## Performance notes
- Virtualized tables for large backlogs
- Incremental loading with cursor based pagination
- Aggressive client side caching for filters and saved views
- Lazy load of timeline items after header renders

## Copy guidelines
- Lead with the status and suggested action
- Keep hints short and neutral. Avoid internal codes in primary copy
- Always include a correlation id in error messages that link to logs

Examples
- Status: Readiness failing. Suggested action: Open runbook and check database connectivity
- Status: Dataset is late. Suggested action: View DRR entry for source status

## Sample layouts
### Backlog table header
`[Search box] [Filters] [Saved view] [Export]`
### Ticket header
`[Key] [Severity] [State chip] [SLA chips] [Tenant badge] [Visibility pill] [Actions]`

## Validation checklist
- [ ] Backlog filters and saved views are persisted
- [ ] SLA chips compute correctly across timezones and daylight changes
- [ ] Visibility control hides platform_only content from tenant roles
- [ ] Timeline items stream in without blocking header
- [ ] Copy to clipboard for correlation id works
- [ ] CSV export honors filters
- [ ] Attachment upload validates type and size and shows antivirus result

## Summary
This UI makes platform and tenant work visible without leaks. Operators move quickly with clear signals, tenants see only their own work, and every action aligns with the Ticketing API and security model.