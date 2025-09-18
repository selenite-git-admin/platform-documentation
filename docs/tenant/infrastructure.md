# Tenant App – Infrastructure

## Deployment Topology
- **Web UI**  
  - Served via CDN with global distribution.  
  - Protected by web application firewall (WAF).  
  - Static assets cached with immutable headers.  
  - Configurations refreshed with short TTLs.  

- **Back-for-Frontend (BFF)**  
  - Deployed regionally for low latency.  
  - Horizontal scaling enabled per region.  
  - Blue/green deployments used for safe rollout.  

- **Connectivity**  
  - Outbound connections to platform services over private networking when available.  
  - mTLS-secured connections for public endpoints.  
  - Outbound allow-lists used to restrict traffic.  

## Tenancy and Isolation
- **Data isolation**  
  - Per-tenant schemas or partitions in platform databases.  
  - All caches and session data are tenant-keyed.  

- **Secrets isolation**  
  - Dedicated secrets namespace for each tenant.  
  - Secrets rotated automatically under dual control.  

- **Network isolation**  
  - Private links or VPC peering for supported tenant systems.  
  - Fallback to secure public endpoints with encryption.  

## Resilience and Operations
- **SLO Targets**  
  - UI availability: 99.9% monthly.  
  - BFF availability: 99.9% monthly.  
  - P95 page load: < 1.5s.  
  - P95 API latency: < 500ms (read), < 1.5s (write).  

- **Deployments**  
  - Canary rollout with automated rollback.  
  - Error budget tracking with alerts on burn rate.  

- **Observability**  
  - Structured logs, traces, and metrics for all requests.  
  - Tenant IDs and correlation IDs included in all records.  
