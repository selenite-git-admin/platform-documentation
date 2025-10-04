# Deployment Options

## Purpose
Deployment options define how connectors are executed in the platform.  
Connectors must run in environments that balance cost, scalability, compliance, and operational simplicity.  
This section describes the supported runners, the networking patterns available, and the decision factors that guide when to use each option.

## Scope
This document applies to connector execution at runtime.  
It covers compute environments including AWS Lambda, AWS Fargate, Amazon EC2, and AWS Glue.  
It also covers supported networking patterns such as VPN, site to site tunnels, AWS PrivateLink, VPC endpoints, and NAT allowlists.  
The scope includes decision guidance for developers and operators who must choose the correct runner and network combination for a connector method.

## Supported Runners

### AWS Lambda
Lambda is the default runner for lightweight connectors.  
It provides automatic scaling, pay per execution cost, and rapid startup.  
It is suitable for short lived tasks, small payloads, and low memory consumption.  
Typical use cases include file ingestion, API based extraction, or webhook handling.  
Constraints include execution time limits and restricted package sizes. Connectors that require large libraries or long running sessions should not use Lambda.

### AWS Fargate
Fargate provides container based execution without server management.  
It supports connectors that require heavy dependencies, large memory, or long execution times.  
Fargate is well suited for database extracts, bulk API loads, and connectors that perform parallel streaming reads.  
It also provides fine grained control over CPU and memory allocation.  
Fargate runs inside a VPC and can be connected to private subnets or endpoints.

### Amazon EC2
EC2 provides the highest flexibility but requires explicit lifecycle management.  
It is intended for connectors that require specialized environments, non standard libraries, or custom network adapters.  
EC2 is typically used for testing, legacy workloads, or cases where containerization is not feasible.  
Operators must manage scaling groups, patching, and monitoring directly.

### AWS Glue
Glue provides a managed Spark environment for large scale batch extractions.  
It is suitable for connectors that process terabyte scale files or require distributed compute.  
Glue is not recommended for low latency or small record extractions.  
Connectors targeting data lakes or large historical backfills should be enabled for Glue execution.

## Networking Patterns

### VPN and Site to Site Tunnels
A connector may require a persistent secure tunnel to reach on premises or partner systems.  
In such cases, a VPN or site to site tunnel is established between the platform VPC and the source network.  
This option provides stable connectivity but increases operational overhead.  

### AWS PrivateLink
PrivateLink enables private connectivity between VPCs and supported AWS or partner services.  
It eliminates the need for public IP addresses or traversing the internet.  
PrivateLink is the preferred option when the source system is exposed as an AWS service or partner endpoint.  

### VPC Endpoints
S3, DynamoDB, and many AWS services can be reached through VPC endpoints.  
Connectors running in Lambda or Fargate can use endpoints to access data sources securely within the AWS backbone.  
This reduces both cost and exposure to the public internet.  

### NAT Allowlists
When connectors must access systems on the public internet, NAT gateways with IP allowlists may be used.  
The source system must be configured to accept traffic from the fixed NAT IP range.  
This option is less secure than PrivateLink or VPN but may be unavoidable for certain SaaS APIs.  

## Decision Guidance
- Use Lambda whenever the connector is lightweight, stateless, and requires fast startup.  
- Use Fargate for connectors with larger dependencies, longer runtimes, or higher concurrency requirements.  
- Use EC2 when specialized environments or drivers are required and containerization is not possible.  
- Use Glue for large batch or distributed extract jobs.  
- Prefer PrivateLink or VPC endpoints over NAT gateways whenever possible.  
- Use VPN or site to site tunnels when connecting to enterprise systems that cannot be exposed directly to AWS.  

## Principles
- The connector must declare supported runners in its manifest.  
- Runners must be tested in CI to validate compatibility.  
- Network patterns must be explicitly documented to avoid misconfiguration.  
- Security requirements take precedence over cost when choosing a deployment option.  

## Relationships
Deployment options are tied to connector manifests, which specify supported runners and networking.  
They are enforced by the orchestrator at runtime.  
Governance modules use this information to verify compliance with enterprise connectivity policies.  

## Exclusions
This document does not cover tenant level onboarding or provisioning of VPN tunnels.  
It also does not describe non AWS runners. The focus is on the standard AWS environments supported by the platform.
