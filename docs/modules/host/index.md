# Host Modules

The Host Modules form the control layer of the BareCount Data Action Platform. 
They provide governance, tenant lifecycle management, and compliance assurance. 
They do not move or transform data directly. 
Instead, they define the guardrails that all ingestion, schema changes, KPI publishing, and workflow execution must follow.  

The Host Modules interact with user stories for tenant provisioning, schema lifecycle governance, evidence capture, and guardrail enforcement. 
They are engaged at the start of most workflows and remain relevant throughout a tenant’s lifecycle.

## Role in the Platform

- Enforce policies that keep operations compliant and consistent  
- Manage the tenant lifecycle from provisioning to offboarding  
- Validate and maintain data contracts to control schema evolution  
- Track lineage obligations so the platform can satisfy audit and regulatory requirements  

## Position in the Platform

The Host Modules provide the governance context for other module families. 
They are invoked during tenant onboarding, schema change requests, KPI publishing, and guardrail setup. 
They continue to act during operations by validating compliance, recording lineage, and ensuring tenant boundaries are respected.  

With Host Modules, the BareCount Data Action Platform can deliver not only technical functionality but also the accountability required in regulated enterprise environments.

## Modules

1. [Policy Engine](policy-registry/index.md)  
   The Policy Engine enforces guardrails defined by administrators. It prevents workflows that violate compliance rules or operational limits. It connects with guardrail setup stories and drives obligations such as data quality checks, cost controls, and access constraints.  

2. [Data Contract Registry](contract-registry/index.md)  
   The Data Contract Registry stores and validates schema definitions. It checks raw, GDP, and KPI schemas before use in the platform. It blocks incompatible changes, supports controlled rollout and rollback, and ensures schema changes are visible to dependent services.  

3. [Tenant Management](tenant-management/index.md)  
   Provisions new tenants with infrastructure baselines, handles schema extensions, and supports offboarding. It provides isolation between tenants while maintaining platform efficiency. It is tied to provisioning and offboarding user stories.  

4. [Lineage Obligations](lineage-obligations/index.md)  
   Records how data originates, transforms, and is consumed. They maintain metadata for audits and support exporting evidence to regulators. This module delivers transparency for compliance and trust.  
