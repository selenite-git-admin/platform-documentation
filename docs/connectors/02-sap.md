# SAP Connector

## Purpose
Connect to SAP to read or write structured data.

## Auth
Describe supported auth methods and how to load secrets.
Limit scope to the required modules.

## Discovery
List supported modules and tables or objects.
Describe how discovery produces a list of source objects.
Support filters by module and table name.

## CDC
Supported CDC modes:
- Append only by date time fields
- High water mark
- Log based when available

## Throughput
Describe pagination and parallelism.
Describe backoff strategy when the system throttles requests.

## Errors
Define error categories:
- Auth errors
- Input errors
- Transient transport errors
- Destination rejections

## Mapping to extraction schema
Explain how the connector fills extraction schema fields.
Explain how to set landing format and partition keys.

## Metrics and SLOs
Track rows, bytes, and errors.
Expose freshness and completeness metrics.
