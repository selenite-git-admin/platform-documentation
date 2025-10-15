# EDGAR REST CONNECTOR

## Purpose
Provide a connector for ingesting public company filings from the SEC EDGAR system. 
Supports the EDGAR RESTful API for metadata and document downloads. 
Standardizes discovery, incremental pulls, error handling, schema registration, and observability.

## Scope
- Company filings (10-K, 10-Q, 8-K, S-1, etc.)
- Metadata (company info, submission dates, form type)
- Document downloads in HTML, TXT, or XBRL

## Authentication
- No authentication required for public endpoints
- API key optional if enabled by SEC in future
- Secrets manager integration not required for baseline

## Network and Deployment
Runners
- AWS Lambda for scheduled incremental metadata pulls
- AWS Fargate for bulk filing downloads and parsing

Network patterns
- Public internet (NAT allowlist) for SEC endpoints

## Discovery
List filings by CIK (company identifier), ticker, or form type. 
Emit streams per company or per form type. 
Support dynamic addition of new companies to watch lists.

## Incremental Extraction
Use `filingDate` as a cursor. 
Support sliding windows to catch late amendments. 
Idempotency by compound key (cik, accession_number, filingDate).

## Manifest
```yaml
manifest_version: 1.0
id: conn::public::filings::edgar::sec::rest
name: EDGAR REST Connector
taxonomy:
  origin: public
  source: filings
  provider: sec
  product: edgar
  method: rest
runtime:
  supported_runners: [lambda, fargate]
  network_patterns: [nat_allowlist]
streams:
  strategy: discovery_or_config
  defaults:
    key_strategy: source_declared
    cursor_strategy: date_range
```

## Throttling and Retries
Respect SEC rate limits (no more than 10 requests per second). 
Retry on 429 and transient 5xx errors with exponential backoff.

## Error Handling
Surface accession number, company id, and filing type in logs. 
Skip malformed documents but record errors.

## Schema Handling
Emit metadata schema (cik, companyName, formType, filingDate, accessionNumber). 
Register schemas for each document type (10-K, 8-K, etc.). 
Support optional XBRL parsing for structured data.

## Observability
Metrics: filings discovered, filings downloaded, bytes, retries, errors. 
Logs: cik, accession number, form type, run id.

## Testing
Unit tests for pagination and cursor handling. 
Integration tests against sample EDGAR company filings.

## Limits and Considerations
- EDGAR endpoints have strict rate limits
- Some filings contain very large exhibits
- HTML parsing requires careful sanitization

## Relationships
Works with schema registry for filing metadata. 
Feeds CFO Pack and Financial KPI Packs for public companies.

## Exclusions
No onboarding or tenant flows. Public data only.
