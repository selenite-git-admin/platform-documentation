# Runtime Domain

## Role in the Platform
The Runtime domain executes data and control flows reliably and at scale. It schedules work, runs compute in isolated sandboxes, moves events through the streaming bus, and aggregates usage for enforcement and billing.

## Submodules
- [Orchestrator](orchestrator/index.md) — schedules DAGs, retries, SLAs, and backfills.  
- [Compute Fabric](compute-fabric/index.md) — multi-tenant execution of containers/functions with quotas.  
- [Streaming Bus](streaming-bus/index.md) — event backbone with topics, partitions, and DLQs.  
- [Metering](metering/index.md) — aggregates usage deltas into windowed counters.  
- [Config & Flags](config-flags/index.md) — runtime configuration, feature flags, gradual rollouts.

## Position in the Platform
Upstream of Storage transforms and downstream of Access decisions. Feeds Metering counters to Access→Subscription Enforcement and Trust→Evidence Ledger. Serves Action domain through rule triggers and outcomes.

## Interfaces
- Tenant/admin APIs for job submission, status, and flags.  
- Internal gRPC/HTTP for scheduling, execution, and metering ingestion.  
- Stream topics for events and DLQs.

## Constraints
- Runtime does not author business logic; it executes it.  
- Strong isolation and idempotency are required to protect tenants.
