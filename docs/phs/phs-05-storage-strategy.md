## Purpose
Define how Platform Host Services (PHS) manages storage for contracts, metadata, lineage, and audit.  
PHS does **not** store customer business data. Its storage layer is limited to metadata and evidence needed for contract enforcement, compliance, and observability.

## Storage Principles
- **Metadata only**: schemas, contracts, lineage, audit, evidence, configuration, and policy state.
- **Tenant data exclusion**: raw, GDP, and KPI business data reside in tenant-controlled domains or storage.
- **Immutable evidence**: all enforcement decisions recorded with pointers to contract/version IDs.
- **Policy-driven**: residency, retention, and legal holds enforced via configuration and contract metadata.
- **Service separation**: different storage backends for different classes of metadata (relational, object, cache).

## Storage Classes

### Relational Stores
- Used for: active contracts, version metadata, lineage records, policy state.
- Backed by Aurora PostgreSQL Serverless v2.
- Features:
  - Multi-AZ replication, PITR enabled.
  - Versioned schema migrations controlled via CDK.
  - Row-level tenancy enforcement for metadata isolation.

### Object Storage
- Used for: audit evidence (JSON/Parquet), logs, artifacts linked to contract enforcement.
- Backed by Amazon S3 with bucket policies scoped to Super Admin role.
- Features:
  - Versioning enabled for all audit objects.
  - Lifecycle rules applied (default 365-day retention, configurable).
  - Object lock for compliance/legal hold scenarios.

### Caching & State
- Used for: transient validation state, throttling counters, rate-limits.
- Backed by Amazon ElastiCache (Redis).
- Features:
  - TTL-driven eviction (seconds to hours).
  - Not used for durable storage.

## Residency & Retention
- Residency policy defined per contract (region binding).
- PHS metadata pinned to region of deployment; no cross-region replication without explicit residency approval.
- Retention policies:
  - Audit logs: 365 days minimum.
  - Evidence objects: 7 years or as per compliance config.
  - Lineage metadata: persisted until contract superseded + grace TTL.

## Data Protection
- Encryption: all storage encrypted with AWS KMS CMKs (customer managed).
- Secrets: never persisted in PHS stores; only referenced from Secrets Manager.
- Backup: daily snapshots for relational metadata stores; S3 versioning for objects.
- Restore: tested quarterly with PITR for Aurora and compliance restores for S3.

## End State
PHS storage remains **narrow, metadata-focused, and policy-driven**.  
It provides durability for contracts, lineage, and audit evidence without hosting business data.  
Tenant workloads stay isolated; PHS enforces governance through metadata only.