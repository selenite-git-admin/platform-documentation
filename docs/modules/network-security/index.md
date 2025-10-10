# Network Security

## Role in the Platform
Implements network segmentation, private connectivity, and egress controls for tenant and system services.

<a href="#fig-network-security-sequence" class="image-link">
  <img src="/assets/diagrams/security/network-security-sequence.svg" alt="Network Security sequence diagram">
</a>
<div id="fig-network-security-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/security/network-security-sequence.svg" alt="Network Security sequence diagram">
</div>
_Figure: Network Security sequence_{.figure-caption}

## Responsibilities
- Provision per‑tenant network segments or tags
- Manage private links and peerings
- Enforce egress allow‑lists
- Monitor network flows and anomalies

## Inputs
- Provisioning requests and tenant network profiles
- Cloud provider APIs
- Policy-as-code repositories

## Outputs
- Network artifacts (VPCs/VNets, subnets, SGs)
- Connectivity status
- Audit logs and metrics

## Interfaces
- Provisioning API for network artifacts
- Connectivity API for private links
- Policy API for egress controls

## Operational Behavior
- Declarative provisioning with drift detection
- Change sets with approvals
- Continuous verification of routes and SGs

## Constraints
- No public buckets by default
- Default‑deny outbound rules
- Tenant isolation validated continuously

## Examples in Action
- Create private link for tenant warehouse
- Block unexpected egress to unknown domains

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
