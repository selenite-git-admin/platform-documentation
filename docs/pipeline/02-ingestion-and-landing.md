# Ingestion and Landing

## Purpose
Ingest data from a source and create a landing artifact.
Validate the landed data against the extraction schema.

## Source modes
- Database pull with table scan or CDC
- API pull with pagination
- File drop on object storage
- Stream subscription

## Landing formats
- Table landing in a database
- Files in object storage
- Stream topics for downstream

## CDC strategies
- Append only
- High water mark
- Log based
- Merge on keys

## Partitioning and layout
Define partition keys and layout for each landing.
Document compression and encoding.

## Evidence
Record bytes, rows, partitions, and checkpoints.
Record source timestamps and extractor version.

## Failure and retry
Define retry policy.
Quarantine bad inputs to a DLQ for inspection.
