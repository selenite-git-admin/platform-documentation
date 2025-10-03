# Flow: Failure and Retry

## Purpose
Describe how transient and terminal failures are handled during connector runs.

## Actors
- Orchestrator
- Connector
- Bronze sink

## Steps
1. Connector encounters an error and classifies it as retryable or terminal. 
2. For retryable errors, apply exponential backoff with jitter and resume paging. 
3. For terminal errors, stop the run and surface a clear error with context. 
4. State is not advanced for failed runs. 
5. On retry the run starts from the last committed checkpoint. 
6. Bronze landing remains idempotent to avoid duplicates.

## Inputs
- Input state
- Run configuration

## Outputs
- Error events
- Retry attempts
- Final status

## Observability
- Retry count
- Last successful cursor
- Failure classification
