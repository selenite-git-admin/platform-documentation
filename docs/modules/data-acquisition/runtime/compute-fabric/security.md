# Compute Fabric – Security

## Scope
Security posture for compute fabric operations.

## Data Protection
- TLS 1.3, mTLS for internal calls, signed artifacts, image provenance checks.

## Access Control
- Least privilege; per‑tenant and per‑job scopes; admission control for workloads.

## Auditability
- Record job submissions, schedule changes, and execution outcomes with evidence ids.

## Notes
- Admission control verifies signatures
- Seccomp/AppArmor profiles enforced
- Rootless containers by default
