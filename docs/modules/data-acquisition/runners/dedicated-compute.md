# Dedicated Compute Runner

## Purpose
Describe the dedicated compute runner class for executing BareCount pipelines. This runner provides virtual machines with pinned capacity for specialized requirements such as very large memory, custom drivers, strict locality, or legacy protocols. It is intended for source extractions or transforms that cannot run efficiently or compliantly on serverless, containers, or managed ETL.

## Context
Some enterprise integrations depend on JDBC or ODBC drivers, kernel modules, or licensed client software. Others must run inside a specific network zone or require predictable high memory instances. Dedicated compute offers full control of the host while keeping pipeline governance, evidence, and observability consistent with other classes.

## When To Use
- Bulk extracts over JDBC or ODBC from ERP, HRMS, or financial systems
- Connectors that require vendor client libraries or hardware bound drivers
- High memory transforms, in memory joins, or columnar conversion at scale
- Workloads that must run in a specific availability zone or on premises
- One time migrations or large backfills that need tuned hosts

## When Not To Use
- Short lived event handlers that fit serverless
- Medium transforms that run well on containers
- Wide distributed joins where managed ETL is more efficient
- Cases where private connectivity is available without pinning hosts

## Sizing Profiles
Dedicated compute uses instance profiles that encode CPU, memory, storage, and network. Profiles vary by environment and are listed in the platform catalog.

- Large  
  High memory or CPU for demanding single node tasks

- XLarge  
  Very high memory or IO tuned for bulk extracts and conversions

- Custom  
  Governance approved bespoke hosts for exceptional cases

## Host Management
- Images are built from hardened base templates with required agents
- Configuration management applies patches and baseline settings
- Instances are ephemeral where possible to avoid configuration drift
- Host identity and image digest are recorded in Evidence entries

## Network Profiles
- VPN or site to site for on premise ERPs and databases
- Private VPC for internal services and storage
- PrivateLink for vendor services that support private endpoints
- Public VPC egress only when policy permits and secrets allow

## Security
- Least privilege IAM roles scoped to storage, messaging, and secrets
- Secrets are fetched at runtime from the platform secrets service
- Disk encryption and TLS in transit are enforced
- Access is logged, including privileged session capture where available

## Cost Model
- Pay for provisioned capacity while hosts are running
- Use start stop orchestration to limit runtime to job windows
- Prefer ephemeral hosts for elasticity and cost control
- Attribute cost per run using tags for tenant, pipeline, and profile

## Reliability
- Health checks ensure drivers and network routes are ready before jobs start
- Retries with backoff on transient errors such as network resets
- Checkpoints and idempotent output paths enable safe restarts
- DLQ for records that fail validations beyond retry budget

## Observability
- Metrics: CPU, memory, IO, network throughput, latency to sources
- Structured logs with driver versions, connection strings redacted, and error codes
- Traces can include JDBC spans and bulk copy phases where supported
- Dashboards grouped by tenant, pipeline, and instance profile

## Operating Model
- Declare class dedicated_compute and a profile in the manifest
- Choose a network profile and pass governance validation
- Reference approved images and driver bundles by version
- Schedule jobs to match source system maintenance windows and rate limits
- Store checkpoints and state in platform services, not on local disk

## Example
An SAP HANA bulk extract requires the vendor JDBC driver and a private route over VPN. A dedicated compute runner with the XLarge profile is provisioned for the window. The job pulls monthly partitions, writes to the Raw Stage, and records driver version, image digest, and network profile in the Evidence Ledger. After completion the host is terminated to control cost.

## Anti Patterns
- Keeping hosts running idle between jobs
- Embedding secrets or licenses in images
- Writing durable state only to local disk or temp volumes
- Using dedicated compute for distributed joins that a managed service handles better
- Skipping driver version pinning and provenance records

## Notes
Dedicated compute gives maximum control for specialized needs while preserving platform governance. Use it deliberately for drivers, memory, or locality constraints. Keep hosts ephemeral, versions pinned, and evidence complete. Move general purpose workloads to serverless, containers, or managed ETL for better elasticity and cost.
