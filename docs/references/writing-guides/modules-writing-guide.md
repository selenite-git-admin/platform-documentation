# Module Writing Guide (Revised)

This guide defines how to write module documentation for BareCount Data Action Platform.  
It balances consistency with flexibility. Use the Core skeleton on every module page.  
Add Optional tracks only when the module warrants them.

## General rules

- Write in AWS-style narrative with select STE constraints.  
- Use present tense. Use active voice.  
- No em dashes. No horizontal rules.  
- Do not use bold in the middle of sentences.  
- Do not bold hyperlinks. Use plain links like [Policy Registry](policy-registry/index.md).  
- Modules are primary. User stories are secondary and illustrative.

## Core skeleton (always present)

### Role in the Platform
Explain what the module is and why it exists in the platform.  
One or two short paragraphs. Keep it factual and mechanical.

### Responsibilities
5 to 10 bullets.  
Each bullet starts with a controlled verb: configure, provision, validate, publish, record, enforce, authorize, authenticate, schedule, route, monitor, retry, rollback, export.

### Inputs
List what the module consumes.  
Data, configs, events, requests.

### Outputs
List what the module produces.  
Decisions, artifacts, state changes, notifications.

### Interfaces
APIs, schemas, tables, files, message topics.  
Name them when known. Describe type when unknown.

### Operational Behavior
Scheduling, retries, idempotency, concurrency, failure modes.  
Observability signals: logs, metrics, alerts.

### Constraints
What the module does not own.  
Dependencies on other modules.  
Limits and prerequisites.

### Related User Stories
Link to specific user stories as examples only.

### Examples in Action
One or two short scenarios that show the module at work.  
Trigger, module action, result.

## Optional tracks (add when useful)

### Data Model
Include when the module persists state or emits durable artifacts.
- ERD
- DBML
- DDL and migrations
- Seed data for local development

### API and Contracts
Include when the module has a public or internal surface.
- Endpoints and verbs or RPCs
- Request and response schemas
- Error model, idempotency, pagination

### Observability
Include when operators will monitor or tune the module.
- Metrics and units
- Log events and fields
- Traces
- Alerts and thresholds
- SLOs

### Security and Access
Include when the module touches identity, data classification, or secrets.
- AuthN and AuthZ expectations
- Data classes and handling notes
- Privacy and retention

### Runbook
Include when the module has operational risk or recovery paths.
- Failure modes and symptoms
- Recovery procedures
- Backfill and rollback
- Hotfix guidance

## Decision rubric per module

Use these questions before adding any Optional track.

- Does this module persist state or publish artifacts  
  If yes, include Data Model.
- Does this module expose an API or formal contract  
  If yes, include API and Contracts.
- Will SREs or operators monitor this module directly  
  If yes, include Observability and consider SLOs.
- Does this module interact with identity or sensitive data  
  If yes, include Security and Access.
- Could on-call engineers need guided recovery steps  
  If yes, include Runbook.

## Authoring checklist

- Role in the Platform is present and specific to this module.  
- Responsibilities use controlled verbs and describe mechanics.  
- Inputs and Outputs are concrete and testable.  
- Interfaces identify names or types.  
- Operational Behavior states how it runs and how it fails.  
- Constraints prevent scope creep into other modules.  
- Examples in Action are short and realistic.  
- Optional tracks are added only when the rubric says yes.  
- Links align with MkDocs nav.  
- Terminology matches Glossary and Taxonomy.

## Example: applying the rubric

Module persists policy objects and records evaluations  
Include Data Model.

Module offers to evaluate and list endpoints  
Include API and Contracts.

Module decisions are audited and alerted on  
Include Observability.

Module does not own identity  
Exclude Security and Access, but state that constraint.

Module may block workflows in production  
Include Runbook for common deny and rollback paths.
