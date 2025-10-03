# Roadmap

## Scope
Track documentation readiness across modules. Columns are split into **Basic** and **Optional**.

## Columns
Basic
- Index: module overview with role, responsibilities, inputs, outputs, interfaces, operational behavior, constraints, related user stories, and examples

Optional
- Data Model: ERD, DBML, DDL, seeds
- API: endpoints, schemas, error model, idempotency, rate limits
- UI: screens, placement (Platform Admin App or Tenant App), API dependencies, wireframes
- Observability: metrics, logs, traces, dashboards, alerts, SLOs
- Runbook: operational procedures for incidents and routine tasks
- Security: data classification, access control, auditability, safeguards
- Engineering Wiring: CI hooks, starter kits, scripts, or automation specific to the module

## Checklist
Use these emojis to track status. ✅ = ready, ⚪ = pending.

| Module                     | Index | Data Model | UI | API | Observability | Runbook | Security |
|----------------------------|-------|------------|----|-----|---------------|---------|----------|
| **Host Modules**           |       |            |    |     |               |         |          |
| Policy Registry            | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| Data Contract Registry     | ✅     | ✅          | ✅  | ✅   | ✅             | ✅       | ✅        |
| Tenant Management          | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Lineage Obligations        | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
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
| Calendar                   | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
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
| Schema Registry            | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Catalog and Discovery      | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Data Observability         | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |
| Migration Service          | ⚪     | ⚪          | ⚪  | ⚪   | ⚪             | ⚪       | ⚪        |

## Notes
- This page is updated as modules progress. Date generated: 2025-10-02
- Keep the module list in sync with `mkdocs.yml` under **Modules**
- For dependency policy see [Dependency Guard](../references/dependency-guard.md)
