# STREAMING CONNECTOR (GLOBAL)

## Purpose
Provide a connector for streaming platforms such as Kafka, Kinesis, and Pulsar. 
It standardizes subscription, checkpointing, and idempotent landing to Bronze.

## Scope
Supports consuming from topics or streams with partition awareness. 
Handles offsets, at least once delivery, and retry with backpressure.

## Authentication
- IAM for Kinesis
- SASL for Kafka
- Secrets from platform secrets store

## Network and Deployment
Runners
- AWS Fargate for persistent consumers
- EC2 for custom drivers or high throughput

Network patterns
- VPC peering or PrivateLink for managed Kafka
- VPC endpoints for Kinesis

## Discovery
Configuration driven. 
List topics and partitions to subscribe to. 
Emit streams per topic or logical group.

## Incremental Processing
Use partition offsets or sequence numbers as cursors. 
Commit offsets in the state registry after successful landing.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::streaming::kafka_kinesis::consume
name: Global Streaming Connector
taxonomy:
  origin: enterprise
  source: streaming
  provider: generic
  product: streams
  method: consume
runtime:
  supported_runners: [fargate, ec2]
  network_patterns: [private_link, vpc_endpoint]
streams:
  strategy: config_defined
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: partition_offset
```

## Throttling and Retries
Use consumer lag metrics to adjust concurrency. 
Retry transient errors and re balance on partition changes.

## Error Handling
Send poison messages to DLQ after retry budget. 
Surface partition, offset, and error reason.

## Schema Handling
Register event schemas in the schema registry. 
Evolve with compatibility checks.

## Observability
Metrics: messages, lag, errors, retries. 
Logs: partition, offset, key, run id.

## Testing
Unit tests for offset commit logic and partition assignment. 
Integration tests with test clusters.

## Limits and Considerations
- Ordering guarantees are per partition
- Backpressure must be handled to avoid lag explosions

## Relationships
Uses state registry for offsets and schema registry for payloads.

## Exclusions
No GDP mappings or onboarding.
