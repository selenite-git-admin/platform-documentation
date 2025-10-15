# Streaming Bus – Security

## Scope
Security posture for streaming bus operations.

## Data Protection
- TLS 1.3, mTLS for internal calls, signed artifacts, image provenance checks.

## Access Control
- Least privilege; per‑tenant and per‑job scopes; admission control for workloads.

## Auditability
- Record job submissions, schedule changes, and execution outcomes with evidence ids.

## Notes
- Producer/consumer auth via mTLS
- ACLs per topic/group
- Schema enforcement on write
