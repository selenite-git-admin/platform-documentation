# Lifecycle: Versioning & Evolution

## Compatibility Modes
- **additive (default):** add optional fields, widen types, add enum values.
- **backward:** strong form; consumers reading older versions must not break.
- **breaking:** not permitted on existing subject; create a **new subject** and migrate.

## Field Operations Matrix
| Operation | Raw | GDP | KPI | Notes |
|---|---|---|---|---|
| Add optional field | ✅ additive | ✅ additive | ✅ additive | safe default/null |
| Add required field | ⚠️ config‑blocked | ❌ breaking | ❌ breaking | use default or phase‑in |
| Rename (with alias) | ✅ via alias | ✅ via alias | ✅ via alias | keep alias ≥ 180 days |
| Type widen int→number | ✅ | ✅ | ✅ | |
| Type narrow number→int | ❌ breaking | ❌ breaking | ❌ breaking | |
| Remove field | ❌ breaking | ❌ breaking | ❌ breaking | deprecate → sunset → remove |
| Enum add value | ✅ | ✅ | ✅ | |
| Enum remove value | ❌ breaking | ❌ breaking | ❌ breaking | |

## Deprecation Lifecycle
**Propose → Approve → Announce → Sunset → Remove**  
Defaults:
- Raw: 90 days (tenant override allowed)
- GDP/KPI: 180 days (minimum)  
Sunset emits Catalog notices + Delivery `Sunset` headers with date.

## Subject Branching (Major Changes)
Incompatible proposals require a **new subject** (e.g., `gdp:order.v2`) with:
- Parallel publish window ≥ 90 days (KPIs: ≥ 2 full cycles)
- Migration plan & receipts (see Migration Service)
