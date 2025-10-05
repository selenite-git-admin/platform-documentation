# Storage Domain

## Role in the Platform
The Storage domain receives raw feeds, transforms them into a governed data product (GDP), calculates KPIs, and serves published datasets to downstream apps. It also exposes a calendar of GDP refreshes for predictability and SLAs.

## Submodules
- [Raw Store](raw-store/index.md) — durable landing zone for raw, immutable feeds.  
- [GDP Store](gdp-store/index.md) — governed, versioned data product with lineage.  
- [KPI Store](kpi-store/index.md) — curated KPIs with dimensional lookups.  
- [Published Store](published-store/index.md) — tenant-ready, de-duplicated, and contract-stable exports.  
- [GDP Calendar](gdp-calendar/index.md) — schedules and status for GDP refreshes.

## Position in the Platform
Ingests from external connectors and runtime jobs, emits datasets for Consumption, and feeds Runtime metrics. Trust provides encryption and key management; Security controls access.

## Interfaces
- Ingest APIs and batch loaders for raw feeds.  
- Transformation jobs and lineage records for GDP.  
- Query and export endpoints for KPI and Published stores.  
- Calendar API for refresh windows and SLAs.

## Constraints
- Storage does not author KPIs or rules; it persists and serves.  
- Schema changes are versioned and require migrations.
