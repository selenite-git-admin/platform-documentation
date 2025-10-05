# Lifecycle: Publishing & Propagation

## Flow
1. Writer submits version → **validate** → **store** as immutable.
2. Emit **receipt** and **event**.
3. **Catalog** upsert item & relations.
4. **Delivery** cache invalidate for endpoints/dashboards.
5. **Pipelines** re-materialize if necessary (flags driven).

## Cache Semantics
- Delivery uses **signed cursors**; schema-affecting changes increment resource etag.
- Dashboards render with **expiring links**; schema diffs shown to operators.

## Parallel Publish
For subject branching (`*.v2`), both v1 & v2 publish until consumers migrate. Receipts record cutover.
