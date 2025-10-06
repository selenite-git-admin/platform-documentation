# Tag Strategy

## Overview

This document defines the tagging strategy used across Commercial-Ops to attribute AWS costs and platform telemetry to tenants, plans, and internal components. Tags are essential for accurate cost allocation, reconciliation, and observability. The tagging model applies to all AWS resources managed by the platform and to internal operational metadata recorded in the admin database.

The goal is to achieve deterministic cost attribution with minimal human intervention. Tags are automatically created and applied during tenant provisioning and resource orchestration.

## Purpose and Design Goals

- **Deterministic attribution** Every AWS cost line and telemetry event should resolve to a single tenant and plan.  
- **Automation** Tags are applied programmatically during provisioning and runtime.  
- **Traceability** Tags are visible in AWS CUR and cross-checked during reconciliation.  
- **Governance** Tag schema and policies are version controlled and validated.  
- **Security** Tenants never see or modify system-level tags.

## Canonical Tag Schema

| Tag Key | Description | Scope | Example Value |
|----------|-------------|--------|----------------|
| `user:tenant_id` | Unique tenant identifier | All resources | `TEN-00123` |
| `user:plan_id` | Active plan or subscription code | All resources | `ENT-Standard-v1` |
| `user:service_component` | Logical component or module | Resource specific | `runner`, `nat`, `data-store` |
| `user:environment` | Deployment environment | All resources | `prod`, `staging`, `dev` |
| `user:platform_version` | Platform release identifier | All resources | `v2.0.0` |
| `user:owner_team` | Internal ownership group | Operator only | `platform-core`, `billing-ops` |
| `user:provisioned_at` | ISO timestamp of resource creation | All resources | `2025-10-06T12:04:00Z` |
| `user:billing_entity` | Account or sub-org attribution | Operator only | `SeleniteBusiness` |

Tags prefixed with `user:` are used for AWS cost allocation and are CUR-visible. Tags without prefix are reserved for internal system metadata stored in the admin database.

## Tag Lifecycle

1. **Define** Tags declared in the tag policy JSON template.  
2. **Apply** Tags automatically through infrastructure provisioning (e.g., Terraform, AWS CDK, or CloudFormation).  
3. **Verify** Tag compliance daily using AWS Config and internal validation jobs.  
4. **Ingest** Tags into the Commercial-Ops data model via CUR and telemetry collectors.  
5. **Reconcile** Tags against internal tenant and plan registries.  
6. **Retire** Tags when tenants are deleted or plans expire. Deprecated tags remain in CUR for historical periods.

## Tag Application

Tag application occurs at three levels:

| Level | Mechanism | Description |
|--------|------------|-------------|
| Provisioning | Terraform/CDK module | Tags injected during creation of AWS resources. |
| Runtime | Lambda or ECS tasks | Temporary or derived tags applied at job execution. |
| Data model | Admin database | Tag records linked to `tenant_master`, `plan_master`, and `component_registry`. |

### Example: Terraform Tag Block

```hcl
tags = {
  "user:tenant_id"        = var.tenant_id
  "user:plan_id"          = var.plan_code
  "user:service_component" = var.component_name
  "user:environment"      = var.environment
  "user:platform_version" = var.platform_version
  "user:owner_team"       = "platform-core"
}
```

### Example: Lambda Context Tagging

```python
import os
import boto3

def lambda_handler(event, context):
    tenant_id = event.get("tenant_id")
    plan_id = event.get("plan_id")
    resource_arn = event.get("resource_arn")
    boto3.client("resourcegroupstaggingapi").tag_resources(
        ResourceARNList=[resource_arn],
        Tags={
            "user:tenant_id": tenant_id,
            "user:plan_id": plan_id,
            "user:service_component": "runner"
        }
    )
```

## Validation and Compliance

Daily validation ensures tag coverage and correctness. The system compares AWS resource inventories with internal registries. Noncompliant resources trigger alerts in the Observability module.

| Validation Check | Description | Threshold |
|------------------|-------------|------------|
| Missing `user:tenant_id` | Resource not associated with tenant | Critical |
| Missing `user:plan_id` | Resource not linked to plan | Warning |
| Unknown service_component | Component not registered | Warning |
| Stale environment tag | Old value not matching deployment | Info |
| Duplicate tag values | Two resources with identical tag sets | Info |

Validation jobs write to the `tag_validation_log` table in the admin database.

### Example Validation SQL

```sql
SELECT
  resource_arn,
  COUNT(DISTINCT user_tenant_id) AS tenants
FROM resource_inventory
GROUP BY resource_arn
HAVING tenants > 1;
```

## CUR Tag Propagation

CUR includes all cost allocation tags that are activated in the payer account. Tag values are propagated automatically if applied before the billing cycle closes.

```bash
aws ce list-cost-allocation-tags --status active
```

To ensure continuity, tag activation must occur before month end. Tag value changes mid-cycle are reflected in subsequent CUR deliveries.

Example CUR tag field names:

- `resource_tags_user_tenant_id`
- `resource_tags_user_plan_id`
- `resource_tags_user_service_component`

These fields are parsed and normalized into `fact_cost_raw` during CUR ingestion.

## Governance and Change Control

Tag schema and allowed values are defined in a version-controlled JSON document (`tag_policy_vX.json`). The operator controls tag creation and modification through change management.

**Change policy:**

1. Propose change with rationale and affected modules.  
2. Review and approval by platform and finance leads.  
3. Implement via infrastructure code and propagate to existing resources.  
4. Record effective date and tag schema version in admin database.  

**Schema versioning table:**

| Version | Effective From | Description |
|----------|----------------|-------------|
| v1.0 | 2025-01-01 | Initial tag schema for Commercial-Ops |
| v1.1 | 2025-06-01 | Added `user:platform_version` |
| v1.2 | 2025-10-01 | Added `user:billing_entity` |

## Tag Coverage Metrics

Coverage metrics help track tagging completeness and quality.

| Metric | Definition | Target |
|---------|-------------|--------|
| `tag_coverage_pct` | Percentage of resources with required tags | 100% |
| `tenant_tag_consistency_pct` | Consistency of tenant tag values between systems | ≥ 99% |
| `plan_tag_consistency_pct` | Consistency of plan tag values between CUR and admin DB | ≥ 99% |
| `unmapped_resource_pct` | Resources missing any tag | < 1% |

## Security and Privacy

- Tags never store personally identifiable information (PII).  
- Tenant names are masked to IDs before tag creation.  
- Operators control tag write permissions; tenants have read-only access to aggregated tag data via reports.  
- Tag data is classified as internal system metadata.

## Cross References

- **cur-ingestion.md** for how tags propagate from AWS CUR.  
- **aws-cost-mapping.md** for mapping tags to metrics and allocation rules.  
- **plan-parameters.md** for quota definitions.  
- **observability.md** for tag coverage dashboards and alerts.  
- **security.md** for tag governance and access control.
