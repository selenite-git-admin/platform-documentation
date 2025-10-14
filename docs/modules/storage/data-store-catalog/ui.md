# Data Store Catalog (Catalog) UI

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
Defines user interface patterns for discovering datasets and reading descriptors from Catalog. Focus is clarity, zero engineering usage, and alignment with PostgreSQL-first architecture.

## Principles
- Honest signals. UI shows exactly what the API returns.
- Minimal controls. Simple search and filters before advanced options.
- Fast by default. Use ETag validation and short-lived caching.
- Accessible. Text-first status, color as a secondary cue.
- Tenant safe. Only show items the caller can access.

## Primary Views
### Dataset list
Paginated table or grid of datasets with quick signals.

Columns
- Dataset id
- Title
- Layer
- Tags
- Owner
- Status badge from DRR when included via describe

Interactions
- Search by free text
- Filter by layer and tags
- Sort by title or last updated
- Select a dataset to open the descriptor panel

### Descriptor panel
Right-side panel or detail page for a single dataset.

Sections
- Identity: dataset id, title, summary, layer
- PostgreSQL coordinates: database, schema, name, location role
- Schema: version and link to schema document
- Ownership: module and contact
- Access: access class and role name
- Lineage: upstream and downstream ids
- Freshness: badge and last_success_at when included via describe
- Actions: copy API link, copy psql snippet

### Compare versions
Dialog to compare two schema versions.

Shows
- Versions side by side
- Compatibility mode
- Checksums and publish dates
- Diff summary if available

## Data flow
### List path
1. Call `GET /storage/v1/catalog/datasets?limit=50&layer=&tag=&q=`.
2. Render rows with title, tags, and basic metadata.
3. Prefetch describe for visible rows when the viewport settles.

### Detail path
1. Call `GET /storage/v1/catalog/datasets/{id}:describe?include=freshness`.
2. Render descriptor and, if present, DRR freshness badge.
3. Provide copyable psql snippet for the primary location.

## UI components
### Status badge
Text plus color where applicable.

States
- fresh: green, tooltip includes last_success_at
- late: amber, tooltip includes lag
- failing: red, tooltip includes last failure time
- unknown: gray, tooltip explains no recent update

### Tag pill
Clickable label with count badge, filters list by tag on click.

### Code snippet
Copyable block with connection example.
```
psql "host={DB_HOST} dbname=platform_store user=reporter sslmode=require" -c "select * from {schema}.{name} limit 10;"
```

## Error handling
| Scenario | Behavior |
|----------|----------|
| 404 not found | Show message and link back to list |
| 403 forbidden | Show access denied with support link |
| 429 rate limit | Retry after header surfaced in toast |
| 5xx server error | Keep cached value and show banner |
| Network timeout | Show skeleton and auto retry |

## Caching
- Use `ETag` and `If-None-Match` for all GET requests.
- Default cache TTL is 60 seconds for list and 30 seconds for detail.
- Persist last known descriptor for back navigation.

## Accessibility
- All badges include text labels.
- Keyboard navigation across list, filters, and actions.
- Screen reader labels for status and timestamps.
- Live region updates when freshness changes.

## Internationalization
- Time shown in UTC with relative labels next to the ISO timestamp.
- Message catalog under `i18n/catalog/*.json`.
- Avoid concatenated strings; use ICU formats.

## Performance
- Virtualize lists with more than 50 rows.
- Debounce search at 200 ms.
- Batch describe fetches to 10 requests per second.
- Prefer list endpoint for overview instead of N+1 describe calls.

## Telemetry
- `ui.catalog.list.rendered` with result count.
- `ui.catalog.describe.rendered` with dataset id.
- `ui.catalog.error` with code and endpoint.
- `ui.catalog.copy.snippet` when code block copied.

## Contracts
### List response
```json
{
  "items": [
    {
      "dataset_id": "gdp.sales_invoice_v3",
      "layer": "gdp",
      "title": "Sales Invoice",
      "tags": ["finance"]
    }
  ],
  "count": 1,
  "cursor": "eyJvZmZzZXQiOjEwfQ=="
}
```

### Describe response with freshness
```json
{
  "dataset": {
    "dataset_id": "kpi.cash_conversion_cycle_v2",
    "layer": "kpi",
    "physical": [
      {"type":"postgres_table","database":"platform_store","schema":"kpi","name":"cash_conversion_cycle_v2","is_primary": true}
    ],
    "schema_uri": "s3://schemas/kpi/cash_conversion_cycle_v2/1.4.0/json",
    "owner": {"module": "kpi-service", "email": "kpi-owners@example.com"},
    "access_class": "read_internal",
    "tags": ["finance","executive"]
  },
  "freshness": {
    "status":"fresh",
    "last_success_at":"2025-10-12T06:02:14Z",
    "freshness_lag_sec": 421,
    "freshness_slo_sec": 10800
  }
}
```

## QA checklist
- [x] ETag validation prevents unnecessary fetches
- [x] RLS confirmed by attempting to open an unauthorized dataset
- [x] Compare dialog shows compatibility and version metadata
- [x] Copy snippets match the primary location
- [x] Error banners include correlation id

## Ownership
- Product: Data Platform
- Engineering: Platform Foundation
- Design: Core UX