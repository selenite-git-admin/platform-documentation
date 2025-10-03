# JDBC CONNECTOR (GLOBAL)

## Purpose
Provide a vendor independent JDBC connector for relational databases. 
It standardizes authentication, discovery, incremental extraction, and idempotent landing.

## Scope
Works with PostgreSQL, MySQL, SQL Server, Oracle, and other JDBC compatible databases. 
Covers catalog discovery, SQL pagination, cursors, retries, and observability.

## Authentication
- Username and password or IAM auth where supported
- Secrets from platform secrets store
- Optional TLS client certificates

## Network and Deployment
Runners
- AWS Fargate for most workloads
- AWS Glue for large backfills
- EC2 for special drivers

Network patterns
- VPN or PrivateLink to reach private databases
- VPC endpoints for managed services where available

## Discovery
Read JDBC metadata for catalogs, schemas, tables, and columns. 
Emit streams with stable ids such as jdbc.public.customers.

## Incremental Extraction
Use a cursor column such as updated_at or a numeric id. 
Page with LIMIT and ORDER BY. 
Fallback to full refresh where cursors do not exist.

## Manifest
```yaml
manifest_version: 1.0
id: conn::global::database::jdbc::extract
name: Global JDBC Connector
taxonomy:
  origin: enterprise
  source: database
  provider: generic
  product: jdbc
  method: extract
runtime:
  supported_runners: [fargate, glue, ec2]
  network_patterns: [vpn, private_link]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Limit concurrent connections. 
Backoff on lock timeouts and deadlocks. 
Use read only and repeatable read where possible.

## Error Handling
Retry transient network failures. 
Surface terminal errors with table name and SQL, without secrets.

## Schema Handling
Emit schemas from catalog. 
Track type widths and nullability. 
Register schemas in schema registry and raise drift alerts.

## Observability
Metrics: rows read, rows emitted, bytes, query latency, errors. 
Logs: database, schema, table, SQL hash, run id.

## Testing
Unit tests for SQL generation and pagination. 
Integration tests against representative databases.

## Limits and Considerations
- Large tables need partitioning predicates
- Time zone normalization for timestamp cursors
- Driver specific quirks must be abstracted in SDK

## Relationships
Uses state registry for cursors and schema registry for schemas.

## Exclusions
No business mappings or onboarding flows.
