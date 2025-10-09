
# Tenancy Module - Configuration

> Audience: DevOps engineers, platform administrators  
> Status: Draft v0.1  
> Purpose: This document explains configuration surfaces, manifests, controller flags, and operational parameters used by the Tenancy module for provisioning and lifecycle management.

---

## 1. Overview

Configuration in the Tenancy module is declarative. Every tenant, environment, and isolation profile is defined through YAML manifests or configuration APIs. The controller reads these manifests, validates them, and reconciles the desired state with the actual infrastructure.

The goal of configuration is predictability. Each environment behaves consistently regardless of how it was created or who executed the command.

---

## 2. Configuration Layers

The module operates across three configuration layers:

1. **Declarative Manifests**  
   YAML or JSON definitions submitted through CLI, API, or Admin UI. They define the desired state of a tenant and its environment topology.

2. **Controller Configuration**  
   Runtime flags and environment variables that tune behavior of the tenancy controllers, such as retry intervals, reconciliation modes, and quota limits.

3. **Policy Registry**  
   Central registry of compliance, residency, and encryption policies. These are referenced in tenant manifests but maintained independently by the Governance module.

---

## 3. Tenant Manifest Structure

Example manifest:

```yaml
apiVersion: tenancy.v1
kind: Tenant
metadata:
  tenantId: t_5f9d83
  organizationId: org_delta
spec:
  profile: mt-standard      # or st-dedicated, st-byoc
  environments: [dev, stage, prod]
  quotas:
    storageGiB: 500
    concurrentJobs: 20
  policies:
    dataResidency: in-region-only
    encryption: kms-per-tenant
  billing:
    plan: professional
    costCenter: fin-ops
  network:
    region: ap-south-1
    privateEndpoint: true
  tags:
    owner: team-analytics
    priority: high
```

### Key Fields

| Field | Description |
|--------|--------------|
| apiVersion | Schema version for the tenancy manifest. |
| kind | Type of resource, always "Tenant". |
| metadata.tenantId | Unique immutable identifier for the tenant. |
| metadata.organizationId | Identifier of the parent organization. |
| spec.profile | Deployment type. Can be "mt-standard", "st-dedicated", or "st-byoc". |
| spec.environments | List of environment codes under this tenant. |
| spec.quotas | Storage and compute limits. |
| spec.policies | References to policies in the Governance module. |
| spec.billing | Optional cost allocation details used by Commercial-Ops. |
| spec.network | Region and endpoint configuration. |
| spec.tags | Freeform metadata for internal tracking. |

---

## 4. Controller Configuration

The Tenancy Controller reads its own configuration at startup. These settings determine how manifests are applied and how failures are handled.

Example controller configuration file:

```yaml
controller:
  reconciliationInterval: 60s
  maxRetries: 5
  backoffFactor: 2.0
  defaultProfile: mt-standard
  defaultRegion: ap-south-1
  maxConcurrentReconciliations: 10
  enableMetrics: true
  enableAuditLogging: true
  isolationStrategy:
    default: mt
    allowOverride: true
  secretsManager:
    provider: aws
    rotationDays: 30
```

### Explanation

- `reconciliationInterval` controls how often the controller checks for drift.  
- `maxRetries` and `backoffFactor` define retry strategy for failed operations.  
- `defaultProfile` specifies which deployment profile applies when none is provided.  
- `maxConcurrentReconciliations` controls concurrency and resource pressure.  
- `isolationStrategy` defines default strategy and whether tenants can override it.  
- `secretsManager` defines provider and secret rotation policy.

---

## 5. Policy Registry Configuration

The Tenancy module reads and applies policies registered by the Governance service. These policies are not defined in tenant manifests but referenced by name.

Example policy entry:

```yaml
policyId: dataResidency.in-region-only
type: residency
spec:
  allowedRegions:
    - ap-south-1
    - ap-southeast-1
  enforcement: hard
```

Another example for encryption:

```yaml
policyId: encryption.kms-per-tenant
type: encryption
spec:
  provider: aws-kms
  keyPolicy: tenant-specific
  keyRotationDays: 90
```

Policies are fetched at provisioning time and cached locally for enforcement.

---

## 6. Environment Configuration

Each tenant may define multiple environments. The configuration applies recursively to each environment. Overrides can be applied through environment-level manifests.

Example environment manifest snippet:

```yaml
apiVersion: tenancy.v1
kind: Environment
metadata:
  tenantId: t_5f9d83
  name: stage
spec:
  region: ap-south-1
  storageGiB: 300
  computeQuota: 10
  isolation:
    level: strict
  retentionDays: 90
```

Environment manifests can be embedded within the Tenant manifest or submitted independently.

---

## 7. Operational Parameters

| Parameter | Description |
|------------|-------------|
| TENANCY_LOG_LEVEL | Sets verbosity for controller logs. |
| TENANCY_DEFAULT_REGION | Region used for resource provisioning when unspecified. |
| TENANCY_METRICS_PORT | Exposes Prometheus metrics for controller health. |
| TENANCY_RETRY_LIMIT | Overrides retry count for API operations. |
| TENANCY_AUDIT_MODE | Enables or disables event emission to Governance. |
| TENANCY_POLICY_REFRESH_INTERVAL | Determines how often policy cache is refreshed. |

These parameters can be configured through environment variables or Helm values when deploying the controller.

---

## 8. Validation and Drift Detection

When a manifest is submitted, it passes through a validation chain:

1. **Schema validation** ensures structural correctness.  
2. **Policy validation** checks compliance with governance rules.  
3. **Quota validation** verifies requested limits against global caps.  

During reconciliation, the controller compares live state with manifest definitions. Any difference triggers a corrective action. Drift detection logs differences to observability metrics.

---

## 9. Versioning and Change Control

Every tenant manifest carries a version annotation. The controller stores historical manifests for audit purposes. Changes are applied incrementally with rollback support.

Example annotation:

```yaml
metadata:
  annotations:
    version: v1.3.2
    appliedBy: admin@company.com
```

Manifests are immutable after successful application. Updates must use a new version.

---

## 10. Example: Full Tenant Provisioning Flow

1. Administrator submits a Tenant manifest via API or CLI.  
2. The controller validates manifest and applies policy checks.  
3. Resources are provisioned according to the selected isolation strategy.  
4. Controller emits audit events to Governance and billing signals to Commercial-Ops.  
5. Tenant enters Active state; environment credentials and endpoints become available.

---

## 11. Best Practices

- Keep manifests version-controlled with GitOps or similar workflows.  
- Avoid manual modification of provisioned resources.  
- Use descriptive tags to enable cost tracking.  
- Limit concurrent reconciliations in large clusters.  
- Regularly review policy registry entries for compliance updates.  
- Validate manifests in staging before applying to production tenants.

---

**Summary**  
The configuration layer in the Tenancy module ensures predictable and auditable provisioning through declarative manifests and consistent controller behavior. It enables developers and operators to maintain infrastructure uniformity across both shared and dedicated deployment models.
