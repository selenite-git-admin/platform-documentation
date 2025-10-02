# Runtime Domain

## Purpose and scope
The Runtime Domain provides the execution backbone for the platform. It handles scheduling, orchestration, messaging and events, error handling, observability, and usage metering. Runtime does not define business contracts or store datasets; it ensures jobs, events, and operational signals run predictably and are observable.

## Boundaries
Owns: job scheduling, workflow orchestration, pub/sub delivery, retries and DLQs, metrics/logs/traces, health checks, usage metering.  
Does not own: business policy decisions (Host), identity and authorization (Access), encryption and evidence (Trust), long-term data storage (Data Storage).

## Modules
- **Scheduler Module** — Runs recurring and on-demand jobs with idempotency and backoff. [Read more](./scheduler/index.md)
- **Messaging and Events Module** — Queues and topics for inter-domain communication with replay controls. [Read more](./messaging-events/index.md)
- **Observability Module** — Structured logs, metrics, traces, health; read-only surfaces for Apps. [Read more](./observability/index.md)
- **Error Handling Module** — Normalized error taxonomy, retries, DLQ, compensation flows. [Read more](./error-handling/index.md)
- **Metering Module** — Tracks runtime usage for quotas and billing integration; exports auditable usage. [Read more](./metering/index.md)

## Context
All domains consume Runtime services. Compute relies on scheduling and events to run pipelines. Consumption and Action depend on reliable delivery. Observability feeds operators and Apps, while Metering emits usage for quota enforcement and external billing. Security and Access guard entry; Trust receives evidence from Runtime surfaces.
