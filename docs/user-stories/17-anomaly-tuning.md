# Anomaly Threshold Tuning

> Goal: Adjust and optimize anomaly detection thresholds to balance sensitivity and noise.  
> Scope: Covers threshold definition, simulation, tuning, approval, and evidence.

## Context
Anomaly detection is only effective if thresholds are tuned correctly. Too strict and the system generates noise, too lenient and important anomalies are missed. Threshold tuning provides a controlled process to calibrate detection rules while maintaining auditability.

## Actors (Personas and Roles)
- Anomaly Engineer: defines and adjusts thresholds
- Business Owner: reviews business impact and approves changes
- Compliance Officer: ensures tuning changes are logged and compliant
- Observability Engineer: validates effectiveness through metrics

## Preconditions
- Anomaly engine integrated and active
- Historical data available for simulation
- Governance policy defined for tuning changes

## Scenario Flow
1. Anomaly Engineer proposes threshold adjustment based on historical data
2. Simulation runs to show expected detection rates
3. Business Owner reviews business impact of proposed changes
4. Compliance Officer validates that governance rules are followed
5. New threshold deployed and monitoring enabled
6. Effectiveness metrics captured and logged

## Acceptance Criteria
- Threshold adjustments justified with historical evidence
- Business impact reviewed and approved
- Compliance validation recorded
- Post-deployment effectiveness metrics available

## Failure Paths
- Simulation indicates high false positive rate: adjustment rejected
- Approval missing: deployment blocked
- Metrics gap: effectiveness cannot be validated

## Observability and Governance
- Audit Events: anomaly.threshold.proposed, anomaly.threshold.approved, anomaly.threshold.deployed
- Metrics: false_positive_rate, false_negative_rate, detection_latency
- Evidence: tuning proposal, simulation report, approval record

## Interfaces and Cross Links
- Previous: [Anomaly Engine Integration](16-anomaly-engine.md)

## Configuration Examples

**Threshold Config (YAML)**
```yaml
anomaly_id: DSO
old_threshold: 45
proposed_threshold: 50
simulated_false_positive_rate: 2.5
simulated_false_negative_rate: 1.2
status: approved
```

## BDD Scenarios

### Scenario: Threshold tuning approved and deployed
```gherkin
Given historical data is available
When an Anomaly Engineer proposes a new threshold
And the Business Owner approves it
And the Compliance Officer validates governance
Then the threshold is deployed
And effectiveness metrics are recorded
```

### Scenario: Threshold tuning rejected due to high false positives
```gherkin
Given historical data is available
When an Anomaly Engineer proposes a new threshold
And simulation shows high false positive rate
Then the proposal is rejected
And feedback is recorded
```

## Review Checklist
- [x] Proposal created and justified
- [x] Simulation run and reviewed
- [x] Business Owner approval recorded
- [x] Compliance validation captured
- [x] Effectiveness metrics logged
