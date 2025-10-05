# Lifecycle: Taxonomy & Naming

## Subject Naming
```
raw:<source>.<stream>
gdp:<entity>
kpi:<measure>
ref:<name>
meta:<name>
```
- `<source>`: system id (`sap`, `sf`, `db2`), lowercase a‑z0‑9, `-` allowed.
- `<stream>`: table or feed name, dot‑separated for logical nesting.
- `<entity>`: business entity (`order`, `customer_account`).
- `<measure>`: concise KPI name (`gm_percent`, `nps`, `churn_rate`).

## Versioning Keys
- Each **subject** has a **monotonic integer** `version` series.
- Canonical key: `subject@v<nn>`; example: `gdp:order@v24`.

## Metadata
All subjects carry:
- `owner` (team slug), `domain` (bounded context), `tags[]`
- `description` (markdown), `pii_flags[]` (field-level)
- `lineage` links: upstream/raw subjects; downstream datasets/KPIs
- `contracts[]` (policy ids in Governance)
