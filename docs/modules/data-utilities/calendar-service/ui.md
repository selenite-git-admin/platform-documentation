# UI

## Scope
Screen definitions for Calendar Service. This page lists required screens, where they belong, their data elements, and API dependencies.

## Placement
- Platform Admin App: authoring and operations
- Tenant App: read only effective calendars when exposed

## Screens at a glance
| Screen | App | Purpose |
| --- | --- | --- |
| [Calendar definitions and events](#calendar-definitions-and-events) | Platform Admin App | Manage calendar definitions and events |
| [Calendar sets](#calendar-sets) | Platform Admin App | Build reusable sets |
| [Tenant overlay](#tenant-overlay) | Platform Admin App | Configure per tenant overlays and preview effective calendar |
| [Fiscal calendars](#fiscal-calendars) | Platform Admin App | Define fiscal calendars and periods |
| [Date Table](#date-table) | Tenant App | Configure profiles and export rows |
| [Tenant organizational settings](#tenant-organizational-settings) | Tenant App | Set week start, weekends, defaults |

## Calendar definitions and events
API
- [List calendar definitions](api.md#list-calendar-definitions)
- [List calendar events](api.md#list-calendar-events)
- [Create calendar definition](api.md#create-calendar-definition)
- [Create calendar event](api.md#create-calendar-event)

## Calendar sets
Wireframe

<a href="#fig-cal-sets" class="image-link">
  <img src="/assets/diagrams/calendar-service/calendar-sets-editor.svg" alt="Calendar sets editor">
</a>

<div id="fig-cal-sets" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/calendar-service/calendar-sets-editor.svg" alt="Calendar sets editor">
</div>

_Figure 1: Calendar sets editor_{.figure-caption}

API
- [List calendar sets](api.md#list-calendar-sets)
- [Create calendar set](api.md#create-calendar-set)

## Tenant overlay
Wireframe

<a href="#fig-cal-overlay" class="image-link">
  <img src="/assets/diagrams/calendar-service/tenant-overlay-editor.svg" alt="Tenant overlay editor">
</a>

<div id="fig-cal-overlay" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/calendar-service/tenant-overlay-editor.svg" alt="Tenant overlay editor">
</div>

_Figure 2: Tenant overlay editor_{.figure-caption}

API
- [Get tenant overlay](api.md#get-tenant-overlay)
- [Put tenant overlay](api.md#put-tenant-overlay)
- [Resolve calendar set](api.md#resolve-calendar-set)

## Fiscal calendars
API
- [List fiscal calendars](api.md#list-fiscal-calendars)
- [List fiscal periods](api.md#list-fiscal-periods)


## Tenant organizational settings
Purpose
Configure week start, weekend days, default calendar set, timezone, and business hours for the tenant.

App
Tenant App

API
- [Get tenant settings](api.md#get-tenant-settings)
- [Put tenant settings](api.md#put-tenant-settings)
- [Resolve calendar set](api.md#resolve-calendar-set)

UX notes
- Use selects for week start and weekend days
- Business hours editor supports per-day ranges
- Preview effective business days using the selected calendar set and timezone

## Date Table
App
Tenant App

Purpose
Create Date Table profiles, pick columns, preview, and trigger materialize or export.

API
- [List date table profiles](api.md#list-date-table-profiles)
- [Create date table profile](api.md#create-date-table-profile)
- [Update date table profile](api.md#update-date-table-profile)
- [Materialize date table](api.md#materialize-date-table)
- [Export date table](api.md#export-date-table)
- [List available date columns](api.md#list-available-date-columns)

UX notes
- Column picker with common presets: Standard, ISO, Fiscal 445
- Preview first 50 rows with effective holidays marked
- Respect tenant timezone and locale on preview
