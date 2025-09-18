# PHS — Security & NFRs

## Purpose
Define the security model, reliability targets, and operational guardrails for Platform Host Services (PHS).  
This section sets the expectations for how PHS is accessed, how it behaves under stress, and how it supports compliance and audit needs.

---

## Security Posture

### Access Control
- Only the **Platform Super Admin** has direct access to PHS.
- Access is via **AWS CLI/CDK/CICD pipelines only**. No UI or console access.
- Super Admin role is narrow but high-power: contract enforcement, versioning, and configuration of shared services.
- MFA is mandatory; IAM policies follow **least privilege** principles.

### Network & Connectivity
- All PHS services deployed in private subnets.
- Ingress/Egress traffic flows through controlled gateways with policy enforcement.
- Outbound connectivity follows **deny-by-default**; explicit allowlists defined in CDK.
- PrivateLink and VPC endpoints used for AWS services and partner systems.

### Data & Secrets
- PHS stores **metadata only** (contracts, lineage, audit, policy).  
  No tenant business data is ever persisted.
- Secrets stored in AWS Secrets Manager; keys managed by KMS with automatic rotation.
- All service-to-service communication is TLS encrypted; optional mTLS for connectors.

### Audit & Compliance
- Every control-plane action emits immutable audit events with contract/version IDs.
- CloudTrail and GuardDuty monitor all Super Admin and CICD actions.
- Audit retention aligned with compliance policies; exportable to external evidence systems.

---

## Non-Functional Requirements (NFRs)

### Reliability & Availability
- Enforcement APIs: **99.95% availability** per region.
- Ingress validation: < **200 ms p95 latency** for schema checks on typical payloads.
- KPI build checks: < **1 s p95 latency** for contract validation per metric definition.
- Multi-AZ deployment in each active AWS region.

### Scalability
- Contracts: support thousands of active Raw/GDP/KPI contracts per platform.
- Tenancy: support hundreds of tenants with isolated enforcement paths.
- Throughput: ingress validation scalable to millions of records/hour.
- Horizontal scaling of validation engines and observability pipeline.

### Performance
- Quarantine handling capacity for up to 10% of daily ingress volume without data loss.
- Audit/event pipeline capable of sustaining 10k+ events/minute.
- Alerting latency < 60 seconds for contract or policy breaches.

### Observability & Operations
- Metrics: contract validation success rate, latency, quarantine rate, egress policy blocks.
- Dashboards: SLO compliance, connector health, tenant quota usage.
- Alerts: triggered on SLO violation, policy drift, or quota exhaustion.
- Logs: centralized, structured, and retained for 365 days minimum.

### Compliance
- Residency: enforced at contract level; no cross-region spillover without explicit policy.
- Retention: metadata purged according to retention rules; legal holds supported.
- Security reviews: IAM policies and CDK stacks audited quarterly.

### Disaster Recovery & BCP
- Backup: daily snapshots of metadata stores; 7-day PITR.
- DR: cross-region backup with RPO = 1 hour, RTO = 4 hours.
- Business continuity: contract enforcement can continue with read-only PHS in degraded mode.

---

## End State
PHS operates under a **secure, controlled, and highly available** model.  
Access is tightly scoped to the Super Admin via automation; enforcement APIs meet strict SLOs; and compliance requirements (residency, retention, audit) are built in.  
This ensures PHS remains a **durable control plane** independent of tenant workloads or Admin App availability.
