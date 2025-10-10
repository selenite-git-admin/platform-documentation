# Secrets

## Role in the Platform
Provides secure storage, versioning, and scoped retrieval of secrets. Supports automatic rotation hooks and short‑lived credentials for client apps.

<a href="#fig-secrets-sequence" class="image-link">
  <img src="/assets/diagrams/trust/secrets-sequence.svg" alt="Secrets sequence diagram">
</a>
<div id="fig-secrets-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/trust/secrets-sequence.svg" alt="Secrets sequence diagram">
</div>
_Figure: Secrets sequence_{.figure-caption}

## Responsibilities
- Store and version secrets
- Generate scoped tokens/leases
- Rotate credentials via hooks
- Audit all reads/writes

## Inputs
- KMS for envelope encryption
- Policy/role mappings
- Tenant metadata

## Outputs
- Secret versions and leases
- Audit/evidence logs
- Metrics and traces

## Interfaces
- Tenant API for secret read (scoped)
- Admin API for write/rotate
- Lease API for short‑lived credentials

## Operational Behavior
- Encrypt secret at write; store metadata only in index
- Serve reads with least privilege and TTLs
- Rotate via provider hooks

## Constraints
- No plaintext at rest
- Strict RBAC per path/tenant
- Lease expiry enforced

## Examples in Action
- Client requests secret lease → service returns temporary credentials
- Admin rotates database password with zero‑downtime

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
