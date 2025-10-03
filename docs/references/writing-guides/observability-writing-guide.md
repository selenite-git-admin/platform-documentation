# Observability Writing Guide

## Scope
Define metrics, logs, traces, dashboards, alerts, and SLOs for a module.

## Structure
1. Scope
2. Metrics
3. Logs
4. Traces
5. Dashboards
6. Alerts
7. SLOs
8. Retention and sampling

## Metrics
For each metric include
- Name
- Type (counter, gauge, histogram)
- Labels and allowed values
- Unit
- Purpose

## Logs
Define structured events with fields and examples. List event names and when they are emitted.

## Traces
List spans and their relationships. Include attributes and links to metrics and logs by correlation id.

## Dashboards
List required views and graphs. Name data sources.

## Alerts
Define conditions, thresholds, and runbooks to follow. Include alert names and suppression rules.

## SLOs
State objectives, measurement windows, and burn alerts if used.

## Retention and sampling
Document log and trace retention and any sampling strategy.
