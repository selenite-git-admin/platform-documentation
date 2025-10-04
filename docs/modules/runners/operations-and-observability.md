# Operations and Observability for Runners

## Purpose
Describe how BareCount operates and observes runner classes. Operations ensure smooth execution and cost discipline, while observability provides metrics, logs, and traces to debug, optimize, and audit workloads.

## Context
Runners execute pipeline workloads across classes including serverless, container, managed ETL, and dedicated compute. Each run must be observable, auditable, and cost attributed. Operations include scheduling, scaling, recovery, and upgrades. Observability spans metrics, logs, traces, and dashboards.

## Metrics
- **Resource Metrics**  
  CPU, memory, IO, and network throughput tagged by runner class and size.

- **Execution Metrics**  
  Invocations, duration, concurrency, partition processed, shuffle volume.

- **Error Metrics**  
  Retry count, failure rate, DLQ entries, driver errors.

- **Cost Metrics**  
  Runtime hours, storage consumed, data transfer, tagged by tenant and pipeline.

- **Network Metrics**  
  Latency, error codes, tunnel health for VPN, PrivateLink, or private VPC.

## Logs
- Structured logs with correlation IDs, run tokens, and pipeline identifiers.
- Include runner class, image or driver digest, and network profile.
- Redact secrets and sensitive fields.
- Log levels: info, warn, error, debug (governance controls debug in production).
- Logs are shipped to the platform log service and retained per policy.

## Traces
- Spans across runner tasks show timing, retries, and dependencies.
- Trace context flows from ingestion to publish phases where enabled.
- Useful for multi step ETL, large joins, and latency debugging.
- Traces are sampled based on tenant policy to balance cost.

## Dashboards
- Pre built dashboards per runner class and tenant.
- Show CPU, memory, throughput, errors, retries, and cost over time.
- Include network metrics and endpoint latency for private profiles.
- Governance dashboards highlight over provisioning and policy exceptions.

## Alerts
- Trigger on sustained error rates, retry storms, or DLQ growth.
- Latency alerts for API calls or queries beyond thresholds.
- Cost alerts on projected overruns.
- Health alerts on VPN tunnels, PrivateLink endpoints, or on premise agents.

## Operations

### Scheduling
- Pipelines use orchestrator schedules to trigger runs.
- Runners must register healthy before tasks are assigned.
- Dedicated compute hosts are provisioned just in time and terminated after jobs.

### Scaling
- Serverless scales elastically per event.
- Containers scale horizontally by worker count or vertically by profile.
- Managed ETL scales parallelism dynamically within limits.
- Dedicated compute scales by provisioning more hosts under governance control.

### Recovery
- Automatic retries with capped budgets.
- Dead letter queues capture failed events or records.
- Replay functions re ingest failed records with idempotency.
- Governance approval required for large scale replays.

### Upgrades
- Runner base images and drivers patched regularly.
- Upgrades tested in staging before production.
- Rollouts use canary or phased deployment.
- Evidence records image digests and upgrade timestamps.

## Evidence
Every run writes Evidence including
- Metrics snapshot at completion
- Logs with correlation IDs
- Trace identifiers when enabled
- Cost attribution
- Policy validations and approvals

## Notes
Operations keep runners reliable and cost efficient. Observability ensures every run is measurable, debuggable, and auditable. Together they give confidence to scale pipelines safely while meeting compliance and budget goals.
