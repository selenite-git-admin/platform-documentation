# Managed ETL Runner

## Purpose
Describe the managed ETL runner class for executing BareCount pipelines. This runner provides distributed processing for heavy batch transforms, large joins, windowed aggregations, and backfills. It is designed for high throughput workloads that benefit from parallelism and managed shuffle.

## Context
Some pipeline stages require wide joins across sources, long time windows, and significant I O. Serverless and simple containers are not efficient for these jobs. Managed ETL services provide a distributed engine with autoscaling, job management, and storage integration. BareCount abstracts these engines as the managed ETL runner class so that pipeline logic remains portable and governance remains consistent.

## When To Use
- Consolidating GDPs from multiple systems with large joins
- Backfills across long time ranges that require significant scan
- KPI recomputation for historic periods
- Batch ingestion from data warehouses or large object stores
- Transformations that need distributed shuffle and sorting

## When Not To Use
- Small transforms where container or serverless is more efficient
- Latency sensitive event handling
- Workloads that rely on specialized kernel modules or vendor drivers not supported by the managed service

## Sizing Profiles
Managed ETL uses size profiles that map to parallelism and memory. Exact values depend on the selected backend and are documented in the platform catalog.

- Medium  
  Default for moderate joins and windowed aggregations

- Large  
  High parallelism for wider joins and higher throughput

- XLarge  
  Exceptional batch windows and heavy backfills. Requires governance approval

## Parallelism and Shuffle
- Parallelism is controlled by the size profile and can scale during a run
- Shuffle is managed by the service and should be minimized by partition design
- Partition pruning and predicate pushdown reduce shuffle volume
- Hint fields in manifests allow teams to tune partition counts for large stages

## Partitioning and Windows
- Inputs should be partitioned by calendar periods and high cardinality keys where appropriate
- Time windows are declared in manifests with alignment to the platform calendar
- Late arriving data triggers targeted recompute instead of full restatements
- Output is written in partitioned form to support incremental reads by downstream stages

## Checkpointing and Idempotency
- Runs are idempotent through run tokens and deterministic output locations
- Checkpoints record which input partitions were processed
- Partial outputs are written to a staging location and atomically committed on success
- Failed runs can resume from the last successful checkpoint

## Network Profiles
- Private VPC for access to internal storage and services
- PrivateLink for vendor databases or services that expose private endpoints
- VPN or site to site for enterprise systems that are not reachable over PrivateLink
- Public VPC egress for reading public object stores or APIs when allowed by policy

## Security
- IAM roles grant least privilege access to storage and messaging
- Secrets are fetched at runtime from the platform secrets service
- Encryption in transit and at rest is enforced
- Evidence entries include job configuration, image or engine version, and data locations

## Cost Model
- Pay for workers and run duration
- Larger profiles cost more but finish faster
- Schedule heavy runs in off peak windows where possible
- Use partition pruning to avoid scanning data that is not needed

## Reliability
- Built in retries for task failures
- Automatic task re attempts on transient storage or network errors
- DLQ for records that fail business validations
- Comprehensive run metadata for triage and replay

## Observability
- Metrics include task attempts, spill to disk, shuffle volume, and skew indicators
- Logs capture stage level timing, validation failures, and partition statistics
- Traces can be enabled to follow critical stages
- Dashboards summarize throughput and cost by tenant and pipeline

## Operating Model
- Declare class managed_etl and a size profile in the manifest
- Provide partition and shuffle hints where needed
- Choose a network profile and validate through governance
- Use CI to version job code or notebooks and promote through environments
- Keep business logic deterministic so replays produce the same outputs

## Example
A GDP consolidation job joins sales orders from an ERP, customer master data, and currency rates for the last three years. The managed ETL runner processes monthly partitions in parallel. Partition pruning skips months with no changes. Outputs are written to the GDP Store with version tags. Evidence records include input partitions, engine version, and shuffle metrics. A later backfill increases the time window and the job scales to the large profile to meet the freshness SLO.

## Anti Patterns
- Running trivial transforms on managed ETL when containers are simpler and cheaper
- Ignoring partition design and relying on large shuffles to make joins work
- Writing outputs directly to final locations without atomic commit
- Embedding secrets in job code or notebooks
- Triggering full recompute when targeted recompute is possible

## Notes
Managed ETL is the right choice for heavy batch work. Design partitions carefully, keep logic deterministic, and capture evidence for every run. Use containers or serverless for control paths and small transforms. Together these classes keep cost and performance in balance while preserving governance.
