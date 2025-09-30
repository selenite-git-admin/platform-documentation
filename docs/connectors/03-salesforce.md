# Salesforce Connector

## Purpose
Connect to Salesforce to read or write objects.

## Auth
Use OAuth with the minimum required scopes.
Rotate tokens on schedule.

## Discovery
List objects and fields.
Support include and exclude lists.

## CDC
Preferred modes:
- Incremental by SystemModstamp
- Change Data Capture when licensed

## Throughput
Respect API limits.
Use batch sizes that fit limits.
Use backoff when rate limits fire.

## Errors
Define categories for errors and how to retry.
Handle partial successes for bulk APIs.

## Mapping to extraction schema
Show how to map object fields to extraction schema columns.
Show how to capture CDC markers.

## Metrics and SLOs
Track API calls, rows, success ratio, and latency.
