# SAP RFC

## Purpose
Describe the development requirements for the SAP ECC RFC connector. 
Explain how function modules are called, how tables are extracted, and how incremental and idempotent behavior is achieved.

## Scope
Reads data from SAP ECC or compatible systems through RFC. 
Supports discovery by configured table or function module lists, incremental extraction using timestamp or numeric cursors, and chunked pagination for large result sets. 
Includes authentication, networking, error handling, observability, and certification.

## Supported Versions
- SAP ECC 6.x with RFC SDK available to the runtime
- SAP S4HANA systems that still expose RFC targets when permitted
RFC libraries must be provided as part of the artifact and must be compatible with the runner environment.

## Authentication
Supported modes
- SAP user and password with least privilege roles
- SNC optional when available
Secrets are retrieved from the platform secrets store at runtime.

## Network and Deployment
Supported runners
- AWS Fargate for containerized execution with native libraries
- Amazon EC2 when special drivers or kernel modules are required

Supported network patterns
- Site to site VPN for on premises systems
- PrivateLink to an internal NLB when available
Avoid public exposure. NAT allowlist is discouraged for RFC unless there is a specific exception.

## Discovery
RFC does not expose a uniform metadata catalog for all tables. 
Discovery is driven by configuration that lists function modules or table names. 
The connector emits streams based on entries in this configuration and validates access at start.

Example configuration snippet
```yaml
rfc_targets:
  - name: BSEG
    function: RFC_READ_TABLE
    options:
      where: "GJAHR >= 2022"
      fields: ["BELNR","GJAHR","BUKRS","CPUDT"]
```

## Incremental Extraction
Preferred cursor fields include CPUDT or AEDAT for many finance tables. 
The connector accepts an input state and builds RFC_READ_TABLE predicates accordingly.

Example predicate
```
WHERE CPUDT > '2025-09-30'
```

Paging
- Use RFC rowcount with offset for pagination
- Tune batch size to balance throughput and memory

Safety window
- Apply a safety window in days when timestamps are date only
```yaml
safety_window: P1D
```

## Manifest
Minimal fragment
```yaml
manifest_version: 1.0
id: conn::enterprise::erp::sap::sap_ecc::rfc
name: SAP ECC RFC Connector
taxonomy:
  origin: enterprise
  source: erp
  provider: sap
  product: ecc
  method: rfc
runtime:
  supported_runners: [fargate, ec2]
  network_patterns: [vpn, private_link]
streams:
  strategy: discovery_by_config
  defaults:
    key_strategy: source_declared_or_config
    cursor_strategy: source_declared_or_full_refresh
observability:
  logs: json_structured
  metrics: standard_connector_metrics
  tracing: opentelemetry
compliance:
  sensitive_data: pii
  security_controls: secrets_manager
```

## Throttling and Retries
RFC servers may throttle implicitly. 
Use small page sizes and backoff on busy signals. 
Retry transient network errors and timeouts with jitter.

## Error Handling
Classify errors clearly.
- Retryable: timeout, temporary network failure
- Terminal: authorization failure, missing table, invalid WHERE clause
Return clear messages with function name and target, without secrets.

## Schema Handling
Do not embed schemas in the manifest. 
Emit field lists discovered at start. 
Register discovered schemas in the schema registry and track type widths such as NUMC or CHAR lengths.

## Observability
Include function name, target table, row counts, and latency in metrics. 
Log RFC return codes and request identifiers. 
Trace each call so that retries are linked to the same run id.

## Testing
Unit tests for predicate construction, paging, and type coercion. 
Integration tests against a sandbox with representative tables. 
Certification in Fargate and EC2 with at least one VPN scenario.

## Limits and Considerations
- NUMC and packed decimals require precise conversion
- Some tables are very large and need partitioning by company code or year
- RFC_READ_TABLE has row length limits. Use custom function modules when needed

## Relationships
State registry manages CPUDT or AEDAT checkpoints. 
Schema registry stores discovered field definitions and lengths.

## Exclusions
No business mapping or KPI logic. No tenant onboarding instructions.
