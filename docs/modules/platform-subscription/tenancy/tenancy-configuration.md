# Tenancy Module Configuration

**Audience:** DevOps engineers, platform administrators  
**Status:** Working draft  
**Purpose:** Define all configuration surfaces for the Tenancy subsystem. This includes tenant manifest schema, environment and system level settings, API and webhook controls, policy and quota definitions, residency and placement settings, observability and SLO variables, controller execution tuning, security and secrets configuration, and change management. The document is self contained. It can be read without any other references.

## Configuration Overview

Tenancy configuration is declarative. Operators submit manifests that express desired state and rely on controllers to converge the actual environment. The same configuration model applies to multi tenant and single tenant deployments. Differences are captured through isolation strategy and placement fields, not through separate schemas.

**Goals of configuration:** predictability, safety, repeatability, and auditability. Every configuration mutation is validated, versioned, and auditable. Runtime drift is corrected by reconciliation. Manual mutations in the data plane are treated as violations and are reversed by the control plane.

## Configuration Surfaces

**Tenant manifest:** Declares identity, lifecycle intent, placement, isolation, quotas, plan code, contacts, webhooks, and tags.

**Environment settings:** Defines controller cadence, concurrency, retry and backoff parameters, dead letter handling, queue sizing, and default profiles.

**API controls:** Enables idempotency keys, ETags, pagination, caching hints, rate limits, and administrative overrides.

**Webhook configuration:** Defines delivery endpoints, signing keys, retry policies, dead letter streams, and operator requeue controls.

**Policy registry linkage:** References named policies for residency, encryption, retention, and action permissions.

**Quota and feature flags:** Derives limits and flags from plan codes, with policy driven overrides.

**Security configuration:** Sets IAM roles, scope boundaries, KMS keys, rotation intervals, and secrets storage.

**Observability configuration:** Specifies metrics emission, log structure, sampling, alert thresholds, and dashboard parameters.

**Migration and failover configuration:** Provides parameters for MT to ST migration, region migration, replication, cutover windows, and rollback.

## Tenant Manifest Schema

**Intent:** The manifest is the single source of truth. It must be explicit, versioned, and validated before any actions are taken.

```yaml
apiVersion: tenancy.v1
kind: Tenant
metadata:
  tenantId: t_123456
  displayName: Example Corp
  externalIds:
    billing: BILL-00988
    crm: SFDC-ACCT-44A
  tags:
    - enterprise
    - finance
spec:
  profile: singleTenant            # singleTenant or multiTenant
  planCode: ENTERPRISE_PLUS        # drives quotas and feature flags
  residency:
    allowedRegions: ["ap-south-1", "eu-central-1"]
    preferredRegion: "ap-south-1"
    dataSovereigntyRequired: true
  isolation:
    strategy: dedicatedDatabase     # schemaPerTenant or dedicatedDatabase
    networkMode: dedicatedVpc       # sharedVpc or dedicatedVpc
  quotas:
    storageGb: 5000
    eventsPerMinute: 3000
    connections: 200
  webhooks:
    signingKeyRef: secret://tenancy/webhooks/signing
    retry:
      maxRetries: 12
      backoffSeconds: 30
      jitter: true
    endpoints:
      - name: billing-sync
        url: https://billing.example.com/hooks/tenancy
        events: ["TENANCY_ACTIVATED","TENANCY_SUSPENDED","TENANCY_ARCHIVED"]
      - name: crm-sync
        url: https://crm.example.com/hooks/tenancy
        events: ["TENANCY_CREATED","TENANCY_UPDATED"]
  contacts:
    technical: tech.ops@example.com
    billing: ar@example.com
    incident: oncall@example.com
  identity:
    domain: example.com
    groups:
      adminGroup: example-admins
      readOnlyGroup: example-readers
status: {}
```

**Validation behavior:** manifests must pass residency checks, plan code verification, and quota constraints. Invalid manifests are rejected with actionable errors. All accepted manifests are stored with an immutable version id and linked to audit records.

## Environment And System Configuration

**Controller cadence and concurrency**
```yaml
controllers:
  reconciliationIntervalSeconds: 30
  maxConcurrentReconciliations: 64
  rateLimits:
    perWorkerOpsPerSecond: 20
  backoff:
    initialSeconds: 2
    maxSeconds: 120
    multiplier: 2.0
  queue:
    maxDepth: 100000
    visibilityTimeoutSeconds: 300
    deadLetter:
      target: tenancy.events.dlq
      maxReceiveCount: 10
```

**Deployment profiles**
```yaml
defaults:
  profile: multiTenant
  isolationStrategy: schemaPerTenant
  residency:
    allowedRegions: ["ap-south-1"]
    preferredRegion: "ap-south-1"
```

**Feature flag and plan binding source**
```yaml
commercial:
  planCatalogRef: catalog://plans/v3
  featureFlagsRef: catalog://features/v7
```

These settings ensure predictable throughput, bounded retries, safe failure handling, and stable default behavior across environments.

## API Configuration

**Protocols and headers**
- Base path is `/tenant-management/v1` for management endpoints that affect tenant records and lifecycle.
- Requests and responses use `application/json`.
- Authentication and authorization are enforced by the Access module with scoped roles.
- Idempotency is provided through the `Idempotency-Key` header on POST and on state changing PUT operations.
- Reads return `ETag` headers. Clients can use `If-None-Match` to take advantage of caching and reduce load.

**Pagination and search**
```yaml
api:
  pagination:
    defaultPageSize: 50
    maxPageSize: 500
  search:
    allowPrefixQueries: true
    maxQueryTimeMs: 200
```

**Rate limits and admin overrides**
```yaml
api:
  rateLimits:
    readPerTenantPerMinute: 6000
    writePerTenantPerMinute: 600
    burstMultiplier: 2
  adminOverrides:
    enabled: true
    ttlMinutes: 30
    auditRequired: true
```

## Webhook Configuration

**Delivery parameters**
```yaml
webhooks:
  signingKeyRef: secret://tenancy/webhooks/signing
  delivery:
    timeoutSeconds: 10
    maxRetries: 12
    backoffSeconds: 30
    jitter: true
  deadLetter:
    stream: tenancy.webhooks.dlq
    retentionHours: 72
  requeue:
    enabled: true
    maxBatch: 500
```

**Payload contract**
```json
{
  "event": "TENANCY_ACTIVATED",
  "tenantId": "t_123456",
  "previousState": "Draft",
  "newState": "Active",
  "timestamp": "2025-10-09T12:05:01Z",
  "sequence": 1881,
  "requestId": "req_9f3a",
  "correlationId": "corr_1c77",
  "signature": "base64:hmac..."
}
```

Webhook failures follow exponential backoff with jitter. After the configured retry count, events are moved to a dead letter stream. Operators can requeue by sequence number. All deliveries are logged with latency, response code, and retry count.

## Policy Registry Configuration

**Policy references**
```yaml
policy:
  residencyPolicyRef: policy://residency/v2
  encryptionPolicyRef: policy://encryption/v3
  retentionPolicyRef: policy://retention/v1
  actionPolicyRef: policy://actions/v2
```

**Evaluation**
- All mutating operations call the policy service before any resource change.
- Residency policy validates allowed and preferred regions.
- Encryption policy validates KMS key selection and rotation periods.
- Retention policy validates archival and deletion requests.
- Action policy validates lifecycle transitions and special operations.

Operations that cannot be audited or validated are rejected and do not change state.

## Quotas And Feature Flags

**Derivation and overrides**
```yaml
quotas:
  deriveFromPlan: true
  overrides:
    t_critical:
      eventsPerMinute: 10000
      connections: 500
```

**Feature flags**
```yaml
features:
  sourceRef: catalog://features/v7
  perTenantOverrides:
    t_beta:
      enableSandboxCloning: true
```

Quota enforcement occurs in the controller path and at the API gateway. Violations return clear errors and are logged for governance reporting. Overrides require audit records that include actor and reason.

## Residency And Placement Configuration

**Placement resolver**
```yaml
placement:
  defaultRegion: "ap-south-1"
  resolver:
    considerPreferredRegion: true
    failIfOutOfPolicy: true
    fallbackRegions: ["ap-south-2"]
```

**Isolation configuration**
```yaml
isolation:
  strategies:
    schemaPerTenant:
      dbPoolRef: "aurora/shared"
      schemaPrefix: "t_"
    dedicatedDatabase:
      templateRef: "aurora/dedicated-template"
      kmsKeyRef: "kms://keys/tenant-dedicated"
  network:
    sharedVpcRef: "vpc/shared"
    dedicatedVpcTemplateRef: "vpc/templates/dedicated-vpc"
```

Out of policy requests are rejected early. Decisions are written to the registry and included in audit entries. Region migration uses the Lifecycle Orchestrator and requires explicit cutover verification.

## Security And Secrets Configuration

**IAM role scoping**
```yaml
security:
  roles:
    controllerRole: "arn:aws:iam::111111111111:role/tenancy-controller"
    registryRole: "arn:aws:iam::111111111111:role/tenancy-registry"
    webhookRole: "arn:aws:iam::111111111111:role/tenancy-webhook"
  boundaries:
    allowActions:
      - "rds:*"
      - "kms:Encrypt"
      - "kms:Decrypt"
      - "logs:PutLogEvents"
    denyActions:
      - "s3:DeleteBucket"
```

**Key management and rotation**
```yaml
encryption:
  kms:
    defaultKeyRef: "kms://keys/tenancy-default"
    rotationDays: 90
    perTenantKeys:
      enabled: true
      templateRef: "kms://templates/per-tenant"
```

**Secrets management**
```yaml
secrets:
  provider: "secrets-manager"
  rotation:
    enabled: true
    minIntervalDays: 30
  references:
    webhookSigningKey: "secret://tenancy/webhooks/signing"
    apiTokens: "secret://tenancy/api/tokens"
```

Controllers and orchestrators only assume scoped roles. No secrets are stored in manifests or logs. Access is time bound and audited.

## Observability Configuration

**Metrics and logs**
```yaml
observability:
  metrics:
    emitIntervalSeconds: 30
    includeDimensions:
      - tenantId
      - region
      - controller
  logs:
    format: "json"
    fields:
      - timestamp
      - level
      - tenantId
      - requestId
      - correlationId
      - manifestVersion
    sampling:
      errorRateAlwaysSample: true
      infoSampleRate: 0.3
```

**Alerts**
```yaml
alerts:
  reconcileFailureRatePct: 2
  queueDepthThreshold: 50000
  webhookFailureRatePct: 1
  policyEvalLatencyMs: 200
  actions:
    pagerDutyService: "tenancy-control-plane"
    email: "platform-ops@example.com"
```

**Dashboards**
```yaml
dashboards:
  regions: ["ap-south-1","eu-central-1"]
  cuts:
    - name: Controller health
      queries: ["reconcile_duration_ms","reconcile_failures_total","queue_depth"]
    - name: Webhook delivery
      queries: ["webhook_latency_ms","webhook_failures_total"]
    - name: Policy evaluation
      queries: ["policy_eval_latency_ms","policy_eval_errors_total"]
```

All alerts include direct links to runbook procedures. Dashboards provide per tenant and per region slices for incident response.

## Controller Execution Configuration

**Idempotency and retries**
```yaml
execution:
  idempotency:
    enabled: true
    dedupeWindowMinutes: 15
  retries:
    strategy: "exponential"
    initialSeconds: 2
    multiplier: 2
    maxSeconds: 120
  timeouts:
    reconcileSeconds: 300
```

**Work queue parameters**
```yaml
queue:
  type: "sqs"
  maxInFlight: 2000
  visibilityTimeoutSeconds: 300
  deadLetter:
    stream: "tenancy.reconcile.dlq"
    maxReceiveCount: 10
```

**Safety**
- Every handler is idempotent. Reprocessing a task does not duplicate resources.
- Backoff and jitter are required to avoid coordinated retries.
- Dead letters are reviewed and requeued with sequence checkpoints.

## Migration And Failover Configuration

**MT to ST migration**
```yaml
migration:
  mtToSt:
    dataCopyMode: "snapshot-plus-cdc"
    allowDualWrite: true
    cutoverWindowMinutes: 30
    verification:
      required: true
      checks:
        - "row_counts_match"
        - "checksum_match"
```

**Region failover**
```yaml
failover:
  standbyRegion: "eu-central-1"
  replication:
    type: "logical"
    rpoSeconds: 60
  drills:
    syntheticTenants: 5
    frequencyDays: 14
  cutback:
    requireGreenTrafficMinutes: 20
```

These parameters define repeatable and safe migrations. The orchestrator checkpoints every step and emits audit entries. Rollback paths are defined for every phase.

## Defaults And Overrides

**Global defaults provide sensible behavior**
```yaml
defaults:
  profile: "multiTenant"
  isolationStrategy: "schemaPerTenant"
  quotas:
    storageGb: 200
    eventsPerMinute: 500
    connections: 50
  webhooks:
    retry:
      maxRetries: 8
      backoffSeconds: 20
      jitter: true
```

**Per tenant overrides require audit and expiry**
```yaml
overrides:
  tenants:
    t_enterprise_01:
      quotas:
        eventsPerMinute: 15000
      features:
        enableSandboxCloning: true
      expiryDays: 30
      reason: "seasonal spike"
```

Overrides are applied after plan derivation and before policy checks. Expired overrides are removed automatically.

## Validation And Linting

**Pre submit checks**
- Schema validation for all manifest fields
- Residency and placement validation against policy
- Quota sanity checks and plan binding verification
- Webhook URL and signing key reference checks
- Contact address format checks

**Lint rules**
- Tenant ids must be immutable once assigned
- Preferred region must be in allowed regions
- Plan code must exist in the plan catalog
- Isolation strategy must be one of the supported values
- No secret literals in manifests

## Versioning And Change Management

**Manifest versioning**
```yaml
versioning:
  enabled: true
  retentionVersions: 50
  changeLog:
    includeDiff: true
    includeActor: true
```

**Rollouts**
- Progressive delivery of configuration changes with region by region rollout
- Automated pause on alert thresholds
- Rollback by version id with automatic reconcile

**Audit**
- Every submit, approve, and rollout action writes an audit entry
- Audit is required for administrative overrides and emergency actions

## UI Configuration Surfaces

**Admin console parameters**
```yaml
ui:
  onboarding:
    requireResidencySelection: true
    requirePlanSelection: true
  validation:
    showPolicyOutcomes: true
  lists:
    defaultSort: "displayName"
    pageSize: 50
```

The console surfaces the same configuration that APIs accept and applies server side validation with consistent error messages.

## Data Model Configuration Dependencies

**Registry references**
```yaml
registry:
  indexes:
    - "displayName"
    - "planCode"
    - "state"
  uniqueness:
    tenantId: true
    externalIds:
      billing: true
      crm: true
```

Indexes and uniqueness constraints are part of configuration because they influence API search behavior, reconciliation performance, and correctness guarantees.

## End To End Example

```yaml
apiVersion: tenancy.v1
kind: Tenant
metadata:
  tenantId: t_9001
  displayName: Acme Ventures
  externalIds:
    billing: BILL-ACME-9001
    crm: SFDC-ACME-9001
  tags: ["enterprise","beta"]
spec:
  profile: singleTenant
  planCode: ENTERPRISE_PLUS
  residency:
    allowedRegions: ["ap-south-1","eu-central-1"]
    preferredRegion: "ap-south-1"
    dataSovereigntyRequired: true
  isolation:
    strategy: dedicatedDatabase
    networkMode: dedicatedVpc
  quotas:
    storageGb: 8000
    eventsPerMinute: 12000
    connections: 400
  webhooks:
    signingKeyRef: secret://tenancy/webhooks/signing
    retry:
      maxRetries: 12
      backoffSeconds: 30
      jitter: true
    endpoints:
      - name: ops
        url: https://ops.example.com/hooks/tenancy
        events: ["TENANCY_ACTIVATED","TENANCY_SUSPENDED","TENANCY_ARCHIVED"]
  contacts:
    technical: ops@acme.example
    billing: billing@acme.example
    incident: sre@acme.example
status: {}
```

This example is valid for both multi tenant and single tenant systems. Isolation and placement are the only differences between profiles. All other semantics are consistent.

## Summary

This configuration specification defines how tenancy is declared, enforced, and observed. It captures every surface that an operator or integrator needs in order to run the system safely at scale. The model favors explicit manifests, strong policy evaluation, comprehensive audit, and predictable reconciliation. The result is a system that is operable, compliant, and consistent across environments and regions.
