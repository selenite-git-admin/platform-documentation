# Access Domain

## Purpose and scope
The Access Domain governs identity and permissions inside the platform. It authenticates users and services and enforces authorization rules for every call. It also applies subscription entitlements so only permitted operations proceed.

## Boundaries
Owns: authentication, authorization/RBAC, entitlement checks tied to subscription state.  
Does not own: perimeter controls and rate limits (Security), encryption and evidence (Trust), job execution and observability (Runtime), data storage (Data Storage).

## Modules
- **Authentication Module** — Validates identities via SSO or tokens and issues scoped credentials. [Read more](./authentication/index.md)
- **Authorization Module** — Evaluates roles and entitlements for fine-grained access decisions. [Read more](./authorization/index.md)
- **Subscription Enforcement Module** — Enforces plan limits and entitlements at request time. [Read more](./subscription-enforcement/index.md)

## Context
All requests pass through Security’s Gateway, then Access authenticates and authorizes them. Subscription Enforcement checks tenant plan limits before calls reach domain modules. Decisions and reasons are logged and, where required, exported as evidence to Trust.
