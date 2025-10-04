# Serverless Runner

## Purpose
Describe the serverless runner class for executing BareCount pipelines. This runner provides event driven execution with automatic scaling and minimal operational burden. It is best suited for short lived tasks, webhook and file events, and light to medium data processing.

## Context
Many pipeline tasks are bursty and do not require always on infrastructure. Serverless execution scales to zero when idle and scales out on demand when events arrive. Cold starts and per request limits exist and must be planned for. Serverless is a good fit for ingestion triggers, control tasks, lightweight validation, and API oriented work where latency is measured in seconds rather than milliseconds.

## When To Use
- Webhook ingestion and near real time API callbacks
- Small to medium API pulls on a cadence
- File arrival notifications and pre validation steps
- Orchestration utilities such as state writes and evidence posting
- Publish tasks that push results to SaaS endpoints
- Low to moderate memory needs and short execution time per invocation

## When Not To Use
- Heavy batch transforms with wide joins or large shuffles
- Long running jobs that exceed platform time limits
- Workloads that require specialized drivers or custom kernels
- Strictly private networks where outbound egress is not allowed

## Sizing Profiles
Serverless uses simple size tiers to reduce configuration sprawl. Actual CPU and memory per tier are defined in the platform catalog.

- Small  
  Short tasks, low memory, low concurrency

- Medium  
  Typical webhook and API jobs, moderate concurrency

- Large  
  Higher memory or CPU for bursts, increased concurrency limits

Requests above large require governance approval.

## Concurrency and Throughput
- Concurrency is elastic and governed by a per pipeline cap
- Spikes are smoothed by a queue to avoid throttling upstream systems
- Back pressure is applied when downstream dependencies slow down
- Idempotency keys and run tokens prevent duplicate side effects

## Event Sources
- HTTP callbacks for webhook connectors
- Object store notifications for file arrivals
- Timer schedules for polling APIs
- Message topics for orchestration signals

## Patterns
- Fan out on event to parallelize small independent tasks
- Aggregate partial results in a durable store for later consolidation
- Use step functions or workflow orchestration for multi step operations
- Keep functions single purpose with clear input and output contracts

## Network Profiles
- Public VPC egress for SaaS and public APIs
- Private VPC for access to internal services
- PrivateLink where vendor endpoints support private connectivity
- VPN or site to site only for small control plane actions due to latency

## Security
- Secrets are fetched at runtime from the platform secrets service
- Temporary credentials are used for storage and messaging access
- Payloads are encrypted in transit and at rest
- Audit logs include function identity, version, and request context

## Cost Model
- Pay per request and duration
- Scale to zero when idle
- Concurrency caps prevent runaway cost
- Off peak scheduling reduces spend for periodic tasks

## Reliability
- Retries with exponential backoff on recoverable errors
- Dead letter queue for failed events after retry budget is exhausted
- Idempotent handlers to allow safe replays
- Evidence Ledger entries for each run and failure

## Observability
- Metrics: invocations, duration, errors, throttles, retries
- Structured logs with correlation IDs and run tokens
- Traces for multi step workflows when enabled
- Dashboards grouped by pipeline and tenant

## Operating Model
- Declare class serverless and a size profile in the manifest
- Set concurrency caps and retry policies per pipeline
- Choose network profile and validate through governance
- Use CI to version function code and roll forward with safe deploys

## Example
An API connector receives order updates via webhook. The serverless runner validates payloads against the extractor schema, writes state and evidence, and lands the records in the Raw Stage. If the downstream store is temporarily unavailable, the function retries with backoff. After retry budget is exhausted, the event moves to the DLQ for triage.

## Anti Patterns
- Using serverless for large batch transformations
- Storing long lived connection pools inside functions
- Coupling multiple responsibilities in a single handler
- Hard coding secrets or endpoints in code
- Unbounded fan out without concurrency caps

## Notes
Serverless execution keeps ingestion and control paths responsive while controlling cost. Keep functions small, idempotent, and observable. Move heavy compute and wide joins to container or managed ETL runners. Integrate with governance for network approvals and with the Evidence Ledger for complete traceability.
