
# Tenancy Module - Troubleshooting

Audience: SRE, DevOps, platform engineers  
Status: Refactor v1.0  
Purpose: Operational runbook that consolidates earlier Tenant Management runbook and observability into Tenancy. Format is symptom, checks, diagnostics, remediation. No em dashes or inline bold.

---

## 1. First response checklist

1. Capture correlation id, tenant id, environment, request id, and job id if present  
2. Confirm current state in the registry. Draft, Active, Suspended, Archived  
3. Verify profile and region. mt standard or st dedicated and target region  
4. Review recent governance events around the incident timestamp  
5. Check controller metrics and logs for reconcile errors or saturation

---

## 2. Key metrics

- tenancy_state_counts by state  
- tenancy_lifecycle_transitions_total with from and to labels  
- tenancy_api_requests_total by route, method, and status  
- tenancy_api_request_duration_ms histogram  
- tenancy_write_errors_total by route  
- tenancy_controller_reconcile_seconds and errors total  
- tenancy_events_consumer_lag and webhook_delivery_seconds

Alert suggestions  
- Reconcile error rate above baseline for 15 minutes  
- Webhook failure rate above two percent for 10 minutes  
- Event consumer lag above threshold  
- Policy denials spike for a single tenant

---

## 3. Common incidents

### 3.1 Cannot activate tenant
Checks  
- Missing plan or regions in profile  
- Governance policy gate not satisfied  
- Cloud capacity or IAM permission missing

Diagnostics  
- GET job status for activation job  
- GET tenant and topology for env target

Remediation  
- Supply plan and regions then retry activate  
- Fix IAM or region and retry  
- Request policy override if allowed

### 3.2 Wrong residency policy applied
Checks  
- Policy id mismatch between manifest and registry  
- Governance policy response rejected

Diagnostics  
- GET governance policies for tenant and environment

Remediation  
- Put the correct policy id with effective from today  
- Reconcile tenant and validate in GET

### 3.3 Downstream caches are stale
Checks  
- Change events not delivered or not consumed  
- Webhook target rejects messages

Diagnostics  
- Inspect webhook delivery attempts and event stream lag

Remediation  
- Re publish last change event or flush downstream cache  
- Fix endpoint allow list or TLS settings and replay missed events

### 3.4 Topology mismatch
Checks  
- Client did not send tenant id and env headers on calls  
- Migration from MT to ST in progress and cutover not complete

Diagnostics  
- GET topology and compare with actual cloud resources

Remediation  
- Force reconcile and rotate credentials  
- Complete cutover before resuming traffic

### 3.5 Lifecycle action stuck
Checks  
- Governance approval pending  
- Dependency lock from previous job

Diagnostics  
- GET job status and controller logs

Remediation  
- Retry with a new request id  
- Clear dependency lock and requeue

---

## 4. Procedures

### 4.1 Onboard a new tenant
1. Create tenant with slug and legal name if applicable  
2. Set regions and residency policy  
3. Set plan and contacts  
4. Activate tenant and verify state  
5. Validate topology, credentials, and event delivery

### 4.2 Suspend a tenant
1. Issue suspend with reason  
2. Confirm state is suspended  
3. Verify Access and Runtime have applied the suspension

### 4.3 Correct regions
1. Read current regions  
2. Put corrected region list  
3. Confirm list and publish change

### 4.4 Update contacts
1. Get contacts  
2. Replace with corrected list  
3. Validate emails and roles

---

## 5. Quotas and rate limits

Symptoms  
- 429 too many requests  
- Throttled workloads or rejected submissions

Checks  
- Tenant quotas in manifest and plan limits in Commercial Ops  
- Gateway and Runtime per tenant rate limits

Remediation  
- Increase quotas and apply a new manifest version  
- Upgrade plan or request a temporary burst  
- Backoff and stagger clients

---

## 6. Secrets and credentials

Symptoms  
- Rotation fails or clients receive forbidden responses

Checks  
- Secrets path and permissions  
- Last rotation timestamp and policy

Remediation  
- Rotate keys and force client refresh  
- Fix IAM path and scope

---

## 7. Migration MT to ST

Checks  
- Migration job completed and topology flipped  
- Source in read only during cutover

Remediation  
- Broadcast topology change via webhook and event stream  
- Force clients to refresh topology

---

## 8. Logs and correlation

Always capture  
- correlation id  
- tenant id  
- env  
- job id  
- controller instance id  
- manifest version

---

Summary  
This runbook rehomes Tenant Management operations under Tenancy. Use metrics and procedures here and link to Tenant Life Cycle and APIs for transition rules and request formats.


---

## Operational Notes Restored

- # Tenancy Module - Troubleshooting Audience: SRE, DevOps, platform engineers Status: Draft v0.1 Purpose: Operational runbook for diagnosing and fixing tenancy related incidents.
- Focus areas include provisioning, lifecycle, topology, quota enforcement, policies, and integration failures.
- No em dashes or inline bold are used in this document.
- Incident Primer Use this sequence on every incident before diving deep.
- Capture correlation identifiers from the client request and the controller logs.
- Confirm that the request used the correct headers.
- Check current tenant state in the registry.
- Values can be Draft, Active, Suspended, Archived.
- Retrieve the latest applied manifest version.
- Inspect governance events around the incident timestamp for policy denials or warnings.
- Provisioning Failures Symptoms - Create tenant returns 202 and remains in Draft longer than expected - Environment create stalls or times out - Topology endpoints return incomplete resource maps Checks - Controller metrics.
- Look for reconcile duration and error counts.
- Check database and object store capacity.
- Inspect permission denied entries in controller logs.
- Diagnostics Common root causes - Policy evaluation is pending or rejected in Governance - Secrets manager permission missing for key create or rotation - Region misconfiguration or unsupported profile for the target region - Existing resources conflict with desired names or prefixes Remediations - Requeue provisioning by resubmitting the same manifest version - Fix IAM permission and trigger a reconcile - Update policy bindings or request an override in Governance - Choose a different region or profile and retry with a new version --- ## 3.
- Lifecycle Actions Stuck Symptoms - Activate or Suspend returns job submitted but state does not change - Archive or Delete returns 202 then fails silently Checks - Job state and logs.
- Fetch controller logs near the correlation id.
- Some transitions require external validation.
- Access and Runtime must acknowledge state change.
- Diagnostics Remediations - Retry the lifecycle action with a new request id - Clear dependency locks if a previous action did not complete - Escalate to Governance for manual approval if required by policy --- ## 4.
- Topology Mismatch Symptoms - Application connects to a wrong schema or bucket - Runtime submits jobs to the default queue instead of tenant queue - Secrets path does not resolve Checks - Compare topology response with live cloud resources - Verify isolation profile.
- MT maps to shared resources with tenant scoped partitions.
- - Confirm that app clients pass tenantId and env on every call Diagnostics Remediations - Force reconcile for the tenant - Rotate credentials and purge client caches - For MT to ST migrations, verify cutover has completed before resuming traffic --- ## 5.
- Policy Conflicts Symptoms - Provisioning blocked with residency or encryption errors - Deletion blocked by retention policies - Profile change from MT to ST rejected Checks - Fetch active policy bindings for the tenant - Inspect latest governance events for enforcement decisions Diagnostics Remediations - Adjust the manifest to comply with policy - Request a temporary override with a time bound approval - If residency requires in region only, move the tenant to a supported region --- ## 6.
- Quota and Rate Limit Breaches Symptoms - API returns 429 too many requests - Workloads are throttled or rejected by Runtime - Storage or compute quotas reached Checks - Review quotas in the tenant manifest - Inspect Commercial Ops plan constraints - Confirm rate limits per tenant in the gateway and in Runtime Remediations - Increase quotas in the manifest and apply a new version - Upgrade plan or request a temporary burst allowance - Stagger batch submissions and enable backoff in clients --- ## 7.
- Drift Detection Reports Symptoms - Controller reports resource drift after a manual change - Reconciliation loops keep reverting external edits Checks - Compare manifest against live resource state - Confirm whether manual changes were intended Remediations - Accept desired state by updating the manifest and reapplying - If manual change was accidental, allow controller to reconcile and close the incident - Restrict direct access to provisioned resources --- ## 8.
- Webhook Delivery Failures Symptoms - External systems do not receive lifecycle events - Tenancy logs show repeated webhook retries Checks - Verify webhook URL, TLS certificate, and DNS resolution - Confirm secret is correct and HMAC signature validation passes - Inspect retry policy and dead letter queue Diagnostics Remediations - Fix endpoint availability and network allow list - Rotate webhook secret and verify HMAC on the receiver - Requeue missed events by sequence number --- ## 9.
- Event Backlog or Outage Symptoms - High lag in tenancy.events topics - Governance or Commercial Ops shows delayed updates - Controller reconciliation slows down Checks - Broker health and partition skew - Consumer lag for Governance and Commercial Ops - Controller worker saturation Remediations - Increase partitions and consumer concurrency - Apply backpressure by lowering event production rate - Scale controller workers and adjust reconcile interval --- ## 10.
- Secrets and Credentials Issues Symptoms - Rotate secrets fails - Clients authenticate but receive forbidden for resource access - Connection attempts exceed error budgets Checks - Secrets path and permissions - Key rotation policy and last rotation timestamp - Client caches for credentials and topology Remediations - Rotate keys manually and force clients to refresh - Fix IAM policy to grant least privilege for the target path - Shorten client cache TTLs for credentials --- ## 11.
- MT to ST Migration Issues Symptoms - Data becomes available in the new dedicated resources but clients still point to shared resources - Cutover causes duplicate writes or missed events Checks - Ensure migration job completed and topology flip occurred - Confirm read only mode on the source during cutover - Validate data reconciliation and checkpoint integrity Remediations - Reissue topology to all clients - Rerun final delta sync with strict idempotency - Roll back to MT only if the cutover window failed, then plan a new window --- ## 12.
- Region Placement and Failover Symptoms - Provisioning fails in selected region - Cross region failover does not pick up tenant traffic Checks - Tenant policy for residency - Region availability and capacity - Replication of secrets and policy entries Remediations - Select a supported region that satisfies residency policy - Prewarm capacity and verify replication before failover - Test failover regularly with synthetic tenants --- ## 13.
- Useful Metrics and Alerts Metrics - tenancy_controller_reconcile_seconds - tenancy_controller_reconcile_errors_total - tenancy_webhook_delivery_seconds - tenancy_events_consumer_lag - tenancy_policy_denials_total - tenancy_topology_lookup_seconds Alert suggestions - Reconcile error rate above baseline for 15 minutes - Webhook failure rate above 2 percent for 10 minutes - Event consumer lag above threshold - Policy denials spike for a single tenant - MT to ST migration job stalled --- ## 14.
- Log Fields and Correlation Always capture these fields in logs and ticket notes - correlationId - tenantId - env - jobId when applicable - controller instance id - manifest version --- ## 15.
- Escalation Matrix - Access integration issues go to the Access team - Policy or audit failures go to Governance - Usage and plan enforcement go to Commercial Ops - Runtime queue and worker capacity go to the Runtime team - Schema migration failures go to the Data platform team --- Summary This runbook provides a structured approach for diagnosing tenancy incidents.
- Follow the checks and remediations in order and always verify policy and topology before changing resources.
- Record correlation identifiers for every action so post incident review can tie logs and metrics to the original request.
