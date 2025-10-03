# Flow: Schema Drift Handling

## Purpose
Describe how the platform detects and manages schema drift without blocking Bronze landing.

## Actors
- Connector
- Schema registry
- Stream registry
- Mapping registry
- Compat alerts service

## Steps
1. Connector emits discovered schemas. 
2. Schema registry compares schema hash to the active version. 
3. If different, mark as candidate and create a compatibility alert. 
4. Land data to Bronze without transformation. 
5. Mapping registry validates downstream mappings and blocks if unresolved. 
6. After review, promote candidate to active or require mapping updates.

## Inputs
- Discovered schema
- Previous schema version

## Outputs
- Compatibility alert
- Candidate schema
- Promotion event

## Observability
- Drift counters
- Impacted mappings
- Time to promotion
