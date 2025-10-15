# Raw Store

## Role in the Platform
Durable, immutable landing zone for external feeds. Stores raw bytes with metadata and retention policies.

<a href="#fig-raw-store-sequence" class="image-link">
  <img src="/assets/diagrams/storage/raw-store-sequence.svg" alt="Raw Store sequence diagram">
</a>
<div id="fig-raw-store-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/storage/raw-store-sequence.svg" alt="Raw Store sequence diagram">
</div>
_Figure: Raw Store sequence_{.figure-caption}

## Responsibilities
- Accept batch and streaming ingests
- Validate and register metadata
- Partition and tier data
- Expose lineage to GDP jobs

## Inputs
- External connectors
- Ingest API events
- Schema hints

## Outputs
- Registered objects and metadata
- Ingest receipts
- Lineage links

## Interfaces
- Ingest API (batch/stream)
- Metadata registry
- Lineage API

## Operational Behavior
- Write-once, read-many with immutability
- Content-addressed storage for dedupe
- Tiering between hot/cold/object

## Constraints
- No destructive updates
- No PII without classification
- Retention enforced by policy

## Examples in Action
- Batch file landed with checksum
- Stream partition rollover at size/time

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
