# Data Model

## `catalog_item`
- `id` (ulid)
- `type` enum `dataset|kpi|dashboard`
- `slug` (string, unique)
- `name` (string)
- `owner` (string)
- `tags` (json array)
- `links` (json) — storage/delivery/lineage refs
- `created_at`, `updated_at`

## `signal`
- `id` (ulid)
- `slug` (string, fk to `catalog_item.slug`)
- `freshness_ms` (int)
- `quality_score` (int 0..100)
- `usage_7d` (int)
- `produced_at` (timestamp)
