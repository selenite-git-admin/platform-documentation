# Host App — Audit & Evidence

## Purpose
Explains how the Host App records, stores, and exports governance evidence.  
Audit and evidence are the backbone of defensibility during compliance reviews.

## Evidence Model
- **Actions Recorded** — drafts, reviews, approvals, publishes, tenant changes, RBAC assignments.  
- **Fields Captured** — who, what, when, why, and linkage to platform contract version ID.  
- **Immutability** — evidence entries cannot be modified or deleted.  

## Exports
- Export bundles include approvals, diffs, policy references, and linkage IDs.  
- Formats: JSON for machine use, PDF for auditors.  
- Exports can be tenant-scoped or org-wide.  

## Integration
- Linked to Schema/PHS contract versions for full lineage.  
- Evidence bundles attached to compliance workflows.  
- Accessible only to roles with export permissions (e.g., Auditor).  

## Why This Matters
Without immutable evidence, governance becomes unverifiable.  
Audit trails give regulators and auditors confidence that approvals and policies are consistently applied.
