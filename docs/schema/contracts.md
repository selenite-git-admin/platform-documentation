# Schema Services — Contracts & Versioning

## Purpose
Define how schema contracts (Raw, GDP, KPI) are identified, versioned, and governed across their lifecycle.  
This section formalizes contract structure, compatibility rules, lifecycle states, and eventing.

---

## Contract Types
- **Raw Contract**: Declares source schemas, keys, partitions, calendars, validation rules, and SLAs for ingress.
- **GDP Contract**: Declares canonical entities, reference bindings (FX, UoM, calendar, org), and conformance rules.
- **KPI Contract**: Declares metric formulas, inputs (GDP entities/versions), aggregation grain, filters, thresholds, and delivery SLAs.

> Contracts are **metadata only**; platform does not persist tenant business data.

---

## Identity & Addressing
Each contract is addressed by an immutable tuple:
```
<contract_type>/<tenant_id>/<contract_id>/<major>.<minor>.<update>
```
- `contract_type ∈ {raw,gdp,kpi}`
- `contract_id`: UUID
- Version triplet uses **Major–Minor–Update** semantics (see below).

A canonical **Contract Header** accompanies every contract:
```yaml
contract:
  type: raw | gdp | kpi
  tenant_id: 00000000-0000-0000-0000-000000000000
  contract_id: 11111111-1111-1111-1111-111111111111
  version: 2.3.4        # major.minor.update
  title: "Sales Orders (SAP)"
  description: "Inbound sales order lines from SAP SD"
  residency: "ap-south-1"
  created_at: "2025-09-15T12:00:00Z"
  supersedes: "2.3.3"   # last version in lineage (optional for Major)
  effective_from: "2025-10-01"
  tags: ["sales", "orders", "erp:sap"]
```

---

## Versioning Semantics
- **Major** — Breaking change. Requires explicit migration steps and downstream re-alignment. Examples:
  - Renaming/removing fields used by downstream.
  - Changing primary/business keys or grain.
- **Minor** — Backward-compatible extension. Examples:
  - Adding optional fields.
  - Adding new reference mappings that do not alter existing semantics.
- **Update** — Non-structural changes. Examples:
  - Threshold tweaks, descriptions, display names, non-functional metadata.

**Rules**
- Major increments reset Minor/Update to `0`.
- Minor increments reset Update to `0`.
- Update increments do not change Major/Minor.
- Published versions are **immutable**; corrections require a new Update or Minor/Major as appropriate.

---

## Lifecycle States
Lifecycle is managed in **PHA (Admin App)**; **PHS** stores and enforces only **active** versions.

| State       | Description                                     | Who can move it | Notes |
|-------------|--------------------------------------------------|------------------|-------|
| `draft`     | Created, editable                                | PHA roles        | Not visible to PHS |
| `in_review` | Under review/validation                          | PHA reviewers    | Automated checks run |
| `approved`  | Approved for publish                             | Approvers        | Awaiting publish window |
| `published` | Persisted to PHS, not yet active (staged)        | PHA              | Idempotent publish |
| `active`    | Enforced by PHS                                  | PHA or schedule  | Single active per type+id per tenant |
| `superseded`| Retained for history within grace TTL            | System           | Read-only |
| `retired`   | Hidden from standard listings                    | System           | Access via audit only |

**Activation model**
- One **active** version per (`contract_type`, `tenant_id`, `contract_id`).  
- Activation can be immediate or scheduled (`effective_from`).  
- Superseding creates lineage via `supersedes` pointers.

---

## Compatibility Rules
- **Raw → GDP**: GDP contracts must remain compatible with referenced Raw fields for Minor/Update releases.
- **GDP → KPI**: KPI contracts must reference GDP entities by `(contract_id, version)`; Major GDP changes require KPI review.
- **Semantic locks**:
  - Primary/business keys: **Major** if changed.
  - Aggregation grain (KPI): **Major** if changed.
  - Unit/currency defaults: **Minor** if additive; **Major** if defaults reversed.

---

## Validation Gates (automated)
- **Schema linting**: field types, required/optional, enums.
- **Key integrity**: primary/business keys present and unique (Raw), foreign keys valid (GDP).
- **Reference bindings**: FX/UoM/calendars/hierarchies exist and are in-validity window.
- **KPI formula check**: inputs exist, grain and filters consistent; thresholds well-formed.
- **Residency/retention**: conform to contract header and policy.
- **Change impact**: Major/Minor/Update classification verified by diff engine.

Failures block transition to `approved` or `published` until resolved.

---

## Eventing (illustrative)
- `contract.draft.created` (PHA)  
- `contract.review.requested` (PHA)  
- `contract.published` (PHA → PHS)  
- `contract.activated` (PHS)  
- `contract.superseded` (PHS)  
All events carry `contract_type`, `tenant_id`, `contract_id`, `version`, and `evidence_id`.

---

## Examples

### Raw Contract (excerpt)
```yaml
schema:
  source_system: "sap_sd"
  tables:
    - name: "vbak"
      keys: ["vbeln"]
      fields:
        - { name: "vbeln", type: "string", required: true }
        - { name: "erdat", type: "date", required: true }
        - { name: "waerk", type: "string", required: true, enum: ["USD","EUR","INR"] }
  partitions:
    calendar: "gdp_calendar"
    period_grain: "day"
validation:
  freshness_days: 2
  min_daily_rows: 1000
```

### GDP Contract (excerpt)
```yaml
entities:
  calendar:
    table: "gdp_calendar"
    keys: ["date_key"]
  currency:
    table: "gdp_currency"
    keys: ["currency_code","valid_from"]
  org:
    table: "gdp_org"
    keys: ["org_unit_id"]
conformance:
  mappings:
    - raw: "sap_sd.vbak.waerk"
      gdp: "gdp_currency.currency_code"
    - raw: "sap_sd.vbak.erdat"
      gdp: "gdp_calendar.date_key"
```

### KPI Contract (excerpt)
```yaml
kpi:
  id: "net_sales_usd"
  title: "Net Sales (USD)"
  inputs:
    - entity: "sales_order_line"
      version: "1.4.0"
  formula: "(sum(net_amount_local * fx_rate_to_usd))"
  grain: ["fiscal_year","fiscal_period","org_unit_id"]
  thresholds:
    - { level: "warn", op: "<", value: 0 }
    - { level: "crit", op: "<", value: -10000 }
delivery:
  sla_minutes: 30
```

---

## Changelog & Deprecation
- Each contract update must include a human-readable changelog entry.
- Deprecation windows are declared for Major bumps; KPIs depending on deprecated GDP/Raw versions are flagged.
- Sunset schedules are communicated via events and API.

---

## Governance
- All changes originate in Git; PHA manages reviews and approvals.
- PHS accepts only **published** artifacts; runtime is read-only.
- Every decision is linked to audit evidence and lineage entries.

---

## End State
Contracts provide a **stable, versioned interface** between ingestion, canonicalization, and metrics.  
The lifecycle separates **governance** (PHA) from **enforcement** (PHS), ensuring safe evolution without breaking downstream consumers.
