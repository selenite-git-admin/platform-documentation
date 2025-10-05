# Date Table

## Scope
Provide a tenant aware Date Table similar to PBIX Date Table, with advanced options driven by Calendar Service. The Date Table is generated from platform calendars, tenant overlays, and optional fiscal calendars. It is primarily used by BI tools and downstream analytics to standardize time intelligence.

## Concepts
Profile
A saved configuration for a tenant that defines range, calendars, fiscal mapping, week start, weekends, and which columns to generate.

Materialization
A point in time export of a profile for a specific date range, optionally persisted for reuse.

Columns catalog
A fixed set of column keys that can be toggled on a profile. Values are computed from the effective calendar and timezone.

## Columns catalog
Each column is identified by a key. Enable the keys you need.

- date
  ISO date. Primary key.
- date_key
  Integer in yyyymmdd for surrogate keys.
- year
  Calendar year number.
- quarter
  Calendar quarter number 1..4.
- quarter_name
  Q1..Q4.
- month
  Calendar month number 1..12.
- month_name
  Full month name in locale.
- month_name_short
  Short month name in locale.
- day
  Day number 1..31.
- day_of_week
  ISO day of week 1..7 respecting week_start setting.
- day_name
  Day name in locale.
- iso_week
  ISO 8601 week number.
- week_of_month
  Week number within the month based on week_start.
- is_weekend
  Boolean from weekend mask.
- is_business_day
  Boolean computed as not weekend and not a holiday.
- is_holiday
  Boolean when an effective holiday occurs.
- holiday_label
  Holiday label when is_holiday.
- fiscal_year
  From selected fiscal calendar when present, else null.
- fiscal_period
  Period index from fiscal calendar (e.g., 1..12 or 1..13).
- fiscal_quarter
  Quarter index derived from fiscal periods.
- business_day_index
  Running index of business days in the year.
- eom
  End of month date.
- bom
  Beginning of month date.

## Advanced options
- Range
  start_date and end_date inclusive.
- Week start and weekend
  Inherit from tenant settings unless overridden on the profile.
- Fiscal calendar
  Optional link to a fiscal calendar for fiscal_* columns.
- Pattern
  Standard, 445, 454, 544 period patterns for fiscal mapping.
- Timezone
  Default timezone for name formatting and business hours.
- Holidays
  Derived from effective calendar set and tenant overlays.
- Locale
  Optional locale for names. Default to en.

## API integration
- Create or update a Date Table **profile**.
- Materialize a profile to produce CSV or Parquet for a requested range.
- Stream rows for a range without materializing when needed.
- Discover allowed column keys and defaults.

See endpoints in [API](api.md#date-table-endpoints).

## UI
Tenant App
- Date Table Profiles: create, edit, preview first 50 rows.
- Column picker: toggle keys; defaults align to common PBIX Date Table.
- Materialize and export: CSV or Parquet. Show download link.

## Performance notes
- Generate on the fly for ranges up to one year.
- For multi year exports, materialize once and cache by profile and range.
- Use calendar resolution caches to avoid recomputing holidays and business days.

## Security
- No PII. All fields are derived from dates and metadata.
- Exports follow platform retention policy.
