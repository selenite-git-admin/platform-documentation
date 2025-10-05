# Data Utilities Modules

## Role in the platform
Data Utilities provide shared services that many modules read. They are designed for reuse, clear contracts, and steady performance. Writes are controlled and audited. Reads are cache friendly and stable.

## Modules
[Calendar Service](calendar-service/index.md)
Resolves time semantics for the platform. Provides calendars, tenant overlays, fiscal periods, and working time utilities. Links: [Data Model](calendar-service/data-model.md), [API](calendar-service/api.md), [UI](calendar-service/ui.md), [Observability](calendar-service/observability.md), [Runbook](calendar-service/runbook.md), [Security](calendar-service/security.md).

Schema Registry (planned)
Scope to be authored.

Catalog and Discovery (planned)
Scope to be authored.

Migration Service (planned)
Scope to be authored.

## Conventions
- Follow the module writing guide and the document writing guardrail used across the project
- Use the image modal pattern for diagrams
- Do not bold hyperlinks
- Be precise. Prefer examples over general statements
- Avoid speculative scope. Add only what is implemented or approved

## Add a new module here
Create a subfolder under `modules/data-utilities/<module-name>/` with these pages:
- index.md
- data-model.md
- api.md
- ui.md
- observability.md
- runbook.md
- security.md
