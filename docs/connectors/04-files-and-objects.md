# Files and Objects Connector

## Purpose
Read and write files in object storage.

## Auth
Use IAM roles where possible.
Limit bucket permissions by path.

## Formats
Support CSV, JSON, Parquet, and Avro.
Record compression and encoding.

## Partitioning
Allow date based and key based partitions.
Document layout and naming.

## CDC
Use file arrival time or embedded watermarks.
Support replay by path and time.

## Errors
Handle corrupt files and schema drift.
Quarantine corrupt files to a DLQ.

## Mapping to extraction schema
Map file format and columns to extraction schema fields.
Define path, partition keys, and compression.

## Metrics and SLOs
Track files processed, rows, and errors.
