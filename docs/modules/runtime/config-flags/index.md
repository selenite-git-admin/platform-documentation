# Config & Flags

## Role in the Platform
Runtime configuration and feature flags with gradual rollouts and kill switches. Supports per‑tenant, per‑region targeting.

<a href="#fig-config-flags-sequence" class="image-link">
  <img src="/assets/diagrams/runtime/config-flags-sequence.svg" alt="Config & Flags sequence diagram">
</a>
<div id="fig-config-flags-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/runtime/config-flags-sequence.svg" alt="Config & Flags sequence diagram">
</div>
_Figure: Config & Flags sequence_{.figure-caption}

## Responsibilities
- Manage flags and configs
- Roll out gradually with percentages and rules
- Evaluate flags at runtime with low latency
- Record evaluations for audits

## Inputs
- Targeting rules
- Segments and attributes
- Environment metadata

## Outputs
- Resolved configs and flag decisions
- Evaluation events
- Metrics and traces

## Interfaces
- Flags API for CRUD
- Evaluate API for SDKs
- Segments API

## Operational Behavior
- Edge‑cached configs for <5ms eval
- Sticky bucketing per subject
- Global killswitch respected by SDKs

## Constraints
- No remote code in rules
- No PII in attributes
- No unreviewed global rules

## Examples in Action
- Enable feature for 10% in region=IN
- Kill switch activated to mitigate incident

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
