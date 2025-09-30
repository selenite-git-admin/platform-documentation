# Outbound Integration

## Purpose
Deliver metric outputs to destination systems in bulk.
Support same system tables, other systems, or object storage.

## Contract
Use Outbound contracts in Schema Services.
Reference the metrics contract as a dependency.

## Write semantics
Use insert, upsert, or merge as appropriate.
Require an idempotency key.

## Reconciliation
Compare counts and business totals.
Store a reconciliation report as evidence.

## SLOs
Track delivery timeliness and acceptance ratio.
