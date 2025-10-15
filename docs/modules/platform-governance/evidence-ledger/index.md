# Evidence Ledger

## Role in the Platform
Provides an append‑only, hash‑chained log of decisions and security events. Enables verification of integrity and export for audits.

<a href="#fig-evidence-ledger-sequence" class="image-link">
  <img src="/assets/diagrams/trust/evidence-ledger-sequence.svg" alt="Evidence Ledger sequence diagram">
</a>
<div id="fig-evidence-ledger-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/trust/evidence-ledger-sequence.svg" alt="Evidence Ledger sequence diagram">
</div>
_Figure: Evidence Ledger sequence_{.figure-caption}

## Responsibilities
- Append evidence records with hashes
- Verify chain integrity
- Export and search events

## Inputs
- Decision events from modules
- Hashing and time‑stamping service
- Tenant metadata

## Outputs
- Evidence records and verification proofs
- Export bundles for audits
- Metrics and traces

## Interfaces
- Append API for writes
- Verify API for on‑demand checks
- Export API for auditors

## Operational Behavior
- Write events synchronously; queue export tasks asynchronously
- Verify on demand or scheduled
- Shard by time for scale

## Constraints
- No edits or deletes
- Strict ordering within shard
- Backpressure on overload

## Examples in Action
- Module writes decision → ledger returns evidence_id
- Auditor verifies range and exports bundle

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
