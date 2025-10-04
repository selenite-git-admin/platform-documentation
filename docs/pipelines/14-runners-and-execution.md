# Runners and Execution

## Purpose
The Runners and Execution stage defines how pipelines are executed in the BareCount Data Action Platform. It provides flexible execution contexts that balance cost, performance, and network constraints. This stage abstracts infrastructure details so that developers focus on contracts and logic while the platform manages execution.

## Context
Enterprise pipelines must run across diverse environments: cloud-native, hybrid, or on-premise. Network boundaries, data gravity, and compliance often dictate where and how jobs execute. BareCount introduces a runner abstraction that allows the same pipeline definition to run on multiple backends such as AWS Lambda, Fargate, Glue, or EC2. Runners integrate with orchestration, observability, and evidence systems for consistent operations.

## Key Capabilities

### Runner Abstraction
- Pipelines declare runner type in their manifest.  
- Runner options include serverless (Lambda), containerized (Fargate), managed ETL (Glue), or dedicated compute (EC2).  
- Abstraction ensures that pipelines are portable across environments without code changes.

### Network Models
- Runners support multiple network connectivity options:  
  - VPN or site-to-site tunnels for enterprise systems.  
  - AWS PrivateLink for secure connectivity without public exposure.  
  - VPC peering for internal data exchange.  
  - On-premise runners for air-gapped systems.  
- Network choice is declared in the manifest and enforced by governance.

### Scaling and Scheduling
- Runners integrate with orchestration to scale up or down based on workload.  
- Batch jobs can be distributed across multiple runner instances.  
- Serverless runners auto-scale with request volume, while EC2/Fargate runners provide predictable capacity.  

### Security
- Runners inherit BareCount’s security policies, including encryption, IAM roles, and secrets management.  
- Data never leaves the declared network boundary.  
- Audit logs record runner identity, configuration, and execution environment.

### Cost Controls
- Serverless runners are cost-effective for bursty workloads.  
- Containerized and EC2 runners are optimized for steady workloads.  
- Policies prevent misuse of expensive runner types for trivial jobs.  

## Operating Model
- Developers specify runner type and network requirements in pipeline manifests.  
- Operators monitor execution through observability dashboards.  
- Governance teams validate runner selections against compliance requirements.  
- Runners are provisioned and managed by the platform, reducing manual effort.

## Example
A GDP transform job for SAP runs on AWS Glue due to large-scale batch requirements. The manifest specifies Glue runner with VPC PrivateLink connectivity to SAP HANA. Logs and metrics are emitted automatically, and the Evidence Ledger records runner type, configuration, and execution details. In contrast, a webhook ingestion pipeline runs on Lambda with auto-scaling enabled.

## Notes
Runners decouple pipeline logic from infrastructure. BareCount ensures that pipelines execute reliably and securely across environments, giving enterprises flexibility without sacrificing governance. The abstraction simplifies developer experience while providing operators with predictable control.
