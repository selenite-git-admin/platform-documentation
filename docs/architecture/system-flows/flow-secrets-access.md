# Flow: Secrets Access

## Purpose
Describe how connectors retrieve secrets securely at runtime.

## Actors
- Connector
- Secrets management service
- Orchestrator

## Steps
1. Orchestrator injects secret references into the runtime environment. 
2. Connector requests the secret value from the secrets service using the reference. 
3. Secrets service returns the value with access logged. 
4. Connector uses the secret in memory only and does not persist it. 
5. When the run completes the environment is destroyed.

## Inputs
- Secret references

## Outputs
- Temporary credentials in memory
- Audit trail

## Observability
- Secrets access logs
- Connector auth logs
