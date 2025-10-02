# Roadmap

## Scope
Track documentation and engineering readiness for all modules.

## Dependency order
- Access Modules
- Security Modules
- Host Modules
- Data Utilities Modules
- Data Storage Modules
- Runtime Modules
- Compute Modules
- Consumption Modules
- Action Modules
- Trust Modules

## Checklists
Use these checkboxes to drive work. Each column is a page or track to complete.

| Module                     | Index | Data Model | API | Observability | Runbook | Security | Engineering Wiring |
|----------------------------|-------|------------|-----|---------------|---------|----------|--------------------|
| **Host Modules**           |       |            |     |               |         |          |                    |
| Policy Engine              | [x]   | [x]        | [x] | [x]           | [x]     | [x]      | [x]                |
| Data Contract Registry     | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Tenant Management          | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Lineage Obligations        | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Compute Modules**        |       |            |     |               |         |          |                    |
| Ingestion                  | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Normalization              | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| KPI Build                  | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Publish                    | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Orchestration              | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Data Storage Modules**   |       |            |     |               |         |          |                    |
| Raw Store                  | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| GDP Store                  | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| KPI Store                  | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Published Store            | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Calendar                   | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Consumption Modules**    |       |            |     |               |         |          |                    |
| Activation APIs            | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Exports                    | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Webhooks                   | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Catalog                    | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Action Modules**         |       |            |     |               |         |          |                    |
| Action Engine              | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Action Catalog             | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Action Delivery            | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Security Modules**       |       |            |     |               |         |          |                    |
| Gateway                    | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Network Security           | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Access Modules**         |       |            |     |               |         |          |                    |
| Authentication             | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Authorization              | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Subscription Enforcement   | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Trust Modules**          |       |            |     |               |         |          |                    |
| Evidence Ledger            | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Secrets                    | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Encryption                 | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Runtime Modules**        |       |            |     |               |         |          |                    |
| Scheduler                  | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Messaging and Events       | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Observability              | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Error Handling             | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Metering                   | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| **Data Utilities Modules** |       |            |     |               |         |          |                    |
| Schema Registry            | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Catalog and Discovery      | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |
| Migration Service          | [ ]   | [ ]        | [ ] | [ ]           | [ ]     | [ ]      | [ ]                |

## Development dependencies
- Complete Access and Security baselines before enabling external access.
- Establish Host and Utilities before Compute.
- Define Storage structures before KPI publish and consumption.
- Confirm Runtime capabilities before scheduling long-running jobs.
- Wire Observability signals before production rollout.
- Enforce [Dependency Guard](../references/dependency-guard.md) before enabling production deployments

## Notes
- Keep this roadmap synced with mkdocs.yml.
- Align terms with Glossary and Taxonomy.
- Date generated: 2025-10-02
