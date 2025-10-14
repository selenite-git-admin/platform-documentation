
# UUID Standards (Identifiers)

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Define a single, platform-wide standard for identifiers. We use **UUIDv7** as the default primary key for application and data-layer entities. UUIDv7 preserves time ordering for write efficiency and still retains high entropy for safety.

## Why UUIDv7
- **Time-ordered:** better index locality and pagination than v4.
- **Collision-safe:** 122 bits of randomness similar to v4.
- **PostgreSQL-friendly:** stores natively in `uuid` with B-Tree support.
- **Zero engineering:** no central ID service, works in serverless and batch.

## Scope
Applies to: Catalog, DRR, SCD, Runtime, Delivery, Connectors, and Evidence Ledger event IDs.  
Excludes: third‑party systems that impose their own keys (store our UUID as `platform_id` alongside their key).

## Format
- Type: **UUIDv7** (RFC draft). String canonical form: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- Encodings for APIs: string. For storage: `uuid` column type.
- Do not base58/base64 encode in public APIs; keep canonical for clarity.

## Generation
### Recommended
Generate **in application code** using a vetted UUIDv7 library for your language. Examples:
- Python: `uuid6` or `uuid7` packages (`uuid7()`).
- Node: `uuid` package with v7 support (`v7()`).
- Go: `github.com/google/uuid` (v7) or `github.com/segmentio/ksuid` (only if v7 not available).

### Acceptable alternatives
- If v7 library unavailable, use **UUIDv4** temporarily and add `created_at` for sort order.
- Avoid Snowflake-style int IDs; they introduce clock skew and centralization risk.

### PostgreSQL notes
- Store as `uuid`. Default value is generated in app layer.  
- If DB-side generation is required, gate it behind a function provided by the application extension. Do **not** rely on custom pgcrypto patches in prod.

## Usage Patterns
- Primary keys: `id uuid primary key default gen in app`.
- Foreign keys: reference `uuid`. Always index FKs.
- Events: immutable `event_id uuid` generated at write time.
- Correlation: use `correlation_id uuid` for traceability across services.

## Example DDL
```sql
create table if not exists platform_event (
  event_id uuid primary key,
  source text not null,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create table if not exists catalog_dataset (
  id uuid primary key,
  dataset_id text unique not null,
  title text,
  created_at timestamptz not null default now()
);
```

## Indexing
- B-Tree on `uuid` is sufficient. UUIDv7 improves insertion locality.
- For very hot tables, use **partitioning by month** on `created_at` if needed.
- For range scans by time, index `(created_at, id)` to remove random seeks.

## API Contracts
- Request/response payloads use canonical UUID string.
- Validate format and reject anything not canonical to avoid implicit coercions.
- Log IDs in structured logs for traceability.

## Migration Guidance
- From integer IDs → add `id uuid` column, backfill, flip FK references, drop old PK.
- From v4 → continue to accept v4 in reads; generate v7 for new writes.
- Never reuse or recycle IDs.

## Observability
- Metric: `idgen.uuid.allocations` (counter).
- Metric: `idgen.uuid.collisions` (should remain 0).
- Percent of v7 vs v4 should trend to 100% v7.
- Log the `correlation_id` on all cross-service calls.

## Security & Privacy
- UUIDs are **not secrets**. Do not encode sensitive information in IDs.
- Avoid exposing sequential integers; prefer UUIDs in all public endpoints.
- Sanitize IDs in logs when combined with PII (tokenize or separate fields).

## Testing
- Property tests: uniqueness across 10M generations.
- Monotonicity windows: verify non-decreasing order for batches within 1 second.
- Round-trip encode/decode in all supported languages.

## FAQs
**Q: Why not ULID?**  
ULID is readable but can leak sort order predictably. UUIDv7 standardizes the same idea with better compatibility and no new type.

**Q: Do we need an ID service?**  
No. Libraries generate IDs locally. This fits serverless, containers, and batch.

**Q: Can we expose IDs to clients?**  
Yes. They are stable references. Do not use them as authorization tokens.

## Summary
UUIDv7 gives us ordered, collision‑resistant identifiers that work everywhere we run — Postgres, Lambda, and containers — without a central dependency. Adopt it by default for new tables and APIs, and migrate forward from v4/int when touching older modules.
