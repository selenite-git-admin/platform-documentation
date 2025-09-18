# PHS — Costs & Budget

## Purpose
Outline how costs for Platform Host Services (PHS) are estimated, attributed, and monitored.  
The goal is to keep the control plane predictable and cost-efficient, while enabling scale with tenants and contracts.

---

## Cost Principles
- **Control plane focus**: PHS costs are limited to metadata storage, enforcement checks, and shared services.  
  No tenant business data is stored here.
- **Transparency**: All cost drivers linked to specific AWS services and mapped back to platform modules.
- **Budget enforcement**: Alerts and caps defined in CDK; no silent overruns.
- **Attribution**: Costs split into platform baseline vs. tenant-driven usage.

---

## Major Cost Drivers

### Infrastructure Baseline
- **VPC, NAT gateways, endpoints**: networking cost per region.
- **Aurora PostgreSQL (metadata)**: storage + provisioned/auto-scaling compute.
- **S3 (audit/evidence)**: per GB stored + requests; lifecycle rules manage retention.
- **Secrets Manager / KMS**: per secret stored and per request; key rotations.
- **Observability stack**: CloudWatch/X-Ray/metrics logs; ingestion + dashboards.

### Variable Costs
- **Kinesis/MSK streams**: per shard/hour + data volume for enforcement events.
- **Lambda / Fargate jobs**: per execution; contract validations, orchestration tasks.
- **Quarantine storage**: short-term S3 or queue storage if high rejection rate.
- **Outbound egress**: traffic via NAT/proxies for connectors; billed per GB.

---

## Budgeting Model
- **Baseline budget**: fixed monthly allocation for always-on PHS components (Aurora, NAT, Secrets, Observability).
- **Variable budget**: flexible pool for contract validations, events, and egress.  
  Driven by number of tenants, contracts, and connector activity.
- **Tenant attribution**: where feasible, connector egress and KPI delivery costs linked to tenant tags.

---

## Monitoring & Controls
- **Budgets**: AWS Budgets created per cost category (infra, observability, egress).
- **Alerts**: 70/90/100% thresholds trigger notifications to Super Admin.
- **Guardrails**:
  - CICD pipelines fail if change increases baseline cost beyond approved cap.
  - Outbound connectors throttled if tenant-level budget is breached.
- **Reporting**: monthly cost reports grouped by module (contracts, observability, egress).

---

## Optimization Levers
- Enable Aurora auto-pause for idle dev/test environments.
- Apply S3 lifecycle rules (move evidence to Glacier after 1 year).
- Right-size stream shards; move to on-demand if workloads are spiky.
- Reuse PrivateLink/VPC endpoints where possible to cut NAT costs.
- Tune observability retention (keep high-res for 30 days, roll off to summaries after).

---

## End State
PHS costs remain **predictable and bounded**.  
The baseline infra is steady, while variable costs scale with tenants and contract activity.  
Budgets, alerts, and cost attribution provide early signals and enforce financial discipline without impacting enforcement reliability.
