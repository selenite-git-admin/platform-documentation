## Purpose
Describe how storage in Platform Host Services (PHS) is operated on a day-to-day basis.  
Focus areas include backup, retention, compliance, monitoring, and incident handling.

## Operational Model
- Storage operations apply only to metadata, contracts, lineage, and audit evidence.  
- Tenant business data is excluded from PHS scope.  
- Operations are designed to be automated, repeatable, and auditable.

## Backup and Recovery
- **Aurora metadata stores** are protected with daily snapshots and point-in-time recovery (7-day window).  
- **S3 audit evidence** buckets use versioning and object lock for compliance; lifecycle policies move objects to Glacier after retention thresholds.  
- **Cache (Redis/ElastiCache)** stores transient validation state and counters with TTL; not used for durability.  
- Cross-region recovery is optional and enabled only where residency policy allows.

## Retention and Legal Hold
- Audit logs are retained for a minimum of 365 days.  
- Evidence objects default to 7 years of retention.  
- Lineage metadata is retained until superseded contracts expire plus a configurable TTL.  
- Legal holds are supported through S3 object lock (governance mode).

## Capacity and Performance
- Aurora instances scale automatically; connection pooling is enforced.  
- Evidence objects are partitioned by tenant and contract identifiers to optimize query and retrieval.  
- Redis is monitored for eviction rates; TTL configured per workload.

## Security Operations
- All storage is encrypted with AWS KMS customer-managed keys.  
- Secrets are managed externally in AWS Secrets Manager; no secrets are persisted in PHS stores.  
- IAM access to PHS storage is scoped to the Platform Super Admin role; policies are reviewed periodically.  
- Outbound egress policies are modified only through CDK pipelines with approval.

## Monitoring and Alerts
- Dashboards track backup success, evidence ingestion latency, and retention compliance.  
- Alerts trigger on missed snapshots, PITR gaps, object lock violations, and cost threshold breaches.  
- Observability integrates metrics, logs, and traces into a central hub for analysis.

## Incident Handling
- Evidence corruption is remediated by restoring from snapshots and reconciling lineage with audit records.  
- Retention or residency misconfigurations are frozen via legal hold until corrected.  
- Regional impairments trigger cross-region recovery where configured; otherwise PHS operates in read-only mode until restored.

## End State
Storage operations in PHS are **automated, monitored, and auditable**.  
Procedures for backup, retention, compliance, and recovery ensure that metadata remains durable and compliant without impacting tenant workloads.