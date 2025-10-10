# Encryption

## Role in the Platform
Provides key management and cryptographic services (envelope encryption, signing, verification). Ensures encryption at rest, in transit, and for application‑level secrets.

<a href="#fig-encryption-sequence" class="image-link">
  <img src="/assets/diagrams/trust/encryption-sequence.svg" alt="Encryption sequence diagram">
</a>
<div id="fig-encryption-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/trust/encryption-sequence.svg" alt="Encryption sequence diagram">
</div>
_Figure: Encryption sequence_{.figure-caption}

## Responsibilities
- Manage key aliases and versions
- Perform envelope encryption/decryption
- Issue and verify signatures
- Rotate keys and enforce key policies
- Expose HSM/KMS backed primitives

## Inputs
- KMS/HSM providers
- Policy for key rotation
- Tenant metadata (residency)
- Access claims

## Outputs
- Ciphertexts, signatures, and key metadata
- Audit/evidence entries
- Metrics and traces

## Interfaces
- Admin API for key alias/rotation
- Crypto API for encrypt/decrypt/sign/verify
- Asynchronous evidence write

## Operational Behavior
- Hot path uses KMS data keys; cache DEKs with TTL
- Rotate keys without re‑encrypting via envelope scheme
- Verify signatures using public key resolver

## Constraints
- No raw plaintext persisted
- Keys never leave provider boundary
- Strong residency constraints

## Examples in Action
- Encrypt small payload → return ciphertext + keyref
- Verify signature for webhook callback

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
