# Data Store Catalog (Catalog) Deployment

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
This document describes how the Catalog service is deployed with AWS CloudFormation, Amazon API Gateway, and AWS Lambda. The data plane remains PostgreSQL. The design favors zero engineering operations, safe rollout, and fast rollback.

## Deployment Architecture
Catalog exposes read APIs through API Gateway. Business logic runs in Lambda functions behind a Lambda alias for safe deployments. Catalog persists metadata in an RDS for PostgreSQL cluster. Writes are restricted to owner and platform roles.

```
Client
  |
API Gateway (REST)
  |
Lambda Alias -> Lambda Versions (Blue/Green)
  |
VPC ENI
  |
Amazon RDS for PostgreSQL (Multi-AZ)
  |
Evidence Ledger sink (async)
```

### Components
| Component | Purpose |
|----------|---------|
| API Gateway | Public entry point with auth, throttling, and caching |
| Lambda functions | Stateless handlers for read and internal write endpoints |
| Lambda alias | Routes traffic to a specific version with linear or blue/green rollout |
| RDS for PostgreSQL | Catalog persistence with read replicas for regional scale |
| Secrets Manager | Stores DB credentials and JWT verification keys |
| CloudWatch Logs and Metrics | Observability for APIs and Lambdas |
| EventBridge | Ships audit events to Evidence Ledger asynchronously |

## Environments
| Env | Purpose | Key Settings |
|-----|---------|--------------|
| dev | Developer validation | 1 RDS instance, Lambda on-demand, no API cache |
| staging | Pre-production | Multi-AZ RDS, provisioned concurrency 5, API cache enabled |
| prod | Production | Multi-AZ RDS, provisioned concurrency 20, API cache 1 GB |

Each environment is isolated by account and VPC.

## CloudFormation Stacks
Stacks are versioned and promoted through accounts with change sets.

| Stack | Resources |
|-------|-----------|
| catalog-network | VPC, subnets, security groups, VPC endpoints |
| catalog-storage | RDS for PostgreSQL, parameter groups, subnet groups |
| catalog-secrets | Secrets Manager entries and rotation Lambdas |
| catalog-service | API Gateway, Lambda functions, IAM roles, EventBridge rules |
| catalog-observability | CloudWatch dashboards, alarms, log groups |

### Parameters
| Name | Description | Example |
|------|-------------|---------|
| VpcId | Target VPC id | vpc-abc123 |
| SubnetIds | Private subnets for Lambdas and RDS | subnet-1,subnet-2 |
| DBInstanceClass | RDS instance class | db.r6g.large |
| DBAllocatedStorage | Storage in GB | 200 |
| ApiThrottlingBurst | API burst limit | 500 |
| ApiThrottlingRate | API steady rate | 2000 |
| LambdaProvisionedConcurrency | Provisioned concurrency per region | 20 |
| ApiCacheSize | API Gateway cache size | 1.6GB |

## Build and Release
1. Build Lambda artifact as a zip with `pip install -t ./package` and layer separation for DB drivers.
2. Upload artifact to S3 with a content hash in the key.
3. Create a new Lambda version from the uploaded artifact.
4. Update the Lambda alias to point to the new version using a weighted rollout.
5. Apply API Gateway stage variables for feature flags and DRR integration toggle.
6. Deploy CloudFormation change set to the environment.

CI pipeline stages
- Validate templates with `cfn-lint` and `aws cloudformation validate-template`.
- Run unit tests and contract tests against local Postgres in CI.
- Run integration tests in staging with seeded data.
- Require manual approval before prod alias shift.

## API Gateway Configuration
- REST API with regional endpoint.
- JWT authorizer validates platform tokens.
- Throttling defaults to 2000 RPS and 500 burst, configurable per route.
- Caching enabled for GET endpoints with ETag awareness.
- Access logs in JSON with request id and tenant id.

## Lambda Configuration
| Setting | Value |
|---------|-------|
| Memory | 512 MB default, 1024 MB for list endpoints |
| Timeout | 10 s default, 20 s for heavy reads |
| Runtime | Python 3.x |
| VPC | Enabled with 2 subnets and DB security group |
| Provisioned Concurrency | 5 to 20 based on env |
| Env Vars | DB_HOST, DB_USER, DB_NAME, JWT_JWKS_URI, EVIDENCE_BUS_ARN |

Cold start controls
- Provisioned concurrency on production alias.
- Connection pooling via AWS RDS Proxy or pgbouncer sidecar where applicable.

## Database Topology
- RDS for PostgreSQL Multi-AZ primary for writes.
- Read replica for heavy GET traffic.
- Parameter tuning for connection limits and query plans.
- Backups as automated snapshots and WAL archiving to S3.

## IAM and Secrets
- Lambda execution role with least privilege access to Secrets Manager, RDS, and CloudWatch.
- Secrets stored per environment with rotation Lambdas.
- No secrets in environment variables beyond secure references.

## Rollout and Rollback
- Use Lambda alias weighted traffic shifting: 10 percent for 10 minutes, then 50 percent, then 100 percent.
- CloudWatch alarms gate automatic promotion based on latency and error rate.
- Rollback by flipping alias back to the previous version.
- API Gateway stage can be reverted to the last successful deployment id.

## Deployment Verification
- Health probe `GET /storage/v1/catalog/datasets?limit=1` returns 200 under 100 ms p99.
- Synthetic check validates descriptor and Evidence Ledger audit emission.
- Database smoke query `SELECT COUNT(*) FROM catalog_dataset` executes within 100 ms p95.
- Logs show no auth failures above 1 percent.

## Configuration
| Key | Description | Default |
|-----|-------------|---------|
| READ_PAGE_LIMIT | Maximum items per list | 500 |
| CACHE_TTL_SEC | Default TTL for GET routes | 60 |
| DRR_INTEGRATION | Include freshness in describe | true |
| AUDIT_ASYNC | Emit audit via EventBridge | true |
| DB_MAX_CONN | Max pooled connections per function | 10 |

## Backup and Recovery
| Item | Method | Retention |
|------|--------|-----------|
| RDS snapshots | Automated daily and on demand | 7 to 30 days |
| WAL archive | Continuous to S3 | 14 days |
| CloudFormation exports | Template and artifacts in S3 | Permanent |

Recovery steps
1. Promote the latest clean snapshot to a new RDS instance.
2. Update Secrets Manager with new endpoint.
3. Redeploy service stack with updated DB host parameter.
4. Run reconciliation job to verify audit parity.

## Alarms
- API 5xx error rate greater than 1 percent for 5 minutes.
- p99 latency above 150 ms for 5 minutes.
- Auth failures above 5 percent.
- RDS replica lag above 30 seconds.
- Lambda throttles or concurrent executions hitting 80 percent of limit.

## Cost Controls
- Use provisioned concurrency only on production alias and high traffic routes.
- Enable API cache for list endpoints to reduce DB load.
- Use RDS storage autoscaling with alerts for growth thresholds.
- Turn off detailed logs in dev and sample success logs at 1 percent in prod.

## Ownership
| Role | Responsibility |
|------|----------------|
| Platform Foundation | Service templates, Lambda code, and API definitions |
| DevOps | CloudFormation pipelines and account boundaries |
| SRE | Alarms, observability, and runtime limits |
| Governance | Audit and Evidence Ledger policy |

## Summary
The Catalog service runs serverlessly with API Gateway and Lambda, backed by RDS for PostgreSQL. CloudFormation templates provide reproducibility. Lambda aliases make rollouts safe and rollbacks fast. API cache and provisioned concurrency keep latency within SLO while minimizing operational overhead.