# API

## Scope
Read heavy APIs for Calendar Service with audited admin writes and working time utilities.

## Conventions
- Base path is `/calendar/v1`
- Requests and responses use `application/json`
- Authentication and authorization are handled by Access Modules
- Idempotency uses the `Idempotency-Key` header on POST and PUT
- ETags returned on cacheable reads. Accept `If-None-Match`
- Time uses UTC ISO 8601 unless a timezone parameter is provided

## Endpoints

### At a glance
| [Get tenant settings](#get-tenant-settings) | `GET /calendar/v1/tenants/{tenant_id}/settings` |
| [Put tenant settings](#put-tenant-settings) | `PUT /calendar/v1/tenants/{tenant_id}/settings` |

| Operation | Method and Path |
| --- | --- |
| [List calendar definitions](#list-calendar-definitions) | `GET /calendar/v1/definitions` |
| [List calendar events](#list-calendar-events) | `GET /calendar/v1/definitions/{calendar_id}/events` |
| [List calendar sets](#list-calendar-sets) | `GET /calendar/v1/sets` |
| [Resolve calendar set](#resolve-calendar-set) | `GET /calendar/v1/sets/{set_id}/resolve?tenant_id=&start=&end=&tz=` |
| [Get tenant overlay](#get-tenant-overlay) | `GET /calendar/v1/tenants/{tenant_id}/overlays` |
| [Put tenant overlay](#put-tenant-overlay) | `PUT /calendar/v1/tenants/{tenant_id}/overlays` |
| [List fiscal calendars](#list-fiscal-calendars) | `GET /calendar/v1/fiscal` |
| [List fiscal periods](#list-fiscal-periods) | `GET /calendar/v1/fiscal/{fiscal_id}/periods` |
| [Next business day](#next-business-day) | `GET /calendar/v1/working-time/next-business-day?start=&set_id=&tenant_id=&tz=` |
| [Add business days](#add-business-days) | `GET /calendar/v1/working-time/add-business-days?start=&days=&set_id=&tenant_id=&tz=` |
| [Business minutes between](#business-minutes-between) | `GET /calendar/v1/working-time/business-minutes-between?start=&end=&set_id=&tenant_id=&tz=` |
| [List date table profiles](#list-date-table-profiles) | `GET /calendar/v1/tenants/{tenant_id}/date-table/profiles` |
| [Create date table profile](#create-date-table-profile) | `POST /calendar/v1/tenants/{tenant_id}/date-table/profiles` |
| [Update date table profile](#update-date-table-profile) | `PUT /calendar/v1/tenants/{tenant_id}/date-table/profiles/{profile_id}` |
| [Materialize date table](#materialize-date-table) | `POST /calendar/v1/tenants/{tenant_id}/date-table/profiles/{profile_id}/materialize` |
| [Export date table](#export-date-table) | `GET /calendar/v1/tenants/{tenant_id}/date-table/profiles/{profile_id}/export?start=&end=&format=` |
| [List available date columns](#list-available-date-columns) | `GET /calendar/v1/date-table/columns` |

Admin writes
| Operation | Method and Path |
| --- | --- |
| [Create calendar definition](#create-calendar-definition) | `POST /calendar/v1/definitions` |
| [Create calendar event](#create-calendar-event) | `POST /calendar/v1/definitions/{calendar_id}/events` |
| [Create calendar set](#create-calendar-set) | `POST /calendar/v1/sets` |
| [Create fiscal calendar](#create-fiscal-calendar) | `POST /calendar/v1/fiscal` |
| [Put fiscal periods](#put-fiscal-periods) | `PUT /calendar/v1/fiscal/{fiscal_id}/periods` |

### List calendar definitions
`GET /calendar/v1/definitions`

Response 200
```json
{
  "items": [{"calendar_id":"...","name":"APAC Holidays","kind":"holiday","timezone":"Asia/Kolkata","active":true}],
  "etag":"W/\"defs-123\""
}
```

### List calendar events
`GET /calendar/v1/definitions/{calendar_id}/events?start=&end=`

Response 200
```json
{"items":[{"event_id":"...","starts_at":"2025-10-02T00:00:00Z","ends_at":"2025-10-02T23:59:59Z","label":"Gandhi Jayanti"}]}
```

### List calendar sets
`GET /calendar/v1/sets`

Response 200
```json
{"items":[{"set_id":"...","name":"APAC Biz Hours + Holidays"}]}
```

### Resolve calendar set
`GET /calendar/v1/sets/{set_id}/resolve?tenant_id=...&start=2025-10-01&end=2025-10-31&tz=Asia/Kolkata`

Response 200
```json
{"items":[{"starts_at":"2025-10-02T00:00:00Z","ends_at":"2025-10-02T23:59:59Z","label":"Gandhi Jayanti"}]}
```

### Get tenant overlay
`GET /calendar/v1/tenants/{tenant_id}/overlays`

Response 200
```json
{"overlay_id":"...","set_id":"...","add_events":[...],"suppress_event_ids":[...]}
```

### Put tenant overlay
`PUT /calendar/v1/tenants/{tenant_id}/overlays`

Request
```json
{"set_id":"...","add_events":[...],"suppress_event_ids":[...]}
```

Response 200
```json
{"overlay_id":"...","set_id":"...","updated_at":"2025-10-03T12:00:00Z"}
```

### List fiscal calendars
`GET /calendar/v1/fiscal`

Response 200
```json
{"items":[{"fiscal_id":"...","name":"Standard Fiscal Year","timezone":"UTC","start_month":4}]}
```

### List fiscal periods
`GET /calendar/v1/fiscal/{fiscal_id}/periods?year=2026`

Response 200
```json
{"items":[{"year":2026,"period":1,"starts_on":"2026-04-01","ends_on":"2026-04-30"}]}
```

### Next business day
`GET /calendar/v1/working-time/next-business-day?start=2025-10-01T10:00:00Z&set_id=...&tenant_id=...&tz=Asia/Kolkata`

Response 200
```json
{"next_business_day":"2025-10-03T00:00:00+05:30"}
```

### Add business days
`GET /calendar/v1/working-time/add-business-days?start=2025-10-01T10:00:00Z&days=3&set_id=...&tenant_id=...&tz=Asia/Kolkata`

Response 200
```json
{"result":"2025-10-06T10:00:00+05:30"}
```

### Business minutes between
`GET /calendar/v1/working-time/business-minutes-between?start=2025-10-01T10:00:00Z&end=2025-10-02T17:00:00Z&set_id=...&tenant_id=...&tz=Asia/Kolkata`

Response 200
```json
{"minutes": 420}
```

## Error model
```json
{"code":"invalid_request","message":"unknown set_id","correlation_id":"..."}
```

## Idempotency and caching
- Use `Idempotency-Key` for POST and PUT
- Return `ETag` on reads and accept `If-None-Match`


### Get tenant settings
`GET /calendar/v1/tenants/{tenant_id}/settings`

Response 200
```json
{
  "tenant_id":"...",
  "week_start":1,
  "weekend_days":["sat","sun"],
  "default_set_id":"...",
  "default_timezone":"Asia/Kolkata",
  "business_hours":{
    "mon":[["09:00","18:00"]],
    "tue":[["09:00","18:00"]],
    "wed":[["09:00","18:00"]],
    "thu":[["09:00","18:00"]],
    "fri":[["09:00","18:00"]]
  },
  "updated_at":"2025-10-03T12:00:00Z",
  "etag":"W/\"tenant-settings-123\""
}
```

### Put tenant settings
`PUT /calendar/v1/tenants/{tenant_id}/settings`

Request
```json
{
  "week_start":1,
  "weekend_days":["sat","sun"],
  "default_set_id":"...",
  "default_timezone":"Asia/Kolkata",
  "business_hours":{
    "mon":[["09:00","18:00"]],
    "tue":[["09:00","18:00"]]
  }
}
```

Response 200
```json
{"tenant_id":"...","updated_at":"2025-10-03T12:05:00Z"}
```

Notes
- `week_start` uses 1..7 with 1 = Monday
- `weekend_days` accepts values from ["mon","tue","wed","thu","fri","sat","sun"]
- `business_hours` times are local to `default_timezone` and expressed as HH:MM
- Idempotency supported via `Idempotency-Key`
- ETag returned for caching on GET

# Date Table endpoints

### List date table profiles
`GET /calendar/v1/tenants/{tenant_id}/date-table/profiles`

Response 200
```json
{"items":[{"profile_id":"...","name":"Default","week_start":1,"weekend_mask":96,"pattern":"standard","timezone":"Asia/Kolkata"}]}
```

### Create date table profile
`POST /calendar/v1/tenants/{tenant_id}/date-table/profiles`

Request
```json
{
  "name":"Default",
  "week_start":1,
  "weekend_mask":96,
  "pattern":"standard",
  "timezone":"Asia/Kolkata",
  "fiscal_id":"...",
  "columns":["date","date_key","year","month","month_name","day","iso_week","is_business_day","is_holiday","holiday_label"]
}
```

Response 201
```json
{"profile_id":"...","tenant_id":"...","name":"Default"}
```

### Update date table profile
`PUT /calendar/v1/tenants/{tenant_id}/date-table/profiles/{profile_id}`

Request
```json
{"timezone":"UTC","columns":["date","date_key","year"]}
```

Response 200
```json
{"profile_id":"...","updated_at":"2025-10-03T12:00:00Z"}
```

### Materialize date table
`POST /calendar/v1/tenants/{tenant_id}/date-table/profiles/{profile_id}/materialize?start=2025-01-01&end=2026-12-31&format=parquet`

Response 202
```json
{"materialization_id":"...","rows":731}
```

### Export date table
`GET /calendar/v1/tenants/{tenant_id}/date-table/profiles/{profile_id}/export?start=2025-01-01&end=2025-12-31&format=csv`

Response 200
CSV stream with Content-Disposition. For large ranges, return a 302 to a signed URL.

### List available date columns
`GET /calendar/v1/date-table/columns`

Response 200
```json
{"items":["date","date_key","year","quarter","quarter_name","month","month_name","month_name_short","day","day_of_week","day_name","iso_week","week_of_month","is_weekend","is_business_day","is_holiday","holiday_label","fiscal_year","fiscal_period","fiscal_quarter","business_day_index","eom","bom"]}
```
