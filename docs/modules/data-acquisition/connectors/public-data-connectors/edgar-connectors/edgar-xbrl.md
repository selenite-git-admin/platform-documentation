# EDGAR XBRL CONNECTOR

## Purpose
Provide a connector for ingesting structured XBRL data from SEC EDGAR filings. 
Supports parsing of 10-K, 10-Q, and other filings that contain inline XBRL. 
Standardizes schema extraction, mapping, and incremental updates.

## Scope
- Inline XBRL in company filings
- GAAP and IFRS taxonomies
- Extract key facts, contexts, and units

## Authentication
- None required (public data)

## Network and Deployment
Runners
- AWS Fargate for parsing large filings
- AWS Glue for heavy transformations and backfills

Network patterns
- NAT allowlist for SEC endpoints

## Discovery
Triggered by EDGAR REST Connector when new filings are detected. 
Emit streams per filing accession number. 
Fact-level streams keyed by (cik, accession, concept).

## Incremental Extraction
Use accession number as the cursor. 
Only parse new or amended filings. 
Ensure idempotency by storing fact id (cik, accession, concept, contextRef).

## Manifest
```yaml
manifest_version: 1.0
id: conn::public::filings::edgar::sec::xbrl
name: EDGAR XBRL Connector
taxonomy:
  origin: public
  source: filings
  provider: sec
  product: edgar
  method: xbrl
runtime:
  supported_runners: [fargate, glue]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery_from_trigger
  defaults:
    key_strategy: synthetic_fact_id
    cursor_strategy: accession_number
```

## Throttling and Retries
Retry transient download errors. 
Throttle parsing jobs to avoid resource exhaustion.

## Error Handling
Skip invalid facts but log cik, accession, and concept. 
Surface schema errors separately.

## Schema Handling
Generate schema from taxonomy (GAAP, IFRS). 
Register schemas in registry with versioning. 
Drift alerts when taxonomy updates.

## Observability
Metrics: facts parsed, filings parsed, errors. 
Logs: cik, accession, concept count, run id.

## Testing
Unit tests for fact id generation. 
Integration tests with sample filings.

## Limits and Considerations
- Taxonomy evolves annually
- Some filings contain custom extensions that must be preserved

## Relationships
Triggered by EDGAR REST connector. 
Feeds CFO Pack metrics computation. 
Works with schema registry for taxonomy schemas.

## Exclusions
No onboarding or tenant flows.
