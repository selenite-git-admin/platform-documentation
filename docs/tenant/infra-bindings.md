# Tenant App – Infrastructure Bindings

## Purpose
Infrastructure bindings allow tenants to configure outbound connections and integrations.  
They connect the Tenant App to external services such as storage, email, CRM endpoints, or private networks.

## Capabilities
- **Outbound Connectors**
  - Configure email services for notifications or exports.
  - Link to object storage destinations for report delivery.
  - Connect to CRM or ERP APIs for activation targets.

- **Private Networking**
  - Establish VPC links or peering with tenant infrastructure.
  - Verify connectivity and latency during setup.
  - Fall back to mTLS-secured public endpoints if private networking is unavailable.

- **Secrets Management**
  - Define credentials and tokens for each binding in the secrets vault.
  - Secrets stored per tenant namespace with automated rotation policies.
  - Dry‑run validation before saving configuration.

## Workflow
1. Select connector type (email, storage, CRM, network).  
2. Provide credentials or connection details.  
3. Validate binding through test request.  
4. Save configuration and register binding.  
5. Monitor binding health in dashboards.  

## Roles Involved
- **Admins**
  - Configure and manage all infrastructure bindings.  
- **Operators**
  - Monitor binding health and troubleshoot failures.  
- **Executives and Business Teams**
  - Use bindings indirectly through exports, notifications, or activations.  

## Notes
- All binding configurations are auditable.  
- Failures generate alerts visible in health dashboards.  
- Credentials are never exposed in logs or UI.  
