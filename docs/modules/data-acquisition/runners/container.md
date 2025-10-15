# Container Runner

## Purpose
Describe the container runner class for executing BareCount pipelines. This runner provides long lived containers with predictable resources and customizable runtimes. It is suited for steady ingestion, medium transforms, custom dependencies, and jobs that need local caching or stateful session windows.

## Context
Some workloads require libraries, drivers, or runtimes that do not fit well in serverless functions. Others benefit from predictable CPU and memory or from keeping warm state between tasks. The container runner offers stable execution with image based versioning. It pairs well with private networking and enterprise connectivity.

## When To Use
- Steady API polling at defined cadences
- Medium complexity transforms that do not need distributed shuffle
- Connectors that require vendor SDKs or language specific runtimes
- Workloads that benefit from local disk caching or connection reuse
- KPI builds with moderate windows and deterministic processing
- Publishing tasks that package and ship files to internal or external endpoints

## When Not To Use
- Very large joins or heavy batch windows that require distributed execution
- One off short control tasks where serverless is more efficient
- Jobs that demand specialized hardware or very large memory footprints

## Sizing Profiles
Container runners use simple size tiers. Exact CPU and memory values are defined in the platform catalog and may vary by environment.

- Small  
  Single worker, limited memory, low concurrency

- Medium  
  Common choice for steady ingestion and transforms

- Large  
  Higher memory or CPU, supports wider partitions and caching

- XLarge  
  Exceptional workloads only. Requires governance approval

## Scaling
- Horizontal scaling by increasing the number of container workers
- Vertical scaling by moving to larger size profiles
- Autoscaling can react to queue depth, lag, or SLO targets
- Graceful shutdown with checkpointing to avoid partial writes

## Images and Dependencies
- Images are built from a base maintained by BareCount with security hardening
- Teams layer application code and dependencies on top
- Images are scanned for vulnerabilities before deployment
- Image digests are recorded in Evidence entries for each run

## Network Profiles
- Public VPC egress for SaaS APIs
- Private VPC to reach internal stores and services
- PrivateLink for vendor endpoints without public exposure
- VPN or site to site for enterprise systems on premise

## Security
- Secrets are mounted at runtime from the platform secrets service
- Containers run with least privilege IAM roles
- Egress is restricted by network policies and firewall rules
- File system encryption and TLS in transit are enforced
- Access, image, and run metadata are logged for audit

## Cost Model
- Pay for allocated capacity and running time
- Right size using historical metrics for CPU, memory, and IO
- Batch jobs can be scheduled to off peak windows
- Autoscaling policies keep utilization within target ranges

## Reliability
- Health checks and watchdogs restart unhealthy workers
- Retries with backoff on recoverable errors
- DLQ capture for messages or records that exceed retry budget
- Idempotent handlers and run tokens for safe reprocessing

## Observability
- Metrics: CPU, memory, IO, throughput, error rate, lag
- Structured logs with correlation IDs and run context
- Traces for multi step jobs when enabled
- Dashboards grouped by pipeline, image version, and tenant

## Operating Model
- Declare class container and a size profile in the manifest
- Reference an approved image and tag
- Choose a network profile and pass governance validation
- Configure autoscaling based on queue depth or SLO targets
- Deploy via CI with canary or rolling updates
- Store checkpoints and state in platform services, not local disk

## Example
A NetSuite connector polls the REST API for changes every five minutes. The container runner maintains a warm HTTP client with token reuse and local cache for schema metadata. Records are validated against the extractor schema and landed in the Raw Stage. If the API throttles, the worker backs off and resumes without losing state. Evidence Ledger entries record image digest, network profile, and run metrics.

## Anti Patterns
- Using containers for tiny event handlers that run once per hour
- Embedding secrets in images or environment files
- Writing durable state only to local disk
- Over provisioning large containers for small workloads
- Rebuilding images on every deploy without version discipline

## Notes
Container runners provide a stable middle ground between serverless and managed ETL. Use them when you need predictable resources, custom dependencies, or private networking. Keep images small, dependencies pinned, and observability strong. Move truly heavy workloads to managed ETL and keep short bursts on serverless.
