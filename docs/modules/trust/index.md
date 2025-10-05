# Trust Domain

## Role in the Platform
The Trust domain provides cryptographic foundations and verifiable evidence for the platform. It includes services for key management and encryption, secret storage and distribution, and a tamper‑evident evidence ledger. The domain enforces confidentiality, integrity, and non‑repudiation for tenant and system actions.

## Submodules
- [Encryption](encryption/index.md) — key management, encryption at rest and in transit, envelope encryption with KMS.  
- [Secrets](secrets/index.md) — secure storage, rotation, and scoped distribution of secrets.  
- [Evidence Ledger](evidence-ledger/index.md) — immutable, hash‑chained decision and control records for audits.

## Position in the Platform
- Upstream from Access: signs tokens and validates signatures.  
- Cross‑cuts Storage and Runtime: encrypts data, rotates keys, and exposes cryptographic primitives.  
- Downstream from all modules: records evidence for governance, security, and compliance audits.

## Interfaces
- Public/tenant‑facing endpoints in Secrets for retrieval of scoped client credentials.  
- Admin APIs in Encryption for key alias management and rotation policies.  
- Append‑only API in Evidence Ledger for decision records with verification endpoints.

## Constraints
- Trust does not own business policy. It enforces cryptographic controls and records evidence.  
- All submodules avoid storing raw PII; only references and hashes are recorded where required.

## Related
- [Security Baseline](/modules/security/index.md)  
- [Access Domain](/modules/access/index.md)  
- [Storage Domain](/modules/storage/index.md)
