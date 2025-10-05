# Migration Service

## Purpose
Migration Service provides a stable, governed capability used by pipelines and modules. It exposes APIs, enforces contracts, emits evidence, and ships with SLO-backed operations.

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
- REST: `/api/v1/migration-service/...`
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
    - Safe migrations: dataset re-partitioning, schema evolution with backfills, KPI re-compute.
    - Plans, dry-run, checkpoints, pause/resume, rollback.
