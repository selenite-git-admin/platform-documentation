# Dataset Refresh Registry (DRR) UI

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Purpose
This document defines the user interface patterns for consuming DRR freshness in product surfaces. It focuses on clear signals, predictable interactions, and resilient behavior when data is late or failing.

## Principles
- Truthful: freshness signals reflect DRR state without reinterpretation.
- Minimal: one primary indicator per dataset view.
- Accessible: status is perceivable to all users through text and color.
- Fast: render with cached state, validate in background.
- Tenant-safe: only show datasets that the user is authorized to see.

## Primary Components
### Freshness Badge
Compact indicator used in lists, tables, and headers.

| State | Label | Tooltip | Visual |
|-------|-------|---------|--------|
| fresh | Fresh | Last updated {relativeTime} | Green badge |
| late | Late | Exceeded freshness SLO by {lag} | Amber badge |
| failing | Failing | Last run failed at {time} | Red badge |
| unknown | Unknown | No update in the last 48 hours | Gray badge |

Rules
- Always include text labels next to color.
- Lag uses humanized format (minutes, hours).
- Tooltips include ISO timestamp for precision.

### Dataset Header
Used on dataset detail pages. Combines title, layer, and freshness.

Structure
- Title: dataset_id
- Meta: layer, owner module, tenant scope
- Freshness: primary badge + last_success_at
- Action: copy API link, open in Catalog

### Status Strip
Horizontal strip placed above data visualizations. Shows current status and remediation hint.

Examples
- Fresh: "Data is fresh as of 10:02 UTC"
- Late: "Data is late by 23 minutes"
- Failing: "Last refresh failed. Try again later"
- Unknown: "No recent refresh. Contact support if this persists"

## Data Flow
### Read Path
1. Render page with cached DRR state from local store for the dataset.
2. Validate with live call to `GET /storage/v1/datasets/{id}/freshness`.
3. If ETag unchanged, keep the cached state. If changed, update the UI.

### List Path
1. Fetch paged listing via `GET /storage/v1/datasets?tenant_id=&status=`.
2. Render table with badges and relative times.
3. Prefetch detail freshness for rows in viewport if not cached.

### Composite Describe
For views that also need coordinates, call
`GET /storage/v1/datasets/{id}:describe?include=freshness`.

## Error Handling
| Scenario | UI Behavior |
|----------|-------------|
| 404 not_found | Show "Dataset not registered" and remove actions |
| 403 forbidden | Show "You do not have access to this dataset" |
| stale_update or internal_error | Show "Status temporarily unavailable" and keep last known value |
| network timeout | Show skeleton loader and retry silently |

## Caching
- Use `ETag` and `If-None-Match` on all requests.
- Default cache TTL 30 seconds, extendable via user preference.
- Persist last known state in local storage for read paths.

## Accessibility
- Badge colors meet WCAG AA contrast.
- Provide `aria-live="polite"` updates when status changes.
- Tooltips include machine readable time and relative text.
- Keyboard focus order: dataset title, badge, actions.

## Internationalization
- Use ICU message format for time and durations.
- Timezones displayed as UTC by default; user preference supported.
- Language packs located under `i18n/drr/*.json`.

## Performance
- Render lists with virtualization for more than 50 rows.
- Defer tooltip fetches until hover or focus.
- Batch detail fetches to 10 requests per second per tab.
- Avoid N+1 by preferring the list endpoint for overviews.

## UI Contracts
### Freshness DTO
```json
{
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "status": "fresh",
  "last_success_at": "2025-10-12T06:02:14Z",
  "freshness_lag_sec": 421,
  "freshness_slo_sec": 10800
}
```

### List Response
```json
{
  "items": [
    {"dataset_id":"gdp.sales_invoice_v3","status":"late","freshness_lag_sec":14300,"last_success_at":"2025-10-12T00:00:00Z"}
  ],
  "count": 1,
  "cursor": "eyJvZmZzZXQiOjEwfQ=="
}
```

## UI States
- Loading: skeleton row with placeholder badges.
- Empty: "No datasets match your filters" with reset action.
- Error: banner with correlation id and retry button.
- Partial: cached content with subtle "Validating…" note.

## Telemetry
- Log `ui.drr.badge.rendered` with `dataset_id` and `status`.
- Track `ui.drr.fetch.error` with `code` and `endpoint`.
- Measure time to freshness with mark `ui.drr.freshness.ttr`.

## Sample Implementation Notes
- React components: `<FreshnessBadge status lag lastSuccessAt />`.
- Table integration: column renderer reads from DRR cache store.
- Global store keyed by `dataset_id`, values include `etag` and `updatedAt`.

## Security
- All UI requests include user JWT. No service tokens in browser.
- Tenant_id must be encoded in token and not passed in querystring.

## QA Checklist
- [x] Colorblind safe palette verified.
- [x] Timezone switch changes labels and tooltips.
- [x] Cached state invalidates with ETag change.
- [x] Pagination maintains filter state on back navigation.
- [x] Error banners show correlation id.

## Ownership
- Product: Data Platform
- Engineering: Platform Foundation
- Design: Core UX