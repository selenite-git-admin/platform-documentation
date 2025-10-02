# Deployment

## Deployment Options

### Multi-tenant (Shared)
The shared deployment model is designed for speed and affordability.
It provides each tenant with logically isolated data and contracts, enforced by strong access controls.
Shared infrastructure delivers elastic scale and continuous updates without customer-side maintenance.
This option is well suited for enterprises that need fast onboarding, lower cost of ownership, and secure separation without heavy compliance obligations.

### Single-tenant (Dedicated)
The dedicated deployment model provides an isolated database and frontend per enterprise.
It retains the same contract-bound foundation but ensures physical separation of data and control surfaces.
This model supports customer-specific security policies, audit requirements, and integration rules.
It is intended for compliance-heavy industries and enterprises that require maximum isolation while still benefiting from the shared platform core.

### On-prem Hybrid
The on-prem hybrid deployment model combines managed cloud services with customer-hosted components.
Core governance, contracts, and action planes run in the cloud, while sensitive data or specific workloads remain inside the enterprise network.
This model balances compliance and residency requirements with the benefits of elastic scale and managed upgrades.
It is intended for enterprises that must keep certain datasets or processes local while still leveraging the full capabilities of the platform.