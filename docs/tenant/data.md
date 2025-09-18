# Tenant App – Data Access and Reports

## Purpose
Data access and reports provide curated datasets and KPI views for tenant decision makers.  
The goal is to deliver trustworthy numbers that can be consumed directly by executives and business teams.

## Capabilities
- **Curated Datasets**
  - Exposed through the Tenant App for exploration and downloads.
  - Based on approved contracts in Schema Service.
  - Includes filters for company, business unit, or time period.

- **Reports**
  - Pre‑built KPI reports aligned with executive use cases.
  - Exportable in common formats (PDF, CSV, XLSX).
  - Printable layouts optimized for boardroom consumption.

- **Access Controls**
  - Permissions enforced at row and column level.
  - Column masking applied based on contract definitions.
  - BI connectors available with read‑only scoped credentials.

- **APIs and Tokens**
  - Scoped API tokens for integration with external tools.
  - Tokens inherit role‑based permissions.

## Roles Involved
- **Executives and Business Teams**
  - Consume curated reports and datasets.
  - Export and share reports for decision making.
- **Stewards**
  - Ensure data quality and contract alignment.
- **Admins**
  - Configure access levels and review permissions.

## Notes
- All report access is logged with correlation IDs.
- Freshness indicators are shown alongside every dataset.
- Exports are time‑bounded and delivered via signed URLs.
