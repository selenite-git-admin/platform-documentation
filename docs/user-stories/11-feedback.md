# Feedback

> Goal: Capture feedback and convert it into improvements.  
> Scope: Covers feedback collection, triage, prioritization, and closure loop.

## Context
Users provide insights that drive product and operational improvement. A structured feedback loop turns raw comments into prioritized work with measurable outcomes.

## Actors (Personas and Roles)
- Tenant Admin or User: submits feedback
- Product Owner: triages and prioritizes
- Platform Admin: implements changes or files tickets
- Compliance Officer: reviews compliance-related suggestions

## Preconditions
- Feedback channels available
- Triage rubric defined
- Backlog and tracking system in place

## Scenario Flow
1. User submits feedback via in app widget or portal
2. Product Owner triages and categorizes feedback
3. Priority set and item moved to backlog
4. Platform Admin implements change or files ticket
5. User notified of resolution and closure

## Acceptance Criteria
- Feedback captured with identity and context
- Triage and priority recorded
- Closure status communicated to the submitter

## Failure Paths
- Duplicate feedback: deduplicate and merge contexts
- Missing context: request more information
- No closure: item stalls and triggers reminder

## Observability and Governance
- Audit Events: feedback.submitted, feedback.triaged, feedback.closed
- Metrics: feedback_to_ticket_rate, time_to_close_feedback
- Evidence: feedback record and closure notes

## Interfaces and Cross Links
- Previous: [Incident Handling](10b-incident-handling.md)

## Configuration Examples

**Feedback Record (JSON)**
```json
{
  "feedback_id": "FB-2025-09-29-001",
  "submitted_by": "tenant_admin@acme.com",
  "category": "usability",
  "priority": "P2",
  "status": "CLOSED"
}
```

## BDD Scenarios

### Scenario: Feedback triaged and closed
```gherkin
Given a user submits feedback
When the Product Owner triages and prioritizes it
Then the item is added to the backlog
And the user is notified on closure
```

### Scenario: Feedback needs more information
```gherkin
Given a user submits feedback
When the description is insufficient
Then the system requests more information
And the item remains pending until updated
```

## Review Checklist
- [x] Feedback captured
- [x] Prioritized and tracked
- [x] Closure communicated
