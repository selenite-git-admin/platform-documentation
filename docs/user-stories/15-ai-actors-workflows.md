# AI Actors in Workflows

> Goal: Enable AI actors to participate in workflows.  
> Scope: Covers AI-driven triggers, approvals, actions, and oversight.

## Context
AI systems can act as assistants in workflows, providing recommendations, approvals, or anomaly detection. Their role must remain governed with human oversight and clear evidence trails.

## Actors (Personas and Roles)
- AI Actor: provides recommendations or executes bounded actions
- Workflow Author: defines AI role in workflows
- Business Owner: oversees AI decisions and confirms outcomes
- Compliance Officer: validates AI behavior and evidence

## Preconditions
- AI models integrated with platform
- Guardrails defined for AI actors
- Oversight rules documented

## Scenario Flow
1. Workflow Author configures AI actor in a workflow
2. AI actor evaluates KPI or anomaly signals
3. AI actor recommends or executes bounded action
4. Business Owner reviews AI outcomes
5. Evidence recorded and validated by Compliance Officer

## Acceptance Criteria
- AI actor bounded by guardrails
- Human oversight in place
- Evidence available

## Failure Paths
- AI actor recommendation outside bounds: blocked
- Missing oversight: AI action not executed
- Evidence gap: compliance failure

## Observability and Governance
- Audit Events: ai.actor.configured, ai.actor.executed, ai.actor.evidence.recorded
- Metrics: ai_action_count, ai_recommendation_accuracy
- Evidence: AI logs and receipts

## Interfaces and Cross Links
- Previous: [Hybrid Deployment](14-hybrid-deployment.md)
- Next: [Anomaly Engine Integration](16-anomaly-engine.md)

## Configuration Examples

**AI Actor Config (YAML)**
```yaml
workflow_id: WF-DELAY-VENDOR-PAYMENTS-ACME
ai_actor:
  role: recommender
  scope: vendor_payment_hold
  guardrails: policy_budget_limits
status: active
```

## BDD Scenarios

### Scenario: AI actor recommendation accepted
```gherkin
Given an AI actor is configured
When the AI actor recommends an action within bounds
Then the action is executed
And evidence is recorded
```

### Scenario: AI actor recommendation blocked due to guardrails
```gherkin
Given an AI actor is configured
When the AI actor recommends an out of bounds action
Then the action is blocked
And an alert is raised
```

## Review Checklist
- [x] AI actor bounded
- [x] Human oversight ensured
- [x] Evidence recorded
