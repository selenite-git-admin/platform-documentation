# Flow: Network Connectivity

## Purpose
Describe how network routes are enforced for connector runs.

## Actors
- Orchestrator
- Runner
- Network control plane

## Steps
1. Orchestrator reads network pattern from the connection profile. 
2. Orchestrator selects the correct subnets, security groups, and endpoints for the runner. 
3. Runner executes inside the assigned network boundaries. 
4. Egress is routed through VPN, PrivateLink, VPC endpoints, or NAT allowlists as configured. 
5. Network telemetry is recorded for audits.

## Inputs
- Connection profile
- Runner profile

## Outputs
- Enforced network path
- Network telemetry

## Observability
- Flow logs
- Endpoint metrics
