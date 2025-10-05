# Streaming Bus

## Role in the Platform
Durable event backbone with topics, partitions, retention, and DLQs. Supports exactly‑once semantics for critical streams.

<a href="#fig-streaming-bus-sequence" class="image-link">
  <img src="/assets/diagrams/runtime/streaming-bus-sequence.svg" alt="Streaming Bus sequence diagram">
</a>
<div id="fig-streaming-bus-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/runtime/streaming-bus-sequence.svg" alt="Streaming Bus sequence diagram">
</div>
_Figure: Streaming Bus sequence_{.figure-caption}

## Responsibilities
- Provision topics and partitions
- Publish/subscribe with ordering per key
- Manage consumer groups and offsets
- Provide DLQ and replay
- Enforce schemas and compatibility

## Inputs
- Producer/consumer clients
- Schema registry
- Security policies

## Outputs
- Messages and offsets
- DLQ entries
- Metrics and traces

## Interfaces
- Topic API for provision
- Publish API (internal)
- Consumer group API
- Replay API

## Operational Behavior
- Idempotent producers with keys
- Compaction for state topics
- Replay with watermark control

## Constraints
- No unkeyed high‑volume topics
- No long‑lived consumer lag without alerts
- No schema breaking changes

## Examples in Action
- Replay orders topic from watermark T‑1h
- Provision topic with 24h retention and 8 partitions

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
