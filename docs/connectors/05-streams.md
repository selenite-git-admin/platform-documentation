# Streams Connector

## Purpose
Subscribe to or publish to streaming systems.

## Auth
Use IAM or OAuth depending on the service.

## Systems
Support Kafka compatible endpoints and AWS services like Kinesis.

## Message shape
Define key and value schemas.
Record offsets and sequence numbers.

## Ordering
Declare ordering keys.
Handle out of order events.

## Errors
Handle poison messages.
Send failed messages to a DLQ topic.

## Mapping to extraction schema
Map stream fields to extraction schema fields.
Define subscription group names.

## Metrics and SLOs
Track messages, lag, and errors.
