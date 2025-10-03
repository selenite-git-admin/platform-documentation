# Flow: Incremental Run Lifecycle

## Purpose
Describe how an incremental run executes with stateless connectors and a central state registry.

## Actors
- Orchestrator
- Connector
- State registry
- Bronze sink

## Steps
1. Orchestrator reads last committed state from the registry. 
2. Orchestrator launches the connector with input state, runner, and network. 
3. Connector fetches records newer than the input cursor and emits envelopes to Bronze. 
4. Connector returns the maximum cursor observed. 
5. Orchestrator commits the new cursor atomically in the state registry. 
6. Metrics and logs are recorded for the run.

## Inputs
- Connection profile
- Input state

## Outputs
- Emitted records in Bronze
- Updated state
- Run metrics

## Observability
- Records emitted count
- New cursor value
- Errors and retries
