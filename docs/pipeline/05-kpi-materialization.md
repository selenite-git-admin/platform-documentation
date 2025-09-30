# KPI Materialization

## Purpose
Create Gold serving tables or views for analytics and activation.
Use the KPI schema contract to define grain and metrics.

## Grain and metrics
Declare the record grain.
Declare metrics with types and clear definitions.
Document units and currency rules.

## Materialization
Choose table, view, incremental table, or cube.
Define refresh plan and retention.

## Time and currency
Support standard and fiscal calendars.
Apply currency conversion at the correct time.

## Performance
Select partition and clustering keys.
Add pre aggregations when needed.

## Evidence
Record metric completeness and freshness.


## Behavior when KPI is not ready

## Behavior when KPI is not ready
If there is no Active KPI contract, the pipeline skips this stage.
The system records a SKIPPED status for KPI.
The system continues to run earlier stages.
