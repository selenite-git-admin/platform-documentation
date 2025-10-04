# Runner Selection Guide

## Purpose
Provide an opinionated method to choose runner classes and network profiles for BareCount pipelines. The guide maps workload and risk characteristics to a recommended runner class, size, and network profile.

## Context
Selecting execution environments ad hoc leads to higher cost and lower reliability. This guide standardizes choices so teams design once and operate consistently. Pipelines stay portable because runner class and network profile are configuration, not code.

## Decision Tree

1. Where is the source data
   - Public SaaS or open API
     Go to step 2
   - Vendor private endpoint
     Recommend Container or Managed ETL with PrivateLink
   - Internal VPC service or private database
     Recommend Container or Managed ETL with Private VPC
   - On premise system
     Recommend Dedicated Compute or Container with VPN or on premise agent

2. What is the workload shape
   - Burst events or webhook callbacks
     Recommend Serverless
   - Steady polling or medium transforms
     Recommend Container
   - Heavy batch with large joins or long windows
     Recommend Managed ETL
   - Special drivers or very large memory
     Recommend Dedicated Compute

3. What are the latency expectations
   - Seconds to minutes
     Serverless or Container
   - Minutes to hours
     Container or Managed ETL
   - Hours and backfills
     Managed ETL or Dedicated Compute

4. What are the compliance constraints
   - Public egress allowed with controls
     Public VPC egress
   - Private endpoints required
     PrivateLink
   - Strict isolation inside account
     Private VPC
   - Data must stay on premises
     VPN or on premise agent

## Comparison Matrix

| Criterion                 | Serverless             | Container                 | Managed ETL                 | Dedicated Compute            |
|--------------------------|------------------------|---------------------------|-----------------------------|------------------------------|
| Workload pattern         | Bursty events          | Steady tasks              | Heavy batch                 | Specialized or legacy        |
| Startup latency          | Cold starts possible   | Warm workers              | Job spin up                 | Host provisioning            |
| Throughput               | Elastic bursts         | Predictable scale         | High parallelism            | High per node                |
| Stateful needs           | Avoid long state       | Good for warm state       | Externalized state          | Full control                 |
| Libraries and drivers    | Limited runtime        | Custom images             | Service supported           | Any approved driver          |
| Cost shape               | Pay per request        | Pay per time and size     | Pay per workers and time    | Pay for pinned capacity      |
| Network options          | Public, Private        | Public, Private, PrivateLink, VPN | Private, PrivateLink, VPN | Private, PrivateLink, VPN    |
| Typical phases           | Ingestion control      | Ingestion and KPI compute | GDP consolidation, backfills| JDBC or ODBC extracts        |

## Sizing Guidance
- Start with Medium for unknown workloads
- Scale up when CPU or memory is consistently above 70 percent
- Scale out when queue lag or input backlog grows
- Use XLarge only with governance approval and a cost plan

## Network Profile Guidance
- Public VPC egress for SaaS APIs and public data
- Private VPC for internal stores and staging
- PrivateLink for vendor managed private endpoints
- VPN or on premise agent for systems inside enterprise networks

## Examples

### Webhook ingestion to Raw Stage
- Runner class
  Serverless
- Size
  Small
- Network profile
  Public VPC egress
- Notes
  Concurrency capped to protect downstream stores. Idempotency keys used for safe retries.

### JDBC bulk extract from SAP HANA
- Runner class
  Dedicated Compute
- Size
  XLarge
- Network profile
  VPN
- Notes
  Vendor drivers pinned. Host stopped after job to control cost.

### GDP consolidation across three sources
- Runner class
  Managed ETL
- Size
  Large
- Network profile
  Private VPC or PrivateLink
- Notes
  Partition pruning and shuffle hints set in manifest.

### KPI materialization with moderate windows
- Runner class
  Container
- Size
  Medium
- Network profile
  Private VPC
- Notes
  Validation tests and acceptance thresholds enforced before publish.

## Anti Patterns
- Using serverless for large joins or hour long runs
- Over sizing containers when horizontal scale is sufficient
- Running trivial transforms on managed ETL
- Keeping dedicated hosts idle between runs
- Selecting Public egress when PrivateLink exists
- Embedding secrets in images or code

## Manifest Snippets

Serverless
```yaml
runner:
  class: serverless
  size: small
  network_profile: public_vpc_egress
  concurrency_limit: 150
```

Container
```yaml
runner:
  class: container
  size: medium
  network_profile: private_vpc
  image: barecount/etl:2.4.0
```

Managed ETL
```yaml
runner:
  class: managed_etl
  size: large
  network_profile: privatelink
  shuffle_partition_hint: 256
```

Dedicated Compute
```yaml
runner:
  class: dedicated_compute
  size: xlarge
  network_profile: vpn
  drivers:
    - name: oracle_client
      version: 19.20
```

## Notes
Treat runner selection as configuration that can evolve. Begin with conservative sizes and adjust by metrics. Validate network profiles through governance. Record choices in Evidence for every run so audits can reconstruct the execution context.
