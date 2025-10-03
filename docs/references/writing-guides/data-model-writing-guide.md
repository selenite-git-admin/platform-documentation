# Data Model Writing Guide

## Scope
Define how to document persistent data for a module. Use this guide when a module stores state or publishes durable artifacts.

## Structure
1. Scope
2. Conventions
3. Entities
4. ERD
5. DBML
6. DDL skeletons
7. Validation queries
8. Migration notes
9. Seeds for local development (optional)

## Conventions
- Database: state the target engine. Default is PostgreSQL
- Naming: snake_case for columns, plural table names where appropriate
- Keys: `uuid` primary keys unless a natural key is better and stable
- Time: UTC. Use `timestamptz` in DDL and `datetime` in DBML
- JSON: prefer `jsonb` in PostgreSQL
- Constraints: declare `not null`, `check`, and `unique` where they protect invariants
- Indexes: list the hot queries and add only measured indexes
- Foreign keys: add explicit `Ref:` lines in DBML
- Comments: avoid inline `//` in DBML. Use Notes under sections if needed

## Entities
Describe each table as a short paragraph. List purpose, key fields, and relationships in plain language.

## ERD
Embed the diagram using the standard modal pattern. Use an absolute path under `/assets/diagrams/<module>/<name>.svg`.

## DBML
- Use `datetime` type and newline entries in `Indexes { }`
- Add `Ref:` lines for relationships
- Keep one table per block. No trailing commas

## DDL skeletons
Show portable SQL. Use `check` constraints for enumerations. Include essential indexes only.

## Validation queries
Provide 2 to 5 queries that verify correctness from an operator’s perspective.

## Migration notes
Explain safe change patterns. Prefer additive steps. Capture backfill approaches and rollback triggers.

## Seeds (optional)
Provide small seed sets for local development. Keep them deterministic and documented.
