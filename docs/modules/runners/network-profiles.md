# Network Profiles

## Purpose
Define the approved network profiles for BareCount runners. Network profiles control how runners reach source systems and sinks. They balance security, compliance, and performance while keeping pipeline logic portable.

## Context
Enterprises operate across public clouds, private networks, and on premise datacenters. Connectivity choices have direct impact on security, latency, and cost. BareCount encodes these choices as network profiles that are declared in manifests and validated by governance. Profiles are consistent across runner classes so teams can change execution without redesigning connectivity.

## Profiles

### Public VPC egress
Standard outbound access to public services and SaaS APIs without inbound exposure.
- Use for public REST and file based sources
- Combine with serverless or container runners for small to medium workloads
- Enforce egress controls with allow lists and rate limits
- Prefer TLS and token based auth

### Private VPC
Private subnets with no public ingress and controlled egress.
- Use for internal services, private data stores, and staging zones
- Combine with containers or managed ETL for steady and heavy workloads
- Route outbound traffic through NAT or approved proxies
- Attach security groups and network ACLs with least privilege rules

### PrivateLink
Private service to service connectivity inside the provider network.
- Use when vendors expose private endpoints or when reaching managed databases privately
- Avoids traversal over the public internet
- Combine with containers or managed ETL
- Requires endpoint and DNS setup managed by platform networking

### VPN or site to site
Encrypted tunnels between BareCount VPC and enterprise networks.
- Use for on premise ERPs, databases, and file shares
- Plan for latency and throughput constraints
- Combine with dedicated compute for driver based extractions or with containers for API access
- Coordinate change windows with enterprise network teams

### On premise agent
Execution hosted by the enterprise where data cannot leave the facility.
- Use when data residency prohibits cloud connectivity
- Agent pulls manifests and writes lineage to the Evidence Ledger
- Outputs land in a staging area that mirrors Raw Stage semantics
- Requires local secrets integration and audit logging

## Selection Guidance

### Choose by data location
- Public SaaS or open APIs
  Choose Public VPC egress
- Vendor managed private endpoints
  Choose PrivateLink
- Internal cloud networks
  Choose Private VPC
- On premise systems
  Choose VPN or on premise agent

### Choose by risk posture
- Lowest exposure with managed private endpoints
  PrivateLink
- Strong isolation within cloud account
  Private VPC
- Acceptable risk for public APIs with controls
  Public VPC egress
- Strict residency or regulatory boundaries
  On premise agent

### Performance notes
- PrivateLink reduces latency versus internet paths
- VPN throughput depends on tunnel size and encryption settings
- On premise agents avoid cross network copies but depend on local hardware
- Use close region alignment to reduce network round trips

## Security Controls
- Secrets are fetched at runtime from the platform secrets service
- Mutual TLS and certificate pinning where supported
- Egress allow lists per profile to restrict destinations
- Flow logs and packet mirrors where policy requires deeper inspection
- Periodic validation of DNS and endpoint configuration
- Evidence entries record profile name, routes, and access scopes

## Cost Considerations
- PrivateLink incurs endpoint and data processing costs
- VPN has hourly tunnel charges and data transfer costs
- Public egress may incur data transfer and NAT gateway costs
- On premise agents shift cost to enterprise hardware and operations
- Choose profiles that minimize cross region or cross provider traffic

## Observability
- Metrics include connection success rate, latency, throughput, and error codes
- Logs capture endpoint resolution, TLS handshakes, and retries
- Dashboards segment performance by profile and tenant
- Alerts trigger on failure rate, rising latency, or tunnel instability

## Operating Model
- Declare network_profile in the runner section of the manifest
- Governance validates profile selection against tenant policy and data classification
- Networking teams provision endpoints, routes, and tunnels
- Changes are promoted through environments with smoke tests for connectivity
- Break glass procedures exist for profile cutover during incidents

## Examples
- A Salesforce ingestion uses Public VPC egress with serverless. The profile enables outbound only with token based auth and strict allow lists.
- An SAP HANA extraction uses VPN and dedicated compute. The profile enforces private routes and records driver versions in evidence.
- A Workday GDP transform uses PrivateLink on a container runner. Latency is low and data never traverses the public internet.

## Anti Patterns
- Mixing public and private routes without clear intent or controls
- Hard coding IP addresses in application code
- Using Public VPC egress for sensitive databases that offer PrivateLink
- Running high volume extracts over a small VPN tunnel
- Skipping DNS control and relying on default resolvers for private endpoints

## Notes
Pick the simplest profile that satisfies security and performance. Keep profiles consistent across environments. Validate connectivity as part of deployment. Record profile details in evidence for every run so audits can rebuild the exact network context.
