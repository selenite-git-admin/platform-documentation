# Catalog Module (Metadata & Discovery)

## Purpose
Unified metadata service for **datasets, KPIs, dashboards, and versions**. Powers discovery UX, ownership, freshness, quality signals, and links across the platform.

## What it owns
- **Items**: dataset/kpi/dashboard with stable slugs.
- **Signals**: freshness, quality score, usage.
- **Ownership & tags**: team-level ownership, domain tags.
- **Cross-links**: to Storage snapshots, Delivery endpoints, and Actions.

## Non‑goals
- Serving the data itself (Delivery/Storage own).
- Authoring schemas (Schema Module owns).

## Interfaces
- REST `/api/v1/catalog/...`
- Search DSL: `name:orders fresh:<24h tag:finance`.
- UI: powerful filters, lineage hops.
