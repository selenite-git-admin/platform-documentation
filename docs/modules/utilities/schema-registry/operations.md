# Schema Registry Operations

## Service Level Objectives

- Read availability: 99.99 percent  
- Publish latency: 95th percentile under 200 ms  
- Validation throughput: 50 per second per tenant  

## Observability

- Metrics: publish count, validate count, read latency, queue depth  
- Logs: structured with request_id, tenant_id, schema_id, version, actor  
- Traces: per API call, linked to validation workers  

## Runbooks

- How to promote schemas  
- How to roll back schemas  
- How to force deprecate with exception  
- How to restore registry from backup  

## Failure Handling

- Policy engine down → approvals blocked, reads continue  
- Storage down → reads from replicas, writes queue  
- Validation timeout → retry with backoff, failures go to DLQ
