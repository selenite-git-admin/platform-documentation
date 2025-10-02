# Best Practices

## Code
- Keep modules small and focused.
- Use names that match documentation.
- Prefer composition over inheritance.

## Docs
- Update module docs in the same pull request as code changes.
- Use short sentences and active voice.
- Link to exact files and APIs.

## Interfaces
- Treat schemas and APIs as contracts.
- Version deliberately.
- Add contract tests to CI.
- Enforce dependency order with [Dependency Guard](../references/dependency-guard.md)


## Data
- Use migrations for every schema change.
- Keep seed data small and relevant.
- Make backfill scripts idempotent.

## Testing
- Unit tests for logic.
- Integration tests for boundaries.
- Contract tests for APIs and schemas.
- End to end tests for core flows.

## Observability
- Emit structured logs with identifiers.
- Expose metrics with clear units.
- Add alerts for user-facing failures.

## Security
- Enforce least privilege for services.
- Do not embed secrets in code or docs.
- Classify data and apply retention rules.
