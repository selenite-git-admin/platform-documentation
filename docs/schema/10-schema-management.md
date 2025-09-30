# Schema Management

## Purpose
Control schema change across environments.
Protect data quality, cost, and reliability.
Provide audit evidence for decisions.

## States
- Draft
- Proposed
- Approved
- Seeded
- Active
- Deprecated
- Retired

## Transitions
Require reviews for Proposed to Approved.
Seed data or create empty targets for Seeded.
Activate only after validation passes.
Deprecate with a plan for readers.
Retire after data migration or archival.

## Requests and Approvals
Use a change request for new or changed contracts.
Record risk, impact, and rollback plan.
Assign owners and reviewers.

## Versioning
Use SemVer.
Increase major when breaking changes occur.
Increase minor for additive compatible changes.
Increase patch for fixes.

## Backward Compatibility
Prefer additive changes.
Avoid destructive changes.
Use compatibility views during transitions.

## Rollback
Record a clear rollback plan.
Keep prior DDL and data snapshots when possible.
Automate rollback for small changes.

## Evidence and Retention
Store validation reports, approval decisions, and deployment logs.
Retain evidence to meet compliance goals.
Link evidence to lineage.
