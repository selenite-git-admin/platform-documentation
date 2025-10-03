# Roadmap

## Checklist
**Documentation Status**  
✅ = Ready  
⚪ = Pending  

| Module                     | Index | Data Model | UI | API | Observability | Runbook | Security |
|----------------------------|-------|------------|----|-----|---------------|---------|----------|
| **Host Modules**           |       |            |    |     |               |         |          |
| Tenant Management          | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| Platform Catalog           | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| **Governance Modules**     |       |            |    |     |               |         |          |
| Policy Registry            | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| Data Contract Registry     | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| Lineage Obligations        | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| **Compute Modules**        |       |            |    |     |               |         |          |
| Ingestion                  | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Normalization              | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| KPI Build                  | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Publish                    | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Orchestration              | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Data Storage Modules**   |       |            |    |     |               |         |          |
| Raw Store                  | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| GDP Store                  | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| KPI Store                  | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Published Store            | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Consumption Modules**    |       |            |    |     |               |         |          |
| Activation APIs            | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Exports                    | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Webhooks                   | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Catalog                    | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Action Modules**         |       |            |    |     |               |         |          |
| Action Engine              | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Action Catalog             | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Action Delivery            | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Security Modules**       |       |            |    |     |               |         |          |
| Gateway                    | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Network Security           | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Access Modules**         |       |            |    |     |               |         |          |
| Authentication             | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Authorization              | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Subscription Enforcement   | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Trust Modules**          |       |            |    |     |               |         |          |
| Evidence Ledger            | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Secrets                    | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Encryption                 | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Runtime Modules**        |       |            |    |     |               |         |          |
| Scheduler                  | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Messaging and Events       | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Observability              | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Error Handling             | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Metering                   | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| **Data Utilities Modules** |       |            |    |     |               |         |          |
| Calendar Service           | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| Schema Registry            | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Catalog and Discovery      | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Data Observability         | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Migration Service          | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |

## Notes
- This page is updated as modules progress. Date generated: 2025-10-03
- Keep the module list in sync with `mkdocs.yml` under **Modules**
- For dependency policy see [Dependency Guard](../references/dependency-guard.md)
