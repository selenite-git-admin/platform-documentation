# Schema Database

## Purpose
Provide guidance for physical schema storage and operations.
Keep DDL consistent with contracts.
Support performance, reliability, and cost control.

## Design Principles
Use clear naming conventions.
Keep keys explicit.
Index for common access paths.
Partition large tables by time or key.
Separate landing, Bronze, Silver, and Gold namespaces.

## Technology Selection
Use relational stores for contracts and small tables.
Use columnar stores for analytical tables.
Use object storage for landing files.
Select runners that match workload.

## Benchmarking and Performance
Define test datasets and workloads.
Measure latency, throughput, and cost.
Record results as evidence.

## Setup and Provisioning
Create schemas and roles with infrastructure as code.
Bind stores to the Host App for observability.
Prepare migration tools and secrets.

## Migrations
Use versioned migrations that match contract versions.
Apply additive changes first.
Provide rollback plans.
Protect hot paths with feature flags when needed.

## Operations and Scaling
Manage indexes and vacuum or compaction tasks.
Apply retention and archival policies.
Monitor freshness, completeness, cost, and error rate.
Test backup and restore.
Plan for high availability and disaster recovery.

## DDL Pattern
```sql
CREATE TABLE {schema}.{table} (
  /* columns from contract payload */
);
```
