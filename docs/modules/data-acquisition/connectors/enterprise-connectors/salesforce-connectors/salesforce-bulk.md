# SALESFORCE BULK

## Purpose
Describe development requirements for the Salesforce Bulk API connector.

## Scope
Extracts large volumes of Salesforce data using Bulk API v2. 
Supports query jobs, batch processing, and incremental extraction using SystemModstamp.

## Supported Versions
- Salesforce orgs with Bulk API v2 enabled

## Authentication
OAuth 2.0 refresh token flow. 
Secrets come from platform secrets store.

## Network and Deployment
Supported runners
- AWS Fargate for large exports
- AWS Glue for backfills

Network patterns
- NAT allowlist for Salesforce endpoints

## Discovery
Use REST API discovery first to list objects and fields. 
Confirm if object is supported for bulk extraction.

## Incremental Extraction
Use SystemModstamp in SOQL with Bulk API jobs. 
Paginate by batchId until complete.

SOQL example
```sql
SELECT Id, Amount, SystemModstamp 
FROM Opportunity 
WHERE SystemModstamp > :cursor
```

## Manifest
```yaml
manifest_version: 1.0
id: conn::enterprise-connectors::crm::salesforce::cloud::bulk
name: Salesforce Bulk API Connector
taxonomy:
  origin: enterprise-connectors
  source: crm
  provider: salesforce
  product: cloud
  method: bulk
runtime:
  supported_runners: [fargate, glue]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
```

## Throttling and Retries
Bulk jobs have per org limits. 
Use polling with exponential backoff. 
Retry incomplete or failed jobs by creating new job with same query.

## Error Handling
Classify errors clearly.
- Retryable: job timeout, transient 5xx
- Terminal: invalid SOQL, object not supported

## Schema Handling
Emit schemas via describe calls and store in schema registry. 
Raise drift alerts on changes.

## Observability
Log jobId, batchId, object name, run id. 
Metrics: records processed, batches completed, errors, retries.

## Testing
Unit tests for SOQL generation and job polling logic. 
Integration tests with sandbox orgs. 
Certification in Fargate and Glue.

## Limits and Considerations
- Bulk jobs are asynchronous; latency is higher
- Some objects not supported by Bulk API
- File downloads must be chunked for large result sets

## Relationships
Uses state registry for SystemModstamp and schema registry for schemas.

## Exclusions
No GDP mappings or onboarding flows.
