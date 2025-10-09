# Anomaly Detection Module — Configuration

Audience: Platform engineers, tenant administrators, data governance leads  
Status: Version 1.0  
Purpose: Describe how the Anomaly Detection Module is configured at both the platform control plane and the tenant plane, defining how rules, thresholds, and operational policies are declared, validated, and evolved.  

---

## Configuration Philosophy

The configuration system must be declarative, versioned, and reproducible.  
Every setting—whether platform-level or tenant-specific—must be explicitly described in a manifest or API payload.  
The module avoids hidden defaults, runtime heuristics, or in-memory state that cannot be audited.  

Configuration follows three guiding principles:

1. Clarity. Every key must have a defined purpose and documented effect.  
2. Traceability. Changes must be tracked with timestamps, actor identity, and source version.  
3. Isolation. Tenant configuration changes affect only that tenant’s workspace and do not propagate to others.  

---

## Configuration Hierarchy

| Layer | Ownership | Purpose | Persistence |
|-------|------------|----------|--------------|
| System Defaults | Platform engineering | Define base behavior such as scheduler cadence, retention limits, metric labels, and safe thresholds. | Source controlled and deployed with platform builds. |
| Tenant Policy Overrides | Tenant administrator | Customize rules, baselines, and severity mappings within the tenant environment. | Stored in the tenant configuration store. |
| Runtime Adjustments | API or workflow actions | Temporary tuning during active evaluation or remediation. | Persisted with expiry timestamps in the tenant environment. |

Changes flow downward only. A tenant cannot alter system defaults outside its namespace.

---

## Configuration Domains

### 1. Rule Definition

Rules are the core configuration objects. Each rule belongs to a named rule pack and includes parameters for target metric, baseline, predicate, severity, and actions.

Example:

```yaml
apiVersion: anomaly.v1
kind: Rule
metadata:
  ruleId: revenue_dip_daily
  tenantId: t_23fd
spec:
  target: kpi_sales
  metric: daily_revenue
  baseline: mean(trailing=7)
  predicate: (baseline - current) / baseline > 0.15
  severity: medium
  actions:
    - type: alert
      channel: email
      recipients: [finance-team@tenant.com]
    - type: workflow
      workflowId: wf_revenue_check
```

Rules may reference tenant variables and must validate successfully before activation.  
Each rule has a lifecycle: draft → validated → active → suspended → archived.

### 2. Baseline and Threshold Policies

Baseline and threshold computation are governed by tenant configuration but limited by platform policies to prevent excessive load or non-deterministic evaluation.  

| Setting | Level | Description | Default |
|----------|--------|-------------|----------|
| baseline.window.max | System | Maximum trailing window size in periods. | 12 |
| baseline.window.min | System | Minimum window size. | 3 |
| threshold.absolute.max | Tenant | Maximum allowed threshold percentage. | 1.0 |
| threshold.absolute.min | Tenant | Minimum allowed threshold percentage. | 0.01 |

If a tenant defines a baseline window outside these bounds, validation rejects the configuration.

### 3. Evaluation Scheduling

Scheduling determines how often the engine evaluates rules.

Example configuration:

```yaml
evaluation:
  mode: event_driven
  cron: "0 */6 * * *"  # fallback if no events received
  maxConcurrentJobs: 10
  retry:
    attempts: 3
    backoffSeconds: 30
```

Event driven mode executes when KPI tables publish refresh events.  
Time driven mode uses cron expressions.  
Platform-level controls enforce maximum concurrency per tenant and global job caps.  

### 4. Retention and Archival

Anomaly records and logs are retained according to tenant data policies.

| Key | Scope | Meaning | Default |
|------|--------|----------|----------|
| retention.events.days | Tenant | Retain anomaly events for review period. | 180 |
| retention.status.days | Tenant | Retain resolution status metadata. | 365 |
| retention.jobs.days | System | Retain job logs for audit. | 90 |

Retention values can be extended by platform configuration but cannot be shortened below compliance minimums.  
Archival jobs run through the control plane scheduler.

### 5. Notification and Workflow Routing

Tenants define routing logic for anomaly events.  

```yaml
notifications:
  routes:
    - severity: high
      channel: webhook
      endpoint: https://ops.tenant.com/hooks/anomaly
    - severity: medium
      channel: email
      recipients:
        - analytics@tenant.com
workflows:
  autoCreate:
    onSeverity: ["critical", "high"]
    template: wf_auto_remediation
```

All outbound connections are validated for TLS and signature compliance.  
Platform administrators may whitelist or block external endpoints through system configuration.

### 6. Security and Access Control

Security configuration ensures that only authorized identities can create or modify rules.  

```yaml
accessControl:
  roles:
    - name: tenantAdmin
      permissions:
        - anomaly:rules:create
        - anomaly:rules:edit
        - anomaly:rules:delete
        - anomaly:evaluate:manual
    - name: analyst
      permissions:
        - anomaly:rules:view
        - anomaly:events:view
```

System configuration defines which roles exist; tenant configuration assigns users to roles.  
Access decisions are evaluated by the Access module using JWT claims.

### 7. Audit and Versioning

Every configuration change generates an immutable audit record with these fields:

- Actor (user id or system service)  
- Action (create, update, delete, activate, suspend)  
- Target object (rule id or configuration key)  
- Before and after values  
- Timestamp (UTC)  
- Source (API, CLI, workflow)  

Audit records are retained for at least 365 days or longer per compliance policy.  

Versioning follows semantic style:  
- Increment patch version for parameter changes.  
- Increment minor version for added rules.  
- Increment major version for schema changes.  

---

## Platform Control Configuration

The platform maintains global controls that apply to all tenants.

### Scheduler Defaults

| Key | Description | Default |
|------|-------------|----------|
| scheduler.intervalMinutes | Default time between rule evaluations if no trigger event. | 60 |
| scheduler.timezone | Default timezone for cron expressions. | UTC |
| scheduler.maxParallelJobs | Maximum concurrent evaluations across tenants. | 200 |

### Resource Quotas

| Key | Description | Default |
|------|-------------|----------|
| tenant.maxRules | Maximum rules per tenant. | 500 |
| tenant.maxRulePacks | Maximum rule packs per tenant. | 50 |
| tenant.maxConcurrentJobs | Max concurrent evaluations per tenant. | 20 |

Exceeding quotas results in validation errors when rules are created or activated.

### Control Plane Parameters

| Parameter | Description |
|------------|-------------|
| dispatcher.batchSize | Number of rules per evaluation job. |
| dispatcher.maxQueueDepth | Global job queue limit before backpressure. |
| catalog.validationMode | strict or lenient rule schema validation. |
| catalog.syncInterval | Frequency of synchronization between catalog and tenant stores. |

Platform administrators adjust these settings through the control configuration service.  
All changes are versioned and logged similarly to tenant configurations.

---

## Environment-Specific Configuration

The module supports environment isolation across dev, staging, and production environments.  

Example:

```yaml
environments:
  dev:
    evaluation:
      mode: time_driven
      cron: "0 */12 * * *"
    retention:
      events: 14
  prod:
    evaluation:
      mode: event_driven
      retry:
        attempts: 5
        backoffSeconds: 60
```

Each environment uses its own registry and evaluation pipeline.  
Rules can be promoted between environments using versioned manifests.

---

## Configuration APIs

The configuration service exposes endpoints for full lifecycle management.  

| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /api/v1/anomaly/rules | Create a new rule. |
| GET | /api/v1/anomaly/rules/{ruleId} | Retrieve rule details. |
| PUT | /api/v1/anomaly/rules/{ruleId} | Update rule. |
| PATCH | /api/v1/anomaly/rules/{ruleId}/status | Activate or suspend rule. |
| GET | /api/v1/anomaly/config | Get current tenant configuration. |
| PUT | /api/v1/anomaly/config | Update configuration manifest. |
| GET | /api/v1/anomaly/system | Read global control configuration (platform admins only). |

All endpoints require X-Tenant-Id and JWT authentication headers.  
Responses include current version numbers and audit identifiers.

---

## Validation Pipeline

Configuration changes go through a validation pipeline:

1. Schema validation checks structural correctness.  
2. Dependency resolution verifies referenced metrics and workflows exist.  
3. Constraint evaluation enforces system limits and type safety.  
4. Dry run executes rules in simulation mode against sample data.  
5. Approval workflow may be required for critical or cross-team rules.  

Only after successful validation does a configuration become active.

---

## Operational Management

Configuration is stored in versioned repositories or databases.  
Operations teams can:

- Export and import configuration manifests.  
- Roll back to earlier versions.  
- Apply batch updates to multiple tenants through automation.  
- Monitor configuration drift using daily reconciliation jobs.

Each change is signed and verified before deployment.

---

## Example Composite Configuration Manifest

```yaml
apiVersion: anomaly.v1
kind: TenantConfiguration
metadata:
  tenantId: t_23fd
  version: 1.2.0
spec:
  rulePacks:
    - name: finance-defaults
      enabled: true
    - name: sales-experiments
      enabled: false
  evaluation:
    mode: event_driven
    retry:
      attempts: 3
      backoffSeconds: 45
  retention:
    events: 180
  notifications:
    routes:
      - severity: high
        channel: webhook
        endpoint: https://ops.tenant.com/hooks/anomaly
  accessControl:
    roles:
      - name: admin
        permissions:
          - anomaly:*
```

This manifest is stored under the tenant’s configuration store and is auditable, promotable, and reversible.  

---

## Summary

Configuration defines how anomaly detection behaves for every tenant and how the platform enforces safe, scalable execution.  
By keeping configuration declarative, versioned, and isolated, the module ensures transparency and repeatability across environments.  
Tenants gain flexibility to tune their detection logic while the platform retains control over operational safety and governance.  
This dual configuration model creates a balanced system that is adaptable, secure, and fully auditable.
