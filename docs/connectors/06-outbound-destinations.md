# Outbound Destinations

## Purpose
Write data to destination systems in bulk.

## Modes
- Database tables
- Batch files
- Batch APIs
- Streams

## Idempotency
Require an idempotency key in the outbound contract.
Prefer upsert or merge semantics.

## Reconciliation
Count delivered rows.
Compute checksums and business totals.

## Errors
Categorize errors and provide retry rules.
