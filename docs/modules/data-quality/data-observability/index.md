# Data Observability Service

## Purpose
Data Observability Service provides a stable, governed capability used by pipelines and modules. It exposes APIs, enforces contracts, emits evidence, and ships with SLO-backed operations.

## Scope
- Owns interfaces and metadata related to its domain.
- Integrates with Access, Governance, Storage, Runtime, and Delivery.
- Emits observability signals and receipts for regulated actions.

## Responsibilities
- Contract-first APIs with additive evolution.
- Tenant isolation and ABAC/RBAC enforcement.
- Evidence and lineage integration.
- Clear runbooks and rollback procedures.

## Non‑Goals
- Does not bypass governance or duplicate pipeline logic.
- Does not provide arbitrary compute orchestration.

## Interfaces
- REST: `/api/v1/data-observability/...`
- Events: HMAC-signed webhooks (optional mTLS)
- UI: Admin-facing screens for operators

## SLOs
- Availability ≥ 99.9% (30‑day rollup)
- P95 latency documented per endpoint
- 100% of writes produce evidence receipts

## Cross‑Module Contracts
- **Access** for authn/z and scoping.
- **Governance** for policies/contracts.
- **Storage** for durable artifacts where relevant.
- **Runtime** for background jobs and retries.
- **Delivery** for downstream discovery and access.

    ### What it manages
    - Cross-pipeline signals: freshness, volume, schema drift, null rates, outliers.
    - SLOs and alerting rules; exports signals to Runtime/Delivery UIs.
