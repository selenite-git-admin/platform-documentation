# TALLY BACKUP INGESTION (REFERENCE)

## Purpose
Explain how Tally backup or dump files are ingested into the platform. 
Provide principles, supported patterns, trade-offs, and integration points. 
This document is a reference for architects and operators, not an implementation guide.

## Principle
Do not parse proprietary `.TSB` backup files directly. 
Always restore them into a Tally instance or export to intermediate files (CSV/XML) before ingestion. 
The connector is file-oriented and stateless. 
All state and schema management is owned by platform registries.

## Supported Patterns
1. **Scheduled Export**
   - Tally exports masters and vouchers into CSV/XML periodically.
   - Files are landed in S3 or SFTP.
   - Connector ingests new files incrementally.

2. **Restore and Export**
   - Backup archive is restored into a disposable Tally instance.
   - Scripts export data into CSV/XML.
   - Files are staged and ingested.

3. **Hybrid**
   - Use scheduled exports for incremental loads.
   - Use restore and export for one-time backfills.

## Trade-offs
- **Coverage**: Exports may not cover all tables; backup restore may be needed for full history.
- **Performance**: Large backfills better handled on AWS Glue.
- **Operational overhead**: Restore pipelines require manual or scripted processes.

## System Flow
1. Drop files into S3/SFTP (scheduled or restored export).  
2. Connector lists files and matches patterns.  
3. Connector reads rows, wraps them in envelopes.  
4. Orchestrator commits checkpoints (path+checksum).  
5. Schema registry validates inferred schemas and raises drift alerts.  

## Security and Compliance
- Encrypt files at rest and in transit.  
- Treat file names as sensitive if they contain identifiers.  
- Ensure retention policies for backup files.  
- Audit file access and connector runs.

## Example State
```json
{
  "tenant_id": "t1",
  "connector_id": "tally_file_dump",
  "stream_id": "file.s3.tally.vouchers_xml",
  "last_checkpoint": "s3://org/tally/vouchers/2025-09-30/vouchers.csv#sha256=abc"
}
```

## Example Metrics
- files_discovered=10
- files_processed=9
- rows_emitted=1,250,000
- drift_alerts=1

## Integration Points
- **State Registry**: Tracks last processed files.  
- **Schema Registry**: Stores inferred schemas.  
- **System Flows**: Incremental run lifecycle, schema drift handling.  
- **Global Connectors**: Reuse file connector abstractions.  

## Limitations
- Proprietary `.TSB` backup archives are opaque; must restore.  
- Export fidelity depends on Tally version and customizations.  
- File-based ingestion has inherent latency compared to direct ODBC/XML.

## Guidance
For production tenants, recommend scheduled exports into object storage as the primary pattern. 
Use restore and export pipelines only for historical migrations or backfills.
