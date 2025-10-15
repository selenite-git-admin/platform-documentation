# Notifications UI

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define product-facing patterns for composing, previewing, sending, and viewing the status of notifications. The guidance applies to admin consoles and embedded flows. It is channel agnostic and follows the platform's error envelope and accessibility standards.

## Principles
- Consistent patterns across channels
- Clear next step for the user
- Privacy by default and least information on screen
- Fully accessible: keyboard, screen reader, and color safe
- Observable behavior: every action maps to telemetry and correlation ids

## Primary screens
1. **Template catalog**: browse and search templates by name, id, channel coverage, locale, and active version
2. **Template authoring**: edit localized versions with schema-aware variables
3. **Preview and test send**: render with variables, send to test user, verify delivery
4. **Send programmatically**: developer view with request payload examples and SDK snippets
5. **Status and audit**: track requests, attempts, bounces, complaints, and provider ids
6. **Destinations**: tenant channel configuration and verification status
7. **Suppressions**: search and manage suppressed addresses or endpoints

## Information architecture
- Navigation groups: Templates, Destinations, Suppressions, Activity, Settings
- Search is global and supports template id, tenant, correlation id, provider id
- Details pages use a two-column layout: summary on the left, drill-down and timeline on the right

## Template catalog
- Columns: Template, Locales, Active Version, Channels, Last Updated
- Filters: Channel, Locale, Active/Inactive
- Row actions: View, Edit, Preview, Versions

## Template authoring
- Rich text editor for email HTML and plain text with live preview
- Variables panel shows schema with types and hints
- Validation runs on change using the same engine as the API
- Versioning workflow: Draft → Validate → Activate
- Guardrails
  - No executable logic
  - Link host allow list enforced
  - Size caps for HTML and text
- Actions: Save draft, Validate, Activate, Deactivate version

## Preview and test send
- Inputs: Locale, Channel, Variables (auto-generated form from schema)
- Preview panes: Text and HTML for email, payload for webhook
- Actions: Send test to self, Send to selected users, Copy rendered body to clipboard
- Safety: Test sends are flagged and rate limited

## Status and audit
### Request list
- Columns: Time, Template, Tenant, Channels, Status, Correlation Id
- Filters: Status, Channel, Tenant, Time range
- Clicking a row opens the **Request details** view

### Request details
Sections:
- Summary: Template, Version, Tenant, Submitted by, Priority
- Channel attempts: one card per channel with state, retry count, provider id, and timings
- Timeline: request accepted, queued, attempt started, attempt completed, callback received
- Evidence: link to Evidence Ledger entries by correlation id
- Actions: Retry failed channel, Cancel pending, Open support with prefilled correlation id

### Bounce and complaint drilldown
- Surfaced only for email
- Show bounce type, timestamp, provider diagnostic code, and suppression status
- Resubscribe flow when appropriate and authorized

## Destinations
- Card per channel with verification state and last check time
- Email: domain verification, DKIM keys, From address
- Slack: bot token status and workspace
- Webhook: endpoint list with last success, signature status, and enable toggle
- Actions: Verify, Rotate secret, Disable

## Suppressions
- Search by address, tenant, or reason
- Show reason and expiry
- Actions: Remove suppression with confirmation and reason
- Audit entries created for all changes

## Components
### Notification status badge
Props: `state` = queued | pending | delivered | failed | dead_lettered | partially_delivered
- Color and icon reflect state
- Label uses sentence case

### Attempt card
Props: `channel`, `state`, `attempts`, `providerId`, `deliveredAt`, `lastErrorCode`
- Secondary section toggles to show raw details when permitted
- Copy buttons for provider id and correlation id

### Template variables form
- Auto-generated from JSON Schema
- Type-aware inputs with default hints
- Inline validation messages with aria support

### Test send modal
Props: `templateId`, `version`, `channel`, `to`
- Shows cost estimate if applicable
- Requires confirmation for external addresses

### Error banner
- Uses platform error envelope
- Collapsible details reveal correlation id and safe hints

## Copy guidelines
- Avoid jargon and internal codes in the main message
- Lead with action
- Keep sentences short and specific
- Always provide a secondary path to support with the correlation id

Examples:
- "Cannot send. Fix the highlighted fields and try again"
- "Email domain is not verified. Verify the domain in Destinations"
- "Webhook failed to deliver. Retry later or disable the endpoint"

## Accessibility
- Page level errors use `role="alert"` and trap focus only when blocking
- Inline messages use `aria-live="polite"`
- All interactive elements reachable via keyboard and have visible focus
- Color contrast meets WCAG AA
- Large tables support column headers for screen readers and row actions are keyboard operable

## Telemetry
Emit UI metrics and attach correlation ids when available:
- `ui.notifications.request_opened`
- `ui.notifications.retry_clicked`
- `ui.notifications.test_send`
- `ui.notifications.suppression_removed`
- `ui.notifications.destination_verified`

## Empty states and recovery
- Templates: "No templates yet. Create one to get started"
- Destinations: "No destinations configured. Verify email domain to send emails"
- Activity: "No activity in the selected time range"
- Provide a "Try again" action for fetch errors and show cached data when available

## Security notes
- Never display secrets or provider tokens
- Mask email addresses in lists unless expanded by an authorized user
- Redact variables that carry PII in previews unless the user has the right role
- Confirm potentially destructive actions such as disabling a destination

## Developer mode
- Show sample API requests and SDK snippets for the current view
- Provide a curl and JSON example for `POST /notifications`
- Copy buttons for all code blocks

## QA checklist
- [ ] Schema validation errors appear inline and block activation
- [ ] Preview renders for all locales and channels
- [ ] Retry button honors Retry After when provided
- [ ] Status timeline matches events in logs
- [ ] Correlation id present on details views
- [ ] Suppression actions create audit records

## Summary
These UI patterns make notifications predictable for operators and clear for users. Templates are authored safely, previews are faithful, status is auditable, and recovery actions are a click away. The result is a console that accelerates safe delivery without exposing internals.