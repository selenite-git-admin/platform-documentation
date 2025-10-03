# Flow: Connector Build and Publish

## Purpose
Describe how a connector moves from code to a certified artifact in the catalog.

## Actors
- Developer
- CI pipeline
- Catalog builder

## Steps
1. Developer commits code and manifest. 
2. CI validates manifest schema and runs unit, integration, and compliance tests. 
3. CI publishes artifact and manifest on success. 
4. Catalog builder aggregates manifests and publishes the updated catalog. 
5. Registry records new connector version and release channel.

## Inputs
- Source repo
- Connector manifest
- Test fixtures

## Outputs
- Connector artifact
- Updated catalog
- Registry entries

## Observability
- CI job logs
- Test reports
- Catalog build logs
