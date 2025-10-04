# Runner Classes

## Purpose
Define the standardized execution classes used to run BareCount pipelines. Runner classes abstract infrastructure so that teams select by workload characteristics and network posture rather than by vendor service names. This keeps pipeline logic portable while meeting cost, performance, and compliance goals.

## Context
Enterprises run mixed workloads. Some jobs are bursty and event driven. Others are steady and long running. Some require large memory or special drivers. Some must run inside private networks. BareCount organizes execution into four runner classes and a set of size profiles. Pipeline manifests choose a class, a size, and a network profile. Orchestration and governance handle the rest.

## Classes

### Serverless
Event driven execution that scales to zero. Suited for webhook ingestion, small to medium API pulls, file notifications, lightweight validations, and control tasks. Concurrency is elastic. Start latency exists and is acceptable for near real time use. Cost is proportional to usage.

### Container
Long lived containers with predictable CPU and memory. Suited for steady API polling, medium transforms, custom libraries, and jobs that need local caching. Horizontal scaling is controlled and observable. Images are versioned and scanned. Cost is stable and easy to forecast.

### Managed ETL
Managed distributed processing for heavy batch transforms and large joins. Suited for GDP consolidation, backfills across long windows, and KPI recomputations at scale. Parallelism and shuffle are handled by the service. Cost is optimized for large batches.

### Dedicated Compute
Virtual machines for specialized requirements such as very large memory, custom drivers, JDBC or ODBC bulk extracts, or strict locality constraints. Suited for legacy source pulls, private network appliances, and one off migration jobs. Capacity is pinned and controlled.

## Size Profiles
Each class supports a small set of sizes to reduce configuration sprawl. Sizes define CPU, memory, and concurrency where applicable. The actual numbers depend on the chosen backend and are documented in the platform catalog.

- Small  
  Light workloads, short tasks, low memory.

- Medium  
  Most steady jobs, moderate joins, typical KPI builds.

- Large  
  Heavy transforms, high concurrency, wider partitions.

- XLarge  
  Exceptional cases only. Requires governance approval.

## Network Profiles
Runner classes operate under one of the approved network profiles declared in the manifest.

- Public VPC egress  
  Outbound access to public APIs and SaaS without inbound exposure.

- Private VPC  
  Private subnets with controlled egress. Used for internal stores and staging.

- PrivateLink  
  Private service to service connectivity inside the provider network.

- VPN or site to site  
  Encrypted tunnels to enterprise networks and on premise systems.

- On premise agent  
  Execution hosted by the enterprise where data cannot leave a facility.

## Selection Guidance

### Choose by workload shape
- Bursty or event driven with short tasks  
  Choose Serverless

- Steady cadence with custom dependencies  
  Choose Container

- Heavy batch or wide joins and backfills  
  Choose Managed ETL

- Special drivers, very large memory, or strict locality  
  Choose Dedicated Compute

### Choose by network requirement
- Public SaaS APIs  
  Public VPC egress on Serverless or Container

- Private databases and internal services  
  Private VPC on Container or Managed ETL

- Vendor hosted databases with private endpoints  
  PrivateLink on Container or Managed ETL

- On premise ERPs behind firewalls  
  VPN or On premise agent on Dedicated Compute

### Typical mappings by pipeline phase
These are guidelines. The final choice depends on volume, latency, libraries, and policy.

| Pipeline phase          | Common pattern                  | Runner class           |
|-------------------------|----------------------------------|------------------------|
| Ingestion               | Webhook or small API pull        | Serverless             |
| Ingestion               | JDBC or ODBC bulk extract        | Dedicated Compute      |
| Normalization           | Medium transforms                 | Container              |
| GDP consolidation       | Large joins or windowed backfill  | Managed ETL            |
| KPI materialization     | Tests and acceptance thresholds   | Container or Managed ETL |
| Publish                 | API push or file export           | Serverless or Container |

## Anti Patterns
- Binding runner choice to a specific pipeline stage by policy. Prefer class by workload.  
- Using Dedicated Compute for simple webhook ingestion.  
- Running heavy backfills on Serverless when shuffle and spill are expected.  
- Embedding secrets or drivers in code. Use images, profiles, and the secrets service.  
- Skipping governance approval for XLarge sizes or private network access.

## Manifest Fields
Pipeline manifests declare runner class, size, and network. Values are validated against policy.

Example
```yaml
runner:
  class: container
  size: medium
  network_profile: private_vpc
  image: barecount/transform:v2.1.3
  env:
    BC_RUN_LOG_LEVEL: info
```

Serverless example
```yaml
runner:
  class: serverless
  size: small
  network_profile: public_vpc_egress
  concurrency_limit: 200
```

Managed ETL example
```yaml
runner:
  class: managed_etl
  size: large
  network_profile: privatelink
  shuffle_partition_hint: 256
```

Dedicated Compute example
```yaml
runner:
  class: dedicated_compute
  size: large
  network_profile: vpn
  drivers:
    - name: sap_hana_client
      version: 2.18.4
```

## Governance Checks
- Allowed classes and sizes per tenant  
- Network profile approvals and data residency constraints  
- Cost guardrails and quota limits  
- Image provenance and vulnerability scan status  
- Exception workflow for XLarge or non standard drivers

## Observability and Cost
- Every run emits metrics tagged with runner class, size, and network profile  
- Logs include runner identity and image digest  
- Cost attribution is recorded per run and rolled up by class and tenant  
- Persistent over provisioning triggers a review action

## Notes
Runner classes are stable concepts. Backend services can change over time without changing class selection. Keep pipeline logic independent of runner details. Adjust class and size as data volume and governance requirements evolve.
