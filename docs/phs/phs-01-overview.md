# Platform Host Services (PHS) Overview

Platform Services provide the control plane and shared services for the BareCount Data Platform.
These services enforce contracts, manage metadata, and supply common capabilities such as identity, policy, observability, and storage fabric controls.

## Scope
### Control Plane Services
- Store and enforce **active contracts** (Raw, GDP, KPI).  
- Persist version metadata (Major–Minor–Update), lineage, audit evidence, and compliance signals.  
- Expose stable APIs for CICD, CLI, and host/tenant apps.  
- Provide Schema & Contract Registry for Raw/GDP/KPI contracts.

### Common Shared Services
- Identity & Access (IAM) with RBAC/ABAC.  
- Tenancy Manager for isolation across tenants and deployment models.  
- Policy & Compliance Engine for residency, retention, security, audit.  
- Configuration Service (versioned, environment/tenant overlays).  
- Secrets & Key Management (issuance, rotation, envelope encryption).  
- Observability Hub (metrics, logs, traces, events, SLO dashboards).  
- Orchestration & Scheduling (jobs, retries, idempotency).  
- Storage Fabric (object, relational, cache, stream) with tenancy/residency enforcement.  
- Data Protection & Lifecycle (backup, restore, purge, legal hold).  
- API Gateway + Ingress Enforcement (authN, quotas, throttling, schema/policy enforcement).  

### Security Model
- Only the **Platform Super Admin** has direct access to PHS.  
- Role is **narrow but high-power**: contracts, versioning, audit, shared service configuration.  
- Access only via **AWS CLI/CDK/CICD** (no UI/console access).  
- MFA enforced; least-privilege IAM policies applied.  

### Contracts Enforcement
- **Raw contracts**: enforced at data ingress (schema validation, key checks, freshness/volume thresholds).  
- **GDP contracts**: enforced at normalization boundaries (reference integrity, canonical mapping).  
- **KPI contracts**: enforced at metric build and delivery (formula correctness, thresholds, delivery SLAs).  
- Enforcement is runtime and policy-driven, with audit events recorded at each checkpoint.  

### Outbound Connectivity
- **Network**: outbound traffic controlled via NAT gateways, VPC endpoints, PrivateLink, or egress proxies.  
- **Policy**: deny-by-default; connector-specific allowlists (domains/IPs), TLS/mTLS, DNS pinning, IAM-scoped roles.  
- **Controls**: request signing, quotas, throttling, and audit logging per contract + version ID.  
- **Observability**: outbound latency, error rate, and volume monitored and alarmed per connector.  
- **Change Management**: outbound rules modified only via CDK/Pipeline; no console edits.

## End State
With PHS deployed, the platform has a durable control plane and a set of shared services.  
The Admin Host App manages contract lifecycles, while PHS ensures enforcement, audit, and reliability at runtime.
