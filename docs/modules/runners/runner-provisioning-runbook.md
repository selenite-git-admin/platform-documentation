# Runner Provisioning Runbook

## Purpose
Provide operational guidance for provisioning runner classes in BareCount. This runbook describes how to deploy, validate, and manage serverless, container, managed ETL, and dedicated compute runners in real environments.

## Principles
- Everything declared in manifests and validated against policy.
- Infrastructure as code for all runner provisioning. No manual steps.
- Artifacts built once, scanned, signed, and promoted across environments.
- Governance enforced at pre-deploy, deploy, and run-time stages.
- Evidence recorded for every deploy and run.

## Workflow

### 1. Author
- Add runner.class, runner.size, and runner.network_profile to manifest.
- Reference images, job packages, or functions as needed.

### 2. Validate
- Manifest schema validation.
- Policy validation against tenant matrices of allowed classes and profiles.
- Cost estimation for scheduled runs.

### 3. Build
- Serverless: package function code.
- Container: build Docker image, sign digest.
- Managed ETL: package jobs or notebooks, pin dependencies.
- Dedicated Compute: bake golden image with agents and drivers.

### 4. Scan and Attest
- Vulnerability and license scanning for images and code.
- Store SBOM and sign artifacts.
- Attach digests to platform catalog.

### 5. Provision Shared Primitives
- VPCs and subnets for each profile.
- PrivateLink endpoints and DNS setup.
- VPN or site to site tunnels.
- IAM roles, secrets paths, logging and metrics sinks.

### 6. Deploy Runners
- Serverless: deploy function, concurrency caps, event bindings.
- Container: register task definitions, services, autoscaling policies.
- Managed ETL: register job definitions, set partition hints, retries.
- Dedicated Compute: launch templates, bootstrap, lifecycle hooks.

### 7. Register
- Create runner record in catalog with digest, role, network.
- Bind manifest reference to pipeline version.
- Write Evidence entry for deploy.

### 8. Smoke Test
- Synthetic jobs for storage, secrets, and evidence writes.
- Block promotion if tests fail.

### 9. Promote
- Use same IaC, new environment variables.
- Evidence entry records who promoted and what changed.

### 10. Operate
- Orchestrator selects runner based on manifest.
- Runs emit metrics, logs, traces, and evidence.
- Cost tags applied per run.

## Governance Gates
- Allowed runner classes and profiles per tenant.
- Exceptions only with governance approval.
- All artifacts signed, from approved registries.
- Concurrency and quota limits enforced at run-time.

## Recovery
- Failed runs retried with capped budgets.
- Dead letter queues hold exhausted records.
- Replay with run tokens ensures idempotency.
- Governance approval required for mass replay.

## Notes
Runners are provisioned via automation only. Every runner deploy, change, and run is declared, validated, observable, and auditable. This makes execution predictable, safe, and compliant across all tenants and workloads.
