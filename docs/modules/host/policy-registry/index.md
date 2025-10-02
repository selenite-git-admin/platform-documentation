# Policy Registry

## Role in the Platform
Policy Registry defines and enforces guardrails across the BareCount Data Action Platform.
It stores policy definitions, evaluates them during schema lifecycle events, workflow execution, and tenant lifecycle actions, and produces decisions that downstream modules must respect.
By centralizing policies, it prevents uncontrolled changes and provides evidence for audits and regulatory exports.

## Responsibilities
- Store and version platform policies
- Enforce guardrails on schema lifecycle changes
- Evaluate workflow execution requests before they proceed
- Gate tenant provisioning and offboarding with required checks
- Produce decisions: allow, deny, require approval, or warn
- Record decisions with policy version reference
- Provide evidence records for audit and regulator exports

## Inputs
- Policy definitions created by administrators
- Schema change proposals from raw, GDP, and KPI lifecycle steps
- Workflow execution events such as triggers and approvals
- Tenant lifecycle intents such as provisioning or offboarding

## Outputs
- Decision result: allow, deny, require approval, warn
- Reference to policy version used during evaluation
- Evidence record for lineage and audit functions

## Interfaces
- Reads and writes policy objects in the registry store
- Consumes schema proposals from Data Contract Registry
- Interacts with workflow execution to gate actions
- Provides evidence artifacts to Lineage Obligations and Evidence Export

## Operational Behavior
- Evaluates policies synchronously when invoked by workflows or schema changes
- Records every decision for observability and audits
- Supports rollback by re-evaluating policies against prior versions
- Surfaces alerts if mandatory policies are missing or invalid

## Constraints
- Does not manage schema definitions directly (owned by Data Contract Registry)
- Does not perform identity or entitlement checks (handled by Access Modules)
- Does not run jobs or schedule tasks (Runtime Modules handle execution)
- Relies on other modules to act on its decisions

## Related User Stories
- Setting Up Guardrails
- Safe Rollout and Rollback
- Workflow Triggers and Approvals
- Evidence Export for Regulators

## Examples in Action

Schema change check
A team proposes a new KPI schema.
Policy Registry retrieves the relevant policy, validates the schema, and produces a decision: `deny` because required fiscal period fields are missing.
The change request is blocked, and an audit record is created.

Workflow trigger check
A workflow execution request includes a financial data export.
Policy Registry evaluates the policy requiring approval for exports.
It produces a decision: `require approval`.
The workflow pauses until an authorized approver validates the action.

## Module Documentation

[Data Model](data-model.md)
Database design, ERD, DBML, DDL, and migration details.

[API](api.md)
Endpoints, request and response schemas, and error handling.

[Observability](observability.md)
Metrics, logs, traces, and alerts for monitoring.

[Runbook](runbook.md)
Operational procedures, failure modes, and recovery steps.

[Security](security.md)
Access controls, retention rules, and data classification notes.
