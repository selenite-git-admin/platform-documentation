# CI/CD

## Scope
Define pipelines that build, test, scan, and release components.

## Stages
- Source checkout
- Static checks
- Build and unit tests
- Integration and contract tests
- Package and publish artifacts
- Deploy to environments
- Post-deploy checks

## Gates
- Docs and code must match for schema, APIs, and interfaces.
- DDL and DBML in docs must match migrations.
- API schemas in docs must match OpenAPI in the repo.

## Required checks
- Lint and static analysis
- Unit test pass
- Contract test pass against documented interfaces
- Coverage threshold
- Vulnerability scan pass
- Policy checks for protected branches
- [Dependency Guard](../references/dependency-guard.md) passes for families and modules


## Promotions
- Dev to staging with automated verification
- Staging to prod with manual approval and change record
- Rollback plan stored with each release

## Artifacts
- Container images
- Migrations
- OpenAPI specs
- Release notes linked to module docs
