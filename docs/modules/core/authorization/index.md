# Authorization

## Role in the Platform
Authorize requests using RBAC/ABAC.

## Responsibilities
- Evaluate permissions
- Resource‑scoped grants
- RLS/CLS enforcement

## Inputs
- Subject claims
- Resource descriptor
- Policy rules

## Outputs
- Decision
- Evidence

## Lifecycle
Request → evaluate → decision → log

## Decisions
- permit
- deny
- require-approval
- warn
