# Compute Fabric

## Role in the Platform
Isolated execution of containerized and function tasks with quotas, scheduling, and autoscaling. Provides secure sandboxes and resource accounting.

<a href="#fig-compute-fabric-sequence" class="image-link">
  <img src="/assets/diagrams/runtime/compute-fabric-sequence.svg" alt="Compute Fabric sequence diagram">
</a>
<div id="fig-compute-fabric-sequence" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/runtime/compute-fabric-sequence.svg" alt="Compute Fabric sequence diagram">
</div>
_Figure: Compute Fabric sequence_{.figure-caption}

## Responsibilities
- Run containers/functions with resource limits
- Provide sandboxes with network and secret policies
- Autoscale based on queue depth and metrics
- Expose job logs and artifacts
- Support GPU/accelerator pools where available

## Inputs
- Images/artifacts signed by CI
- Secrets leases from Trust→Secrets
- Network policies from Security
- Jobs from Orchestrator

## Outputs
- Execution results and artifacts
- Logs and traces
- Resource utilization metrics

## Interfaces
- Execution API for submit/stop
- Logs API for streaming
- Admin API for pools and quotas

## Operational Behavior
- Bin‑packing with fairness across tenants
- Pre‑warm pools for low latency
- Evict noisy neighbors by policy

## Constraints
- No unsigned images
- No outbound network without policy
- No shared writable volumes across tenants

## Examples in Action
- Submit container job with CPU=2, MEM=4Gi; get logs and exit code
- Run function with 500ms limit and cold‑start budget

## Related Links
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Runbook](runbook.md)
- [Security](security.md)
- [UI](ui.md)
