# Scheduler Options

## Purpose
Choose how to trigger and coordinate pipeline runs.

## Options
- AWS Step Functions
- Amazon EventBridge Scheduler
- Amazon MWAA

## Guidance
Use Step Functions when you need workflow state and error handling.
Use EventBridge Scheduler for simple time based triggers.
Use MWAA only if the team standardizes on Airflow DAGs.

## Triggers
- Schedule
- Event
- Manual
- Replay

## Queues and limits
Control concurrency.
Protect downstream systems.
