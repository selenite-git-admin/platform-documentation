# Dataset Refresh Registry (DRR) Deployment

**Family:** Data Store **Tier:** Core **Owner:** Platform Foundation **Status:** Review  

## Purpose
This document defines how DRR is deployed, versioned, and scaled in production environments. Deployment is automated through Infrastructure-as-Code (IaC) templates and controlled by continuous delivery pipelines.

## Deployment Architecture
DRR is deployed as a regional microservice with stateless API pods and a replicated PostgreSQL backend.

```
┌──────────────────────────────────────────────────────┐
│                   AWS Region (Primary)               │
│  ┌───────────────┐       ┌────────────────────────┐  │
│  │ DRR API Pods  │◄────►│ AWS RDS (PostgreSQL)   │  │
│  └───────────────┘       └────────────────────────┘  │
│       ▲       │                ▲                     │
│       │       ▼                │                     │
│   Load Balancer      Evidence Ledger / Runtime        │
│                                                  │    │
└──────────────────────────────────────────────────────┘
```

### Core Components
| Component | Description |
|------------|-------------|
| DRR API | Exposes REST endpoints for reads and internal writes |
| DRR Writer | Consumes Runtime completion events and updates state |
| PostgreSQL | Stores dataset metadata and freshness state |
| S3 (optional) | Stores audit exports and long-term run logs |
| CloudWatch / Prometheus | Observability and metrics backend |
| Secrets Manager | Stores DB credentials, tokens, and certificates |

## Deployment Environments
| Environment | Purpose | Key Settings |
|--------------|----------|---------------|
| dev | Developer testing | Single pod, ephemeral DB |
| staging | Pre-production verification | Full topology, synthetic Runtime feed |
| prod | Production deployment | HA mode, 2+ AZs, RPO < 5 min |

Each environment has isolated VPC, secrets, and RDS clusters.

## Infrastructure Definition
- IaC defined in Terraform under `infra/modules/drr/`.
- Versioned artifacts stored in ECR as Docker images.
- Deployments orchestrated through ArgoCD (GitOps).

### Terraform Key Resources
| Resource | Description |
|-----------|-------------|
| aws_ecs_service.drr_api | API containers |
| aws_rds_cluster.drr | PostgreSQL cluster |
| aws_lb_target_group.drr | ALB target group |
| aws_security_group.drr | Ingress/egress rules |
| aws_secretsmanager_secret.drr | Encrypted DB credentials |
| aws_sqs_queue.runtime_events | Runtime → DRR event bridge |

## Deployment Workflow
1. **Build:**  
   Docker image built via CI pipeline (`buildspec.yml`), tagged as `drr:<git-sha>` and pushed to ECR.
2. **Test:**  
   Integration tests execute against staging database; smoke tests validate API health endpoints.
3. **Deploy:**  
   ArgoCD detects image tag change and applies manifests to cluster via Helm chart.
4. **Verify:**  
   Health probes must pass within 5 minutes; observability checks confirm metrics emission.
5. **Promote:**  
   After manual approval, staging image promoted to production.

### Helm Chart Structure
```
charts/drr/
  ├── templates/
  │   ├── deployment.yaml
  │   ├── service.yaml
  │   ├── hpa.yaml
  │   └── configmap.yaml
  ├── values.yaml
  └── Chart.yaml
```

Key parameters:
- replicaCount: default 3  
- autoscaling.enabled: true  
- resources.requests.cpu: 250m  
- resources.limits.cpu: 1  

## Scaling and Availability
- Horizontal scaling via HPA on CPU and RPS metrics.
- PostgreSQL uses multi-AZ Aurora cluster with read replicas.
- Read traffic directed to nearest replica; writes pinned to primary.
- DRR API stateless — scaling does not affect data consistency.

**SLAs**
| Metric | Target |
|---------|---------|
| Read availability | 99.99% |
| Write propagation | ≤ 10 s |
| Cold start | < 60 s |

## Deployment Verification
- `/health` returns 200 when API and DB reachable.
- `/metrics` exposes Prometheus counters and gauges.
- Synthetic probe runs hourly to confirm data freshness propagation.

**Example Probe Output**
```json
{
  "dataset_id": "sales.pipeline_summary",
  "status": "fresh",
  "lag_sec": 380,
  "checked_at": "2025-10-12T07:55:00Z"
}
```

## Configuration Parameters
| Variable | Description | Default |
|-----------|--------------|----------|
| DB_MAX_CONN | Maximum DB connections per pod | 50 |
| CACHE_TTL_SEC | Cache validity | 30 |
| PROPAGATION_SLO_SEC | Expected propagation window | 10 |
| MAX_RETRY | Retry attempts on transient errors | 3 |
| RUNTIME_EVENT_QUEUE | Queue name for completion events | runtime-events |

## Rollback Strategy
- Each deployment revision stored in ArgoCD history.
- Rollback uses previous image tag via `argocd app rollback drr`.
- Database changes versioned using Liquibase migrations.
- If schema migration fails, revert via `liquibase rollbackCount 1`.

## Backup and Recovery
| Type | Frequency | Retention | Location |
|------|------------|------------|----------|
| RDS snapshot | Hourly | 7 days | AWS RDS |
| WAL archive | Continuous | 14 days | S3 |
| Config backup | Daily | 30 days | S3 |

Disaster recovery tested quarterly using regional failover simulation.

## Regional Replication
- Active-active topology with write quorum restricted to primary.
- DRR replicas read-only in secondary regions.
- Lag monitored via `pg_replication_lag_seconds`.
- Event bus mirrored across regions via SQS Cross-Region Replication.

## Security Controls in Deployment
- TLS termination at ALB with ACM-issued certificates.
- API pods run as non-root, read-only filesystem.
- Secrets mounted at runtime from AWS Secrets Manager.
- IAM role per service with least privilege policies.

## Blue-Green Deployment Option
When enabled:
- Blue and Green environments run in parallel.
- Ingress traffic gradually shifted via weighted ALB rules.
- Automated rollback if error rate > 1% or latency > 200 ms for 5 minutes.

## Post-Deployment Verification Checklist
- [x] API `/health` endpoint returns OK
- [x] Writer consumes events from Runtime queue
- [x] Metrics visible in Grafana within 2 minutes
- [x] RLS policy verified by sample tenant read
- [x] Evidence Ledger receives audit trail

## Ownership
| Role | Responsibility |
|------|----------------|
| Platform Foundation | Deployment automation, Helm chart maintenance |
| DevOps | CI/CD, environment provisioning |
| Data Platform SRE | Monitoring, incident response, scaling |

## Summary
DRR deployment is fully automated, secure, and auditable. It supports multi-region resilience, rolling upgrades, and deterministic rollback. Every release follows the same declarative pipeline from build to verification, ensuring reproducibility across all environments.