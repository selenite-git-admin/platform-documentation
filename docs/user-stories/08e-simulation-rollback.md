# Simulation and Rollback

> Goal: Test workflows safely and recover from issues without business impact.  
> Scope: Covers dry run, what-if simulation, and controlled rollback.

## Context
Simulation allows teams to understand outcomes before execution. Rollback ensures that if something goes wrong, the system can recover quickly with minimal disruption.

## Actors (Personas and Roles)
- Workflow Author: prepares simulation scenarios  
- Platform Admin: runs simulations and validates results  
- Business Owner: reviews what-if outcomes  
- Observability Engineer: checks rollback readiness

## Preconditions
- Workflow configured and executable  
- Simulation mode available  
- Rollback hooks defined

## Scenario Flow
1. Platform Admin runs a dry run and reviews what-if results  
2. Business Owner approves live run if outcomes are acceptable  
3. If executed and issues arise, rollback is invoked  
4. Post-rollback verification is performed

## Acceptance Criteria
- Simulation results recorded  
- Rollback restores system to last known good state  
- Evidence available

## Failure Paths
- Simulation mismatch: outcomes differ from live run, review required  
- Rollback failure: escalate to incident response  
- Missing hooks: rollback blocked and fixed

## Observability and Governance
- Audit Events: workflow.simulated, workflow.rolled_back  
- Metrics: simulation_coverage_rate, rollback_time_seconds  
- Evidence: simulation reports and rollback logs

## Interfaces and Cross Links
- Previous: [Workflow Execution Engine](08d-workflow-execution-engine.md)  
- Next: [Workflow Observability and Receipts](08f-workflow-observability-receipts.md)

## Configuration Examples

**Simulation Report (YAML)**
```yaml
workflow_id: WF-DELAY-VENDOR-PAYMENTS-ACME
scenarios:
  - name: mild_breach
    expected_actions: 1
  - name: severe_breach
    expected_actions: 2
status: reviewed
```

## BDD Scenarios

### Scenario: Dry run approved then executed
```gherkin
Given a workflow is configured
When a dry run is executed
Then results are reviewed and approved
And the workflow is allowed to proceed to live execution
```

## Review Checklist
- [x] Simulation run recorded  
- [x] Rollback tested  
- [x] Evidence available  
