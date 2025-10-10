# Gateway

## Role in the Platform
Edge service that terminates TLS, verifies JWTs, enforces WAF and rate limits, and routes traffic to internal services.

<a href="#fig-gateway-sequence" class="image-link">
  <img src="/assets/diagrams/security/gateway-sequence.svg" alt="Gateway sequence diagram">
</a>
<div id="fig-gateway-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/security/gateway-sequence.svg" alt="Gateway sequence diagram">
</div>
_Figure: Gateway sequence_{.figure-caption}

## Responsibilities
- Terminate TLS and enforce HSTS
- Verify JWTs and client certificates
- Apply WAF rules and anomaly detection
- Enforce per‑tenant and global rate limits
- Route requests to upstreams with retries
- Emit structured access logs

## Inputs
- Certificates and keys
- WAF rule sets and policies
- Access public keys and issuer metadata
- Routing tables and health checks

## Outputs
- Routed requests and block events
- Access logs and metrics
- Admin audit logs

## Interfaces
- Ingress endpoints for tenants and admins
- Admin API for certificates, routes, WAF/rate‑limit policies
- Observability sinks for logs and metrics

## Operational Behavior
- Zero‑copy TLS where supported
- JWT verification before routing
- Shadow‑mode rule deployments with staged rollout
- Circuit breakers and upstream health checks

## Constraints
- No plaintext secrets in logs
- No open egress from edge
- Strict default‑deny for routes

## Examples in Action
- Block malicious pattern → return 403 with reason code
- Rotate certificate before expiry via admin API

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
