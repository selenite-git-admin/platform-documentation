# Flow: Catalog Generation

## Purpose
Describe how the developer catalog is generated from manifests and certification results.

## Actors
- Catalog builder
- CI pipeline
- Registry

## Steps
1. Catalog builder scans repository for connector manifests. 
2. Manifests are validated against the schema. 
3. Certification results are joined to the manifest data. 
4. Aggregated catalog is written to the registry and documentation. 
5. Lifecycle and release channel metadata are surfaced.

## Inputs
- Connector manifests
- Certification results

## Outputs
- Developer catalog
- Capability matrix

## Observability
- Catalog build logs
- Validation errors
