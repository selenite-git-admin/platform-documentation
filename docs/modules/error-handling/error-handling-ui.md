# Error Handling UI

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define product-facing patterns for presenting errors in the UI so users can recover quickly without exposing internal details. The guidance applies to web apps, consoles, and embedded widgets that consume the platform's APIs.

## Principles
- Clear, plain language. No stack traces or internal codes.
- One pattern for similar problems across the product.
- Show the action a user can take next.
- Always include the correlation id for support.
- Accessible by default: screen-reader friendly and keyboard navigable.

## Error Surfaces
### Inline field validation
Use when the user has provided invalid input.
- Place the message next to the field.
- Keep messages short and explicit.
- Do not rely on color alone. Provide text and an icon.
- Announce with `aria-live="polite"` on change.

Examples
- "Provide a tenant id"
- "Use a valid email address"

### Form-level summary
Use when multiple fields error or when server validation fails.
- Show a summary banner at the top of the form.
- Focus moves to the banner after submit fails.
- Provide anchor links to each invalid field.

Content
- One sentence summary: "Fix the highlighted fields"
- List of specific items with links: "Tenant id is required"

### Page-level error
Use for route-level failures (403, 404, 500) and data loading failures.
- Prominent banner or full-page empty state.
- Primary action: Retry, Back, or Request access.
- Secondary action: Open support with correlation id.

Copy examples
- 403: "You do not have access to this resource"
- 404: "We could not find that page"
- 500: "Something went wrong. Try again later"
- 429: "Too many requests. Please try again shortly"

### Toasts and non-blocking alerts
Use for transient issues that resolved or do not block the user.
- Keep toasts short and auto-dismiss.
- Provide a "Details" link to the console or logs when appropriate.

## Correlation Id
- Display the id in advanced details, not in the main message.
- Provide a copy button.
- Include the id in any support ticket prefill.

UI text
```
Trouble ID: 01JAH8ZJ0Z8Z0N7M1X6JZ8QW0T
```

## Retry Guidance
- If `details.retryable` is true, show a retry button with backoff.
- If `Retry-After` is present, disable the button and show a countdown.
- For `stale_read`, prompt the user to refresh the page or data before retrying.

## Access and Permissions
- For 403 show "Request access" path when it exists.
- Do not reveal whether a resource exists if the user lacks rights.
- When access is granted asynchronously, show a non-blocking "access requested" state.

## Data-specific Patterns
### Stale read (412)
- Banner: "This data changed. Refresh to continue."
- Action: "Reload" which re-fetches with the latest ETag.

### Conflict (409) and Already exists
- Banner: "This item already exists"
- Provide a link to the existing resource if safe to reveal.

### Validation failed (400)
- Show field errors and keep the user's data intact.
- Do not clear the form.

## Visual Language
- Use a consistent set of icons: info, warning, danger.
- Color is secondary to text. Provide sufficient contrast.
- Avoid technical jargon in the primary text.

## Components
### Error banner
Props: `variant`, `title`, `message`, `actions[]`, `correlationId`, `testId`

Behavior
- Collapsible details section for correlation id and diagnostics.
- Supports keyboard focus and escape to dismiss when non-blocking.

### Field message
Props: `for`, `message`, `assistiveText`, `testId`

Behavior
- Associates with form control via `aria-describedby`.
- Announces on change.

### Retry button
Props: `onRetry`, `disabledUntil`, `loading`, `testId`

Behavior
- Shows spinner when in progress.
- Disables until `Retry-After` countdown elapses.

## State Model
Use a simple, typed state for views that fetch data:
```
Idle → Loading → Loaded
                  ↘
                 Error
```
- Retry moves `Error → Loading` with backoff when applicable.
- Cache the last good state for quick rehydration after transient failures.

## Telemetry
Emit UI metrics to correlate with backend errors:
- `ui.error.view_rendered` with `code`, `endpoint`
- `ui.error.retry_clicked` with `code`, `retryable`
- `ui.error.support_opened` with `code`

## Accessibility
- `role="alert"` for blocking errors; `aria-live="polite"` for inline messages.
- Focus management puts the user at the start of the error summary.
- Provide text alternatives for all icons.
- Keyboard users can reach Retry and Support without a mouse.

## Content Guide
- Prefer short, specific messages: "Provide a tenant id"
- Avoid blame and avoid internal terminology.
- Use sentence case, no exclamation marks.
- Keep a glossary of standard phrases per code for consistency.

## Examples

### Page-level: 500 Internal
Title: "Something went wrong"  
Message: "Try again later. If the problem continues, contact support with the trouble id below."  
Actions: Retry, Back to home  
Details: Trouble ID and timestamp

### Page-level: 403 Forbidden
Title: "You do not have access"  
Message: "Request access or switch to another workspace."  
Actions: Request access, Switch workspace

### Inline: Validation
Field: Tenant id  
Message: "Provide a tenant id"  
Assistive: "You received this error from the server"

## QA Checklist
- [ ] Error banners include correlation id in details
- [ ] Focus moves to summary on submit failure
- [ ] Retry honors `Retry-After` countdown
- [ ] Stale read prompt refreshes data with ETag
- [ ] Messages are concise and avoid internal codes
- [ ] Color contrast AA compliant

## Ownership
- Design: Core UX
- Engineering: Platform Foundation
- QA: Shared with each module team

## Summary
Consistent UI handling of errors builds trust and shortens recovery time. With clear messages, accessible patterns, correlation ids, and guided retries, users can self-correct while operators retain strong forensics and control.