# Runners

## Purpose
Runners provide the execution environments for BareCount pipelines. They abstract the underlying infrastructure so that pipeline logic remains portable while meeting cost, performance, and network requirements.

## Context
Enterprises operate across diverse networks and workloads. Some jobs are bursty and benefit from serverless scale. Others are steady and require predictable containers or dedicated compute. Some sources sit behind strict network boundaries and require private connectivity. Runners separate these concerns from pipeline code. Teams select a runner class and a network profile that fit the workload and the compliance posture.

## Runner Classes
BareCount recommends selecting runners by class rather than binding runners to individual pipeline stages. Classes describe execution characteristics and cost shape. Stages can then map to classes through a simple guide.

- Serverless runner
  Event driven and burst friendly. Automatic scale to zero. Best for light to medium workloads and webhook or file events.

- Container runner
  Long lived containers with predictable resources. Good for steady ingestion, medium transforms, and custom dependencies.

- Managed ETL runner
  Managed data processing service suited for heavy batch transforms and large joins.

- Dedicated compute runner
  Virtual machines for specialized needs such as large memory, custom drivers, or strict locality.

## Network Profiles
Each runner can operate with one of the following network profiles. The profile is declared in the pipeline manifest and validated by governance.

- Public VPC egress
  Standard outbound access to public services and SaaS APIs.

- Private VPC
  Private subnets with no public exposure. Outbound via NAT or approved egress.

- PrivateLink
  Direct service to service connectivity without traversing the public internet.

- VPN or site to site
  Encrypted tunnels to enterprise networks and on premise systems.

- On premise agent
  Enterprise controlled execution where data cannot leave a facility.

## Selection Guide
Use runner classes and network profiles together. The table shows typical choices by pipeline phase and workload pattern. These are guidelines. Final selection depends on data size, latency, libraries, and compliance needs.

| Pipeline phase            | Workload pattern             | Recommended runner class | Typical network profile          |
|---------------------------|------------------------------|--------------------------|----------------------------------|
| Ingestion                 | Webhook or small batch       | Serverless               | Public VPC egress                |
| Ingestion                 | API poll at steady cadence   | Container                | Public VPC or Private VPC        |
| Ingestion                 | JDBC or ODBC bulk extract    | Dedicated compute        | VPN or PrivateLink               |
| Normalization             | Medium transforms             | Container                | Private VPC                      |
| Normalization             | Heavy batch joins             | Managed ETL              | Private VPC or PrivateLink       |
| KPI materialization       | Medium compute with tests     | Container                | Private VPC                      |
| KPI materialization       | Large window backfills        | Managed ETL              | Private VPC                      |
| Publish                   | API push or file export       | Serverless               | Public VPC or PrivateLink        |
| Orchestration utilities   | Small control tasks           | Serverless               | Public VPC                       |

## Operating Model
- Pipeline manifests declare runner class, size profile, and network profile.
- Size profiles define vCPU, memory, and concurrency limits in simple tiers such as small, medium, large.
- Governance validates selections against security policy and cost guardrails.
- Orchestration starts runs on the declared runner and records evidence of runner type and configuration.
- Observability captures metrics, logs, and cost tags per run and per runner.

## Cost and Performance
- Serverless is efficient for bursty and event driven ingestion. Costs scale with usage.
- Containers are predictable for steady loads and custom runtimes.
- Managed ETL is efficient for large batch windows and scale out transforms.
- Dedicated compute is reserved for specialized drivers, very large memory, or locality requirements.

## Security and Compliance
- Network profile determines how a runner reaches source systems and sinks.
- Secrets are fetched at runtime from the platform secrets service. They are not embedded in images or code.
- Evidence entries record runner identity, network profile, and access scopes for audit.
- Data never crosses a boundary that is not declared in the manifest.

## When to Change Runner Class
- When data volume or join complexity grows beyond current capacity.
- When network policy changes require private connectivity.
- When cost reports indicate persistent over provisioning or under utilization.
- When latency targets change and a different class provides a better fit.

## Cross-References
- Pipelines for lifecycle and stage definitions
- Governance for contract checks and policy validation
- Security for gateway and network controls
- Runtime for scheduler and messaging services

## Notes
Choose runner classes for classes of work, not for single tasks. Keep pipeline logic stable while you evolve runners to meet scale, cost, and security needs.
