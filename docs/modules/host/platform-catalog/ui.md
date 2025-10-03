# UI

## Scope
Screen definitions for Platform Catalog. This page lists required screens, where they belong, their data elements, and API dependencies.

## Placement
- Platform Admin App: authoring and operations
- Tenant App: read only discovery of effective calendars if exposed

## Screens at a glance
| Screen | App | Purpose |
| --- | --- | --- |
| [Regions and residency](#regions-and-residency) | Platform Admin App | Manage regions and residency policies |
| [Plans and limits](#plans-and-limits) | Platform Admin App | Manage product plans, features, and defaults |
| [Tag taxonomy and namespaces](#tag-taxonomy-and-namespaces) | Platform Admin App | Manage allowed tags and namespace prefixes |
| [Calendars](#calendars) | Platform Admin App | Manage calendar definitions, events, and sets |
| [Tenant calendar overlay](#tenant-calendar-overlay) | Platform Admin App | Configure per tenant overlays and preview effective calendar |

## Regions and residency
Purpose
Edit lists of regions and residency policies.

API
- [List regions](api.md#list-regions)
- [List residency policies](api.md#list-residency-policies)
- [Upsert region](api.md#upsert-region)

## Plans and limits
Purpose
Manage product plans, feature flags, and default limits.

API
- [List product plans](api.md#list-product-plans)
- [Get plan features](api.md#get-plan-features)
- [Get default limits](api.md#get-default-limits)
- [Create plan](api.md#create-plan)
- [Upsert plan feature](api.md#upsert-plan-feature)
- [Upsert default limit](api.md#upsert-default-limit)

## Tag taxonomy and namespaces
Purpose
Maintain allowed tags and namespace prefixes used across the platform.

API
- [List tag taxonomy](api.md#list-tag-taxonomy)
- [List namespace prefixes](api.md#list-namespace-prefixes)
- [Upsert namespace prefix](api.md#upsert-namespace-prefix)
- [Upsert tag taxonomy entry](api.md#upsert-tag-taxonomy-entry)

## Calendars
Calendars moved to Calendar Service. See [Calendar Service UI](../../data-utilities/calendar-service/ui.md).

## Tenant calendar overlay
Tenant overlays moved to Calendar Service. See [Calendar Service UI](../../data-utilities/calendar-service/ui.md).

## Telemetry
- ui.catalog.region.upsert
- ui.catalog.plan.create
- ui.catalog.calendar.set.create
- ui.catalog.overlay.put

## Access
- Platform Admin App requires admin role for writes
- Tenant App read only endpoints are scoped by authorization
