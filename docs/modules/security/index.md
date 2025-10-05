# Security Domain

## Role in the Platform
The Security domain provides the perimeter, transport protections, and network isolation for the platform. It terminates TLS, enforces WAF and rate limits, verifies tokens, and implements network segmentation and private connectivity.

## Submodules
- [Gateway](gateway/index.md) — API edge: TLS termination, JWT verification, WAF, rate limits, routing.  
- [Network Security](network-security/index.md) — network segmentation, private links, egress controls, per‑tenant isolation.

## Position in the Platform
All tenant and admin traffic enters through the Gateway. Services communicate over segmented networks with strict egress policies. Security integrates with Access for token verification and with Trust for certificate and key management.

## Interfaces
- Tenant‑facing endpoints at the Gateway.  
- Admin endpoints for rule management and certificate rotation.  
- Network controls as code for segmentation and private connectivity.

## Constraints
- Security does not own identity or authorization rules.  
- Security changes must be audited and rolled out progressively.
