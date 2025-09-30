# Connectors — Overview

## Purpose
Describe how the platform connects to sources and destinations.
Provide a consistent model for auth, discovery, change data capture, throughput, and errors.

## Scope
Cover inbound connectors for extract pipelines.
Cover outbound connectors for put back pipelines.

## Principles
Prefer least privilege for credentials.
Prefer idempotent operations.
Record evidence for each operation.

## Capabilities
- Authentication and secrets handling
- Object discovery and selection
- Supported CDC modes
- Throughput limits and backoff
- Error taxonomy and retry rules
- Mapping to extraction schema fields
- Operational metrics and SLOs

## Interfaces
Connectors read configuration from contracts and run configs.
Connectors emit logs, metrics, and evidence.
